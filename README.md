<div align="center">
  <img src="https://img.shields.io/badge/status-active-success?style=flat-square" alt="Status" />
  <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="License" />
  <img src="https://img.shields.io/badge/python-3.10+-blue?style=flat-square" alt="Python" />
</div>

<br />

# 🛡️ InvasiveGuard

**An AI-powered early-warning agent for invasive species detection** — leveraging the information gap between citizen science and official biodiversity records.

Built on the **PEAS** (Performance, Environment, Actuators, Sensors) framework, InvasiveGuard cross-references **iNaturalist**, **GBIF**, and the **IUCN Red List** to detect signals of biological invasion before they appear in formal scientific databases.

<br />

## 🌍 Why This Matters

When invasive species spread into new regions, official surveys often lag **2–3 years** behind ground truth. Research has shown that platforms like iNaturalist detect new invasions earlier than scientific literature in nearly **half** of all cases. 

> **Real-world example**: In 2018, a single iNaturalist observation of a box tree moth in Toronto became the **first record of this species in all of North America** — predating any official detection.

InvasiveGuard automates the detection of this **information gap**, enriches it with IUCN conservation status, and distinguishes between urgent invasion threats and conservation opportunities.

<br />

##  PEAS Framework

| Component | Description |
|-----------|-------------|
| **Performance** | Correctly identify data discrepancies between iNaturalist and GBIF; classify invasion risk level |
| **Environment** | iNaturalist API, GBIF API, IUCN Red List (local CSV), LLM API |
| **Sensors** | iNaturalist API · GBIF API · IUCN Red List (local lookup) |
| **Actuators** | Rule-based risk engine · LLM-powered ecological analysis · Email notification module |

<br />

##  Project Structure
```bash
invasive_guard/
├── main.py # Interactive mode entry point
├── daily_monitor.py # Scheduled daily monitoring
├── config.py # Global configuration constants
├── prompts.py # LLM prompt templates
├── .env # API keys & email credentials (excluded from git)
├── requirements.txt # Python dependencies
├── iucn_threatened_species.csv
├── README.md
└── tools/
├── init.py
├── input_parser.py # Natural language → structured query
├── inaturalist.py # iNaturalist sensor
├── gbif.py # GBIF sensor
├── iucn.py # IUCN Red List local lookup
├── risk_engine.py # Rule-based risk classifier
├── llm_analyzer.py # LLM-powered ecological analysis
└── email_notifier.py # HTML email report sender
```


<br />

##  Features

###  Interactive Query Mode (`main.py`)

Supports both **natural language** (*e.g.*, `小龙虾，中国`) and **precise scientific input** (*e.g.*, `Procambarus clarkii, CN`). The agent automatically resolves common names to Latin binomials and country names to ISO codes via an LLM translation layer.

**Three-tier cross-validation:**

| Sensor | Source | Question Answered |
|--------|--------|-------------------|
| Sensor 1 | iNaturalist | Any recent public observations? |
| Sensor 2 | GBIF | Formally recorded in scientific databases? |
| Sensor 3 | IUCN Red List | What is the global conservation status? |

**Five-level risk classification:**

| Condition | Level |
|-----------|-------|
| GBIF zero + iNaturalist non-zero | 🔴 High Alert |
| GBIF has history but zero in recent 3 years + iNaturalist non-zero | 🟡 Medium Alert |
| iNaturalist > 3× GBIF recent 3-year records | 🟡 Medium Alert |
| GBIF data sufficient + iNaturalist within expected range | 🟢 Normal |
| Data pattern unclear | 🔵 Watch |

When an alert triggers, the LLM analyzes across four dimensions: **data interpretation**, **IUCN cross-validation**, **ecological risk assessment**, and **management recommendations**.

### 📬 Automated Daily Monitoring (`daily_monitor.py`)

1. Loads all species listed as **EN**, **CR**, or **EW** from the local IUCN Red List CSV
2. Queries iNaturalist for recent observations of each species
3. If new sightings are found, generates and sends an **HTML email report** via Gmail SMTP
4. Designed for **cron-based scheduling** (*e.g.*, daily at 08:00)




