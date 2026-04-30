# 配置文件：集中管理所有常量

# API端点
INATURALIST_API = "https://api.inaturalist.org/v1/observations"
GBIF_SPECIES_API = "https://api.gbif.org/v1/species/match"
GBIF_OCCURRENCE_API = "https://api.gbif.org/v1/occurrence/search"
LLM_API = "https://api.deepseek.com/v1/chat/completions"
# IUCN API配置
IUCN_API = "https://api.iucnredlist.org/api/v4"
# 查询参数
YEARS_BACK = 3                    # iNaturalist回溯年数
INAT_PER_PAGE = 30                # iNaturalist每页结果数
INAT_DESC_SAMPLE = 10             # 保留的描述样本数

# 预警阈值
HIGH_RISK_RATIO = 3               # iNaturalist/GBIF比值超过此值视为异常
NORMAL_GBIF_MIN = 50              # GBIF近3年记录超过此值视为充足
NORMAL_INAT_RATIO = 0.5           # iNaturalist低于GBIF此比例视为正常

# 模型参数
LLM_MODEL = "deepseek-chat"
LLM_TEMPERATURE_PARSE = 0.1       # 解析阶段：低温度确保稳定
LLM_TEMPERATURE_ANALYSIS = 0.3    # 分析阶段：适度创造性
