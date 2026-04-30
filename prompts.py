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
                         risk_level: str, risk_reason: str) -> str:
    """生态学预警分析"""
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

【风险评估】
- 等级：{risk_level}
- 判断依据：{risk_reason}

请从以下三个角度进行简练分析（总字数控制在300字以内）：

1. **数据解读**：GBIF与iNaturalist的数据差异意味着什么？更可能是真实的入侵扩散信号，还是公民科学的数据采集偏差？
2. **生态风险**：如果该物种确实在扩散，参考其已知的生态习性，可能对当地生态系统造成什么影响？
3. **管理建议**：基于现有证据，你建议的下一步行动是什么？

请用中文输出。"""