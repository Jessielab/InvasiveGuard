# 工具：iNaturalist API Sensor (修复版 - 使用通用搜索接口)
import requests
from datetime import datetime
import config

def fetch_observations(species_name: str, place_code: str) -> dict:
    """
    通过 iNaturalist 通用搜索接口获取指定物种在目标区域的观察记录。
    核心改动：放弃有字符限制的 taxon_name 参数，改用 /v1/search 接口。
    """
    current_year = datetime.now().year
    
    # 第一步：调用通用 /search 接口，根据物种名和地点模糊查找，不再限制数据质量级别
    search_url = "https://api.inaturalist.org/v1/search"
    search_params = {
        "q": species_name,
        "sources": "taxa",           # 限定搜索分类单元
        "place_id": place_code,
        "per_page": 1               # 只需要拿到系统里匹配到的准确内部ID
    }
    
    try:
        search_resp = requests.get(search_url, params=search_params)
        search_data = search_resp.json()
        # 提取第一个匹配结果的内部ID
        search_results = search_data.get("results", [])
        if not search_results:
            print(f"   ⚠️ iNaturalist 搜索接口也未找到匹配 '{species_name}' 的结果")
            return {"total": 0, "locations": [], "sample_descriptions": []}
            
        # iNaturalist 内部统一用数字 ID 标识物种，拿到这个 ID 才能精准获取其观察记录
        taxon_id = search_results[0].get("record", {}).get("id")
        if not taxon_id:
            print(f"   ⚠️ 找到匹配但未能提取到物种ID")
            return {"total": 0, "locations": [], "sample_descriptions": []}
            
        print(f"   ✅ iNaturalist映射成功，内部Taxon ID: {taxon_id}")
        
    except Exception as e:
        print(f"   ❌ 调用iNaturalist搜索接口异常: {e}")
        return {"total": 0, "locations": [], "sample_descriptions": []}

    # 第二步：用获取到的准确 taxon_id 去获取观察记录详情
    obs_url = "https://api.inaturalist.org/v1/observations"
    obs_params = {
        "taxon_id": taxon_id,        # 使用准确的 ID 替代有Bug的 taxon_name
        "place_id": place_code,
        "d1": f"{current_year - config.YEARS_BACK}-01-01",
        "d2": f"{current_year}-12-31",
        "per_page": config.INAT_PER_PAGE,
        "order": "desc",
        "order_by": "created_at",
        "quality_grade": "any"       # 获取所有数据，而非默认的“研究级”
    }

    try:
        obs_resp = requests.get(obs_url, params=obs_params)
        obs_data = obs_resp.json()
        results = obs_data.get("results", [])
    except Exception as e:
        print(f"   ❌ 调用iNaturalist观察记录接口异常: {e}")
        return {"total": 0, "locations": [], "sample_descriptions": []}

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
        "total": obs_data.get("total_results", 0),
        "locations": locations[:20],
        "sample_descriptions": descriptions[:config.INAT_DESC_SAMPLE]
    }