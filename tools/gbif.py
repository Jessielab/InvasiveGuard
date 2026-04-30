# 工具：GBIF API Sensor

import requests
from datetime import datetime
import config


def get_species_key(scientific_name: str) -> int:
    """用拉丁名查询GBIF的usageKey"""
    params = {"name": scientific_name}
    resp = requests.get(config.GBIF_SPECIES_API, params=params)
    return resp.json().get("usageKey", 0)


def fetch_occurrence_stats(species_key: int, country_code: str) -> dict:
    """获取GBIF上目标物种的记录统计"""
    current_year = datetime.now().year

    # 全部历史
    params_all = {"taxonKey": species_key, "country": country_code, "limit": 0}
    resp_all = requests.get(config.GBIF_OCCURRENCE_API, params=params_all)
    total_historical = resp_all.json().get("count", 0)

    # 近3年
    recent_total = 0
    for year in range(current_year - config.YEARS_BACK, current_year):
        params_year = {
            "taxonKey": species_key,
            "country": country_code,
            "year": year,
            "limit": 0
        }
        resp_year = requests.get(config.GBIF_OCCURRENCE_API, params=params_year)
        recent_total += resp_year.json().get("count", 0)

    return {
        "total_historical": total_historical,
        "recent_3yr": recent_total
    }