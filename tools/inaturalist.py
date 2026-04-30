# 工具：iNaturalist API Sensor

import requests
from datetime import datetime
import config


def fetch_observations(species_name: str, inat_place_id: int) -> dict:
    """
    获取iNaturalist上目标物种在目标区域的近年观察记录
    参数：
        species_name: 物种拉丁名
        inat_place_id: iNaturalist内部数字地点ID（不是ISO代码）
    """
    current_year = datetime.now().year
    params = {
        "taxon_name": species_name,
        "place_id": inat_place_id,          # 使用数字ID
        "d1": f"{current_year - config.YEARS_BACK}-01-01",
        "d2": f"{current_year}-12-31",
        "per_page": config.INAT_PER_PAGE,
        "order": "desc",
        "order_by": "created_at",
        "quality_grade": "any"              # 获取所有数据
    }

    resp = requests.get(config.INATURALIST_API, params=params)
    data = resp.json()
    results = data.get("results", [])

    locations = []
    descriptions = []
    for obs in results:
        place = obs.get("place_guess", "未知地点")
        observed_on = obs.get("observed_on", "日期未知")
        desc = obs.get("description", "")
        locations.append(f"{observed_on} - {place}")
        if desc:
            descriptions.append(f"[{observed_on}, {place}] {desc[:200]}")

    return {
        "total": data.get("total_results", 0),
        "locations": locations[:20],
        "sample_descriptions": descriptions[:config.INAT_DESC_SAMPLE]
    }