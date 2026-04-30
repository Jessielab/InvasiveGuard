# 工具：自然语言输入解析

import json
import requests
import config
from prompts import get_parse_prompt


# iNaturalist 地点ID映射表（ISO代码 → iNaturalist数字ID）
INAT_PLACE_IDS = {
    "CN": 6784,     # 中国
    "US": 1,        # 美国
    "JP": 6785,     # 日本
    "KR": 6791,     # 韩国
    "GB": 6857,     # 英国
    "IN": 6681,     # 印度
    "AU": 6744,     # 澳大利亚
    "BR": 6879,     # 巴西
    "DE": 8052,     # 德国
    "FR": 6757,     # 法国
    "CA": 6712,     # 加拿大
    "MX": 6793,     # 墨西哥
    "IT": 6860,     # 意大利
    "ES": 6753,     # 西班牙
    "NL": 7507,     # 荷兰
    "SE": 6956,     # 瑞典
    "NZ": 6803,     # 新西兰
    "ZA": 6986,     # 南非
    "AR": 6850,     # 阿根廷
    "CL": 6868,     # 智利
}


def parse_user_input(api_key: str, user_input: str) -> dict:
    """
    用大模型将自然语言翻译为结构化查询参数
    返回: {"species": "拉丁学名", "country_code": "CN", "inat_place_id": 6784, "original_name": "原始输入"}
    """
    prompt = get_parse_prompt(user_input)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": config.LLM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": config.LLM_TEMPERATURE_PARSE,
        "response_format": {"type": "json_object"}
    }

    resp = requests.post(config.LLM_API, headers=headers, json=payload)

    try:
        content = resp.json()["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        country_code = parsed.get("country_code", "CN").upper()
        return {
            "species": parsed.get("species", user_input),
            "country_code": country_code,
            "inat_place_id": INAT_PLACE_IDS.get(country_code, 1),  # 默认美国
            "original_name": parsed.get("original_name", user_input)
        }
    except (json.JSONDecodeError, KeyError):
        parts = user_input.replace("，", ",").split(",")
        country_code = parts[1].strip().upper() if len(parts) > 1 else "CN"
        return {
            "species": parts[0].strip(),
            "country_code": country_code,
            "inat_place_id": INAT_PLACE_IDS.get(country_code, 1),
            "original_name": user_input
        }