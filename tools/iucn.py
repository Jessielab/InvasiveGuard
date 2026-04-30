# 工具：IUCN Red List 本地CSV查询
# 数据来源：IUCN受威胁物种名录（已下载至本地）

import csv
import os

# CSV文件路径（相对于项目根目录）
CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "iucn_threatened_species.csv")

# 等级含义映射
CATEGORY_MEANING = {
    "EX": "灭绝",
    "EW": "野外灭绝",
    "CR": "极危",
    "EN": "濒危",
    "VU": "易危",
    "NT": "近危",
    "LC": "无危",
    "DD": "数据缺乏",
}


def _load_csv() -> dict:
    """
    将CSV文件加载为字典：{学名小写: {"category": 等级, "full_name": 原始学名}}
    只在第一次调用时加载，后续使用缓存
    """
    if not hasattr(_load_csv, "_cache"):
        data = {}
        try:
            with open(CSV_PATH, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name = row.get("scientific_name", "").strip()
                    category = row.get("category", "").strip()
                    if name and category:
                        data[name.lower()] = {
                            "category": category,
                            "full_name": name,
                        }
        except FileNotFoundError:
            print(f"   ⚠️ 未找到IUCN CSV文件: {CSV_PATH}")
        except Exception as e:
            print(f"   ⚠️ 读取IUCN CSV出错: {e}")
        
        _load_csv._cache = data
    
    return _load_csv._cache


def fetch_assessment(species_name: str) -> dict:
    """
    在本地IUCN CSV中查询物种保护等级
    参数：species_name - 拉丁学名
    返回：{"found": bool, "category": str, "meaning": str, "full_name": str}
    """
    data = _load_csv()
    
    # 精确匹配
    name_lower = species_name.strip().lower()
    if name_lower in data:
        entry = data[name_lower]
        return {
            "found": True,
            "category": entry["category"],
            "meaning": CATEGORY_MEANING.get(entry["category"], entry["category"]),
            "full_name": entry["full_name"],
        }
    
    # 模糊匹配：遍历所有键，看是否包含输入的物种名
    for key, entry in data.items():
        if name_lower in key:
            return {
                "found": True,
                "category": entry["category"],
                "meaning": CATEGORY_MEANING.get(entry["category"], entry["category"]),
                "full_name": entry["full_name"],
            }
    
    return {
        "found": False,
        "category": "未收录",
        "meaning": "该物种不在IUCN受威胁物种名录中",
        "full_name": species_name,
    }