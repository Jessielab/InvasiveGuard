"""
InvasiveGuard —— 入侵物种早期预警Agent
主循环入口（含IUCN交叉验证）
"""

import os
from dotenv import load_dotenv
from tools.input_parser import parse_user_input
from tools.inaturalist import fetch_observations as sensor_inat
from tools.gbif import get_species_key, fetch_occurrence_stats as sensor_gbif
from tools.iucn import fetch_assessment as sensor_iucn
from tools.risk_engine import assess as assess_risk
from tools.llm_analyzer import analyze as actuator_analyze

load_dotenv()


def print_banner():
    print("=" * 60)
    print("🛡️  InvasiveGuard —— 入侵物种早期预警Agent")
    print("=" * 60)
    print("\n支持两种输入方式：")
    print("  1. 自然语言：爬山虎，中国")
    print("  2. 精确输入：Parthenocissus tricuspidata, CN")
    print()


def main():
    api_key = os.getenv("API_KEY")
    iucn_key = os.getenv("IUCN_API_KEY")
    
    if not api_key:
        print("❌ 未找到 API_KEY，请在 .env 文件中设置。")
        return

    print_banner()
    user_input = input("请输入物种和国家（用逗号分隔）: ").strip()
    if not user_input:
        print("❌ 输入不能为空，程序退出。")
        return

    # ─── 步骤0: 解析输入 ───
    print(f"\n📝 [输入解析] 正在理解您的查询...")
    parsed = parse_user_input(api_key, user_input)
    species = parsed["species"]
    country = parsed["country_code"]
    print(f"   解析结果：物种 = {species} | 国家代码 = {country}")
    if parsed["original_name"] != species:
        print(f"   （原始输入：{parsed['original_name']}）")

    # ─── Sensor 1: iNaturalist ───
    print(f"\n📸 [Sensor 1] 正在查询 iNaturalist...")
    inat_data = sensor_inat(species, parsed["inat_place_id"])
    print(f"   ✅ 近3年记录数: {inat_data['total']}")

    # ─── Sensor 2: GBIF ───
    print(f"\n🔍 [Sensor 2] 正在查询 GBIF...")
    species_key = get_species_key(species)
    if species_key == 0:
        print(f"   ⚠️  未能在GBIF中找到该物种")
        gbif_data = {"total_historical": 0, "recent_3yr": 0}
    else:
        print(f"   GBIF usageKey: {species_key}")
        gbif_data = sensor_gbif(species_key, country)
        print(f"   ✅ 全部历史: {gbif_data['total_historical']} | 近3年: {gbif_data['recent_3yr']}")

    # ─── Sensor 3: IUCN ───
    iucn_data = None
    if iucn_key:
        print(f"\n🌍 [Sensor 3] 正在查询 IUCN 受威胁物种名录（本地数据）...")
        iucn_data = sensor_iucn(species)
        if iucn_data.get("found"):
            print(f"   保护等级: {iucn_data.get('category', '未知')} ({iucn_data.get('meaning', '')})")
        else:
            print(f"   ⚠️ {iucn_data['category']}")
    else:
        print(f"\n🌍 [Sensor 3] 未配置IUCN_API_KEY，跳过IUCN查询")

    # ─── Agent推理 ───
    print(f"\n🧠 [Agent推理] 正在对比两侧数据...")
    risk = assess_risk(
        inat_count=inat_data["total"],
        gbif_total=gbif_data["total_historical"],
        gbif_recent=gbif_data["recent_3yr"]
    )
    print(f"   风险等级: {risk['level']}")
    print(f"   判断依据: {risk['reason']}")

    # ─── Actuator: 大模型分析 ───
    if risk["code"] in ["HIGH", "MEDIUM", "WATCH"]:
        print(f"\n🤖 [Actuator] 触发大模型生态学分析...")
        analysis = actuator_analyze(
            api_key=api_key,
            species=species,
            country=country,
            gbif_total=gbif_data["total_historical"],
            gbif_recent=gbif_data["recent_3yr"],
            inat_total=inat_data["total"],
            inat_locations="\n".join(inat_data["locations"][:8]),
            inat_descriptions="\n---\n".join(inat_data["sample_descriptions"][:5]),
            risk_level=risk["level"],
            risk_reason=risk["reason"],
            iucn_data=iucn_data
        )
        print(f"\n{'=' * 60}")
        print(f"📋 预警分析报告")
        print(f"{'=' * 60}")
        print(f"物种: {species}")
        print(f"区域: {country}")
        print(f"风险等级: {risk['level']}")
        if iucn_data and iucn_data.get("found"):
            print(f"IUCN保护等级: {iucn_data.get('category', '未知')} ({iucn_data.get('meaning', '')})")
        print(f"{'=' * 60}")
        print(analysis)
        print(f"{'=' * 60}")
    else:
        print(f"\n✅ 风险等级正常，无需触发预警分析。")

    print("\n程序运行完毕。")


if __name__ == "__main__":
    main()