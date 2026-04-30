# 工具：大模型生态学分析 Actuator

import requests
import config
from prompts import get_analysis_prompt


def analyze(api_key: str, species: str, country: str,
            gbif_total: int, gbif_recent: int,
            inat_total: int, inat_locations: str, inat_descriptions: str,
            risk_level: str, risk_reason: str) -> str:
    """调用大模型进行生态学解读"""

    prompt = get_analysis_prompt(
        species=species,
        country=country,
        gbif_total=gbif_total,
        gbif_recent=gbif_recent,
        inat_total=inat_total,
        inat_locations=inat_locations,
        inat_descriptions=inat_descriptions,
        risk_level=risk_level,
        risk_reason=risk_reason
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": config.LLM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": config.LLM_TEMPERATURE_ANALYSIS
    }

    resp = requests.post(config.LLM_API, headers=headers, json=payload)
    return resp.json()["choices"][0]["message"]["content"]