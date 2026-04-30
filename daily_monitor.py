import os
import time
from datetime import datetime
from dotenv import load_dotenv

import config
from tools.iucn import get_threatened_species
from tools.inaturalist import fetch_observations
from tools.email_notifier import send_report

load_dotenv()


def check_species(species_name: str) -> dict:
    data = fetch_observations(species_name, inat_place_id=1)
    
    if data["total"] == 0:
        return {"has_new": False, "total": 0, "latest": "", "location": ""}
    
    latest = data["locations"][0] if data["locations"] else "未知"
    return {
        "has_new": True,
        "total": data["total"],
        "latest": latest,
        "location": latest.split(" - ")[-1] if " - " in latest else latest
    }


def main():
    print("=" * 60)
    print("🛡️  InvasiveGuard —— 濒危物种每日监测")
    print(f"   运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   监测等级: {', '.join(config.MONITOR_CATEGORIES)}")
    print("=" * 60)

    sender_email = os.getenv("EMAIL_SENDER")
    sender_password = os.getenv("EMAIL_PASSWORD")
    receiver_email = os.getenv("EMAIL_RECEIVER")

    if not all([sender_email, sender_password, receiver_email]):
        print("❌ 邮件配置不完整，请在 .env 中设置")
        return

    print(f"\n📋 [步骤1] 正在从IUCN名录加载 {', '.join(config.MONITOR_CATEGORIES)} 等级物种...")
    threatened = get_threatened_species(config.MONITOR_CATEGORIES)
    print(f"   共 {len(threatened)} 个物种")

    print(f"\n🔍 [步骤2] 正在逐一查询 iNaturalist 近期观察...")
    print("   (先用前10个物种快速测试)")
    new_discoveries = []
    
    # TODO: 测试通过后删掉 [:10]
    for i, sp in enumerate(threatened[:10]):
        name = sp["scientific_name"]
        try:
            result = check_species(name)
            if result["has_new"]:
                new_discoveries.append({
                    "species": name,
                    "category": f"{sp['category']}（{sp['meaning']}）",
                    "location": result["location"],
                    "observed_on": result["latest"][:10] if result["latest"] else "未知"
                })
                print(f"   🆕 发现: {name} - {result['location']}")
        except Exception as e:
            print(f"   ⚠️ 查询 {name} 失败: {e}")
        
        time.sleep(1)

    print(f"\n   查询完毕: 发现 {len(new_discoveries)} 条新观察")

    print(f"\n📧 [步骤3] 正在发送邮件报告...")
    send_report(sender_email, sender_password, receiver_email, new_discoveries)

    print("\n✅ 每日监测任务完成。")


if __name__ == "__main__":
    main()
