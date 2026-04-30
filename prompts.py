# 提示词模板：集中管理所有大模型提示词

def get_parse_prompt(user_input: str) -> str:
    """自然语言 → 结构化查询参数"""
    return f"""你是一个生物信息学助手。用户想查询一个物种在某个国家/地区的分布数据。

用户的输入是："{user_input}"

请完成以下任务：
1. 识别物种：将俗名/中文名翻译为标准的拉丁学名。如果用户已经输入了拉丁名，直接保留。
2. 识别国家：将国家名称（全称/简称/中文/英文）翻译为ISO 3166-1 alpha-2双字母国家代码。

请严格按以下JSON格式输出，不要输出其他内容：
{{
    "species": "拉丁学名",
    "country_code": "双字母国家代码",
    "original_name": "用户原始输入的物种名部分"
}}

国家代码示例：
- 中国 → CN
- 美国 → US
- 日本 → JP
- 韩国 → KR
- 英国 → GB
- 印度 → IN
- 澳大利亚 → AU

如果用户没有明确指定国家，默认使用 CN（中国）。"""


def get_analysis_prompt(species: str, country: str,
                         gbif_total: int, gbif_recent: int,
                         inat_total: int, inat_locations: str,
                         inat_descriptions: str,
                         risk_level: str, risk_reason: str,
                         iucn_data: dict = None) -> str:
    """生态学预警分析（含IUCN交叉验证）"""

    # 构建IUCN数据段落
    iucn_section = ""
    if iucn_data and iucn_data.get("found"):
        iucn_section = f"""
【IUCN全球保护评估】
- 保护等级：{iucn_data.get('category', '未知')}（LC=无危, NT=近危, VU=易危, EN=濒危, CR=极危, EW=野外灭绝）
- 种群趋势：{iucn_data.get('population_trend', '未知')}
- 已知威胁：{', '.join(iucn_data.get('threats', [])) if iucn_data.get('threats') else '无记录'}
"""
    elif iucn_data and not iucn_data.get("found"):
        iucn_section = """
【IUCN全球保护评估】
- 该物种未被IUCN红色名录收录
"""

    return f"""你是一位入侵生态学专家。以下是一个入侵物种潜在扩散的早期预警数据，请进行专业分析。

【物种】{species}
【目标区域代码】{country}

【GBIF官方数据】
- 全部历史记录：{gbif_total} 条
- 近3年记录：{gbif_recent} 条

【iNaturalist公民科学数据】
- 近3年观察记录：{inat_total} 条
- 观察地点样本：
{inat_locations if inat_locations else "（无地点数据）"}

- 观察描述样本：
{inat_descriptions if inat_descriptions else "（无文字描述）"}
{iucn_section}
【风险评估】
- 等级：{risk_level}
- 判断依据：{risk_reason}

请从以下角度进行简练分析（总字数控制在400字以内）：

1. **数据解读**：GBIF与iNaturalist的数据差异意味着什么？更可能是真实的入侵扩散信号，还是公民科学的数据采集偏差？
2. **交叉验证**：结合IUCN保护等级与种群趋势，该物种的入侵潜力如何？无危且种群稳定的物种在新区域出现，是否意味着更高的入侵风险？如果物种本身是濒危物种，是否应将关注点从"防控"转向"保护监测"？
3. **生态风险**：综合以上，该物种对当地生态系统可能造成什么影响？
4. **管理建议**：基于现有证据，你建议的下一步行动是什么？

请用中文输出。"""