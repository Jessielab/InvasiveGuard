# Agent推理引擎：基于规则的风险评估

import config


def assess(inat_count: int, gbif_total: int, gbif_recent: int) -> dict:
    """
    基于预定义规则评估入侵风险等级
    返回: {"level": 风险等级, "code": 等级代码, "reason": 判断依据}
    """
    if inat_count == 0:
        return {
            "level": "无法评估",
            "code": "NODATA",
            "reason": "iNaturalist上无近年观察记录，缺少判断依据"
        }

    # 规则1: GBIF完全空白
    if gbif_total == 0 and inat_count >= 1:
        return {
            "level": "🔴 高度预警",
            "code": "HIGH",
            "reason": f"GBIF在该区域无任何正式记录，但iNaturalist有{inat_count}条近年观察。"
                       f"极可能为新入侵或未被正式记录的分布区。"
        }

    # 规则2: GBIF有历史但近3年空白
    if gbif_recent == 0 and gbif_total > 0:
        return {
            "level": "🟡 中度预警",
            "code": "MEDIUM",
            "reason": f"GBIF有{gbif_total}条历史记录但近3年无新记录，"
                       f"iNaturalist却有{inat_count}条近年观察。可能种群重新活跃或扩散至新区域。"
        }

    # 规则3: 公民科学远超官方
    if gbif_recent > 0 and inat_count > gbif_recent * config.HIGH_RISK_RATIO:
        return {
            "level": "🟡 中度预警",
            "code": "MEDIUM",
            "reason": f"iNaturalist近年记录({inat_count})远超GBIF正式记录({gbif_recent})，"
                       f"公民科学活跃度显著高于官方采集频率，存在数据滞后可能。"
        }

    # 规则4: 正常
    if gbif_recent > config.NORMAL_GBIF_MIN and inat_count < gbif_recent * config.NORMAL_INAT_RATIO:
        return {
            "level": "🟢 正常",
            "code": "NORMAL",
            "reason": f"GBIF近年有{gbif_recent}条正式记录，数据充足。"
                       f"iNaturalist补充记录{inat_count}条，属已知分布的常规观察。"
        }

    # 规则5: 模糊地带
    return {
        "level": "🔵 需关注",
        "code": "WATCH",
        "reason": f"数据模式不明确。GBIF近年记录{gbif_recent}条，"
                   f"iNaturalist近年记录{inat_count}条。建议持续观察。"
    }