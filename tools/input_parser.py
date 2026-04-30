# 工具：自然语言输入解析

import json
import requests
import config
from prompts import get_parse_prompt


def parse_user_input(api_key: str, user_input: str) -> dict:
    """
    用大模型将自然语言翻译为结构化查询参数
    返回: {"species": "拉丁学名", "country_code": "CN", "original_name": "原始输入"}
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
        return {
            "species": parsed.get("species", user_input),
            "country_code": parsed.get("country_code", "CN").upper(),
            "original_name": parsed.get("original_name", user_input)
        }
    except (json.JSONDecodeError, KeyError):
        # 降级：简单拆分
        parts = user_input.replace("，", ",").split(",")
        return {
            "species": parts[0].strip(),
            "country_code": parts[1].strip().upper() if len(parts) > 1 else "CN",
            "original_name": user_input
        }