## Quick Start

Clone and enter the project:

```bash
cd InvasiveGuard
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
pip install -r requirements.txt
Configure .env:
```
text
API_KEY=your_llm_api_key
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_RECEIVER=recipient@example.com

Place IUCN data: Download the IUCN Red List threatened species CSV (must contain scientific_name and category columns) and save as iucn_threatened_species.csv in the project root.

Run:
```bash

python main.py           # Interactive query mode
python daily_monitor.py  # Automated daily monitoring
```

## Data Sources

| Source | Description | Access |
|--------|-------------|--------|
| [iNaturalist](https://www.inaturalist.org) | Global community of nature observers | Free API, no key required |
| [GBIF](https://www.gbif.org) | Global Biodiversity Information Facility | Free API, no key required |
| [IUCN Red List](https://www.iucnredlist.org) | World's most comprehensive conservation status database | Local CSV file |
| [DeepSeek](https://platform.deepseek.com) | Large language model for ecological reasoning | API key required |

## Tech Stack

`Python 3.10+` · `DeepSeek API` · `requests` · `python-dotenv` · `smtplib` · `PEAS Agent Architecture`

## Citation

If you use the data sources referenced by this project, please cite:

> IUCN 2025. *IUCN Red List of Threatened Species*. Version 2025-2. https://www.iucnredlist.org

> iNaturalist. Available from https://www.inaturalist.org

> GBIF: Global Biodiversity Information Facility. https://www.gbif.org

<br />

<div align="center">
  <sub>Built for a Modern Ecology course project · May 2026</sub>
</div>






<div align="center">
  <img src="https://img.shields.io/badge/状态-活跃-success?style=flat-square" alt="Status" />
  <img src="https://img.shields.io/badge/许可-MIT-blue?style=flat-square" alt="License" />
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python" />
</div>

<br />

# 🛡️ InvasiveGuard

**AI 驱动的入侵物种早期预警智能体** —— 利用公民科学与官方生物多样性记录之间的信息差，在入侵扩散被正式记载之前发出预警。

基于 **PEAS**（Performance, Environment, Actuators, Sensors）框架构建，InvasiveGuard 交叉比对 **iNaturalist**、**GBIF** 和 **IUCN 红色名录** 三个数据源，捕捉潜在入侵信号。

<br />

## 🌍 背景

入侵物种向新区域扩散后，官方调查往往滞后 **2–3 年**才形成正式记录。研究表明，iNaturalist 等平台有近**半数**情况比科学文献更早发现新入侵事件。

> **真实案例**：2018 年，一位多伦多居民在 iNaturalist 上传了一张黄杨木蛾照片，这竟成了该物种在**整个北美大陆**的首次记录——比任何官方调查都早。

InvasiveGuard 自动捕捉这一信息差，结合 IUCN 保护等级进行交叉验证，区分"入侵威胁"与"保护机遇"，并支持每日自动扫描濒危物种的新增观察记录。

<br />

##  PEAS 框架

| 要素 | 说明 |
|------|------|
| **Performance** | 准确识别 iNaturalist 与 GBIF 之间的数据差异，判定入侵风险等级 |
| **Environment** | iNaturalist API · GBIF API · IUCN 红色名录（本地 CSV）· 大模型 API |
| **Sensors** | iNaturalist API · GBIF API · IUCN 本地查询 |
| **Actuators** | 规则引擎（风险判定）· 大模型（生态学解读）· 邮件模块（每日报告推送） |

<br />

##  项目结构
```bash
invasive_guard/
├── main.py # 交互模式入口
├── daily_monitor.py # 定时监测任务
├── config.py # 全局配置常量
├── prompts.py # 大模型提示词模板
├── .env # API 密钥与邮箱配置（不纳入版本控制）
├── requirements.txt # Python 依赖
├── iucn_threatened_species.csv
├── README.md
└── tools/
├── init.py
├── input_parser.py # 自然语言 → 结构化查询
├── inaturalist.py # iNaturalist 传感器
├── gbif.py # GBIF 传感器
├── iucn.py # IUCN 红色名录本地查询
├── risk_engine.py # 规则引擎（风险分级）
├── llm_analyzer.py # 大模型生态学分析
└── email_notifier.py # HTML 邮件报告发送
```


<br />

##  功能

### 交互查询模式（`main.py`）

支持**自然语言输入**（如"小龙虾，中国"）和**精确学名输入**（如 `Procambarus clarkii, CN`）。Agent 通过大模型翻译层自动将俗名转换为拉丁学名，将国家名转换为 ISO 代码。

**三级数据交叉验证：**

| 传感器 | 数据源 | 回答的问题 |
|--------|--------|-----------|
| Sensor 1 | iNaturalist | 近期是否有公开观察记录？ |
| Sensor 2 | GBIF | 科学数据库是否已正式收录？ |
| Sensor 3 | IUCN 红色名录 | 该物种全球保护等级是什么？ |

**五级风险分类：**

| 判定条件 | 风险等级 |
|----------|----------|
| GBIF 零记录 + iNaturalist 非零 | 🔴 高度预警 |
| GBIF 有历史记录但近 3 年为零 + iNaturalist 有记录 | 🟡 中度预警 |
| iNaturalist 记录数 > GBIF 近 3 年的 3 倍 | 🟡 中度预警 |
| GBIF 数据充足 + iNaturalist 在合理区间 | 🟢 正常 |
| 数据模式不明确 | 🔵 需关注 |

触发预警后，大模型从四个维度输出生态学分析：**数据解读**、**IUCN 交叉验证**、**生态风险评估**、**管理建议**。

###  每日自动监测（`daily_monitor.py`）

1. 从本地 IUCN 红色名录 CSV 中加载所有 **EN**、**CR**、**EW** 等级物种
2. 逐一查询 iNaturalist，检查是否有近期新增观察记录
3. 如发现新记录，生成 **HTML 邮件报告**，通过 Gmail SMTP 发送
4. 支持 crontab 定时调度（如每天早上 8 点自动运行）

<br />

##  快速开始

进入项目目录并创建虚拟环境：

```bash
cd InvasiveGuard
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

配置 .env 文件：
```bash
API_KEY=你的大模型API密钥
EMAIL_SENDER=你的邮箱@gmail.com
EMAIL_PASSWORD=你的Gmail应用专用密码
EMAIL_RECEIVER=接收报告的邮箱地址
```
放置 IUCN 数据：将 IUCN 红色名录受威胁物种 CSV 文件（需包含 scientific_name 和 category 两列）放在项目根目录，命名为 iucn_threatened_species.csv。

运行：
```bash
python main.py           # 交互查询模式
python daily_monitor.py  # 每日自动监测
```

##  数据源

| 数据源 | 说明 | 获取方式 |
|--------|------|----------|
| [iNaturalist](https://www.inaturalist.org) | 全球自然观察社区 | 免费 API，无需密钥 |
| [GBIF](https://www.gbif.org) | 全球生物多样性信息网络 | 免费 API，无需密钥 |
| [IUCN 红色名录](https://www.iucnredlist.org) | 全球最权威的物种保护状态数据库 | 本地 CSV 文件 |
| [DeepSeek](https://platform.deepseek.com) | 大语言模型，提供生态学推理 | 需 API Key |

## 技术栈

`Python 3.10+` · `DeepSeek API` · `requests` · `python-dotenv` · `smtplib` · `PEAS Agent Architecture`

## 引用

如需引用本项目所使用的公开数据，请按以下格式注明：

> IUCN 2025. *IUCN Red List of Threatened Species*. Version 2025-2. https://www.iucnredlist.org

> iNaturalist. Available from https://www.inaturalist.org

> GBIF: Global Biodiversity Information Facility. https://www.gbif.org

