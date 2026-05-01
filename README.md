**🛡️ InvasiveGuard** 

入侵物种早期预警Agent —— 基于 PEAS 框架，交叉比对 iNaturalist、GBIF 和 IUCN Red List 三个数据源，利用平台间的“信息差”发现潜在的入侵扩散信号。

生态学背景

入侵物种在新区域扩散后，官方调查往往滞后 2-3 年才能正式记录。研究证明，iNaturalist 等平台有一半情况比科学文献更早发现新入侵物种。2018 年，多伦多有人在 iNaturalist 上传了一张黄杨木蛾照片，成为该物种在整个北美大陆的首次记录。

本项目自动化监测 iNaturalist 与 GBIF 之间的信息差，结合 IUCN Red List 保护等级进行交叉验证，区分“入侵威胁”与“保护机遇”，并支持每日自动扫描濒危物种（EN/CR/EW）的新观察记录。

PEAS 框架
要素	说明
Performance	正确识别 iNaturalist 与 GBIF 之间的数据差异，判断入侵风险等级
Environment	iNaturalist API、GBIF API、IUCN Red List（本地 CSV）、大模型 API
Sensors	iNaturalist API / GBIF API / IUCN 本地 CSV
Actuators	规则引擎（风险判定）/ 大模型（生态学解读）/ 邮件模块（每日报告）

系统架构
invasive_guard/
├── main.py
├── daily_monitor.py
├── config.py
├── prompts.py
├── .env
├── requirements.txt
├── iucn_threatened_species.csv
├── README.md
└── tools/
    ├── __init__.py
    ├── input_parser.py
    ├── inaturalist.py
    ├── gbif.py
    ├── iucn.py
    ├── risk_engine.py
    ├── llm_analyzer.py
    └── email_notifier.py

功能模式
交互查询（main.py）

支持自然语言（小龙虾，中国）或精确输入（Procambarus clarkii, CN），Agent 自动解析为拉丁名和国家代码。

三级数据交叉验证：

Sensor	数据源	问题
Sensor 1	iNaturalist	是否有近期观察记录？
Sensor 2	GBIF	科学界是否已正式记录？
Sensor 3	IUCN Red List	全球保护等级是什么？

五级风险评估规则：

条件	等级
GBIF 无记录 + iNaturalist 有记录	🔴 高度预警
GBIF 有历史但近 3 年无记录 + iNaturalist 有记录	🟡 中度预警
iNaturalist > GBIF 近 3 年的 3 倍	🟡 中度预警
GBIF 数据充足 + iNaturalist 在合理范围	🟢 正常
数据模式不明确	🔵 需关注

触发预警后，大模型从四个维度进行生态学分析：数据解读、IUCN 交叉验证、生态风险评估、管理建议。

每日自动监测（daily_monitor.py）

从 IUCN Red List CSV 中加载所有 EN/CR/EW 等级物种，逐一查询 iNaturalist 近期新观察，如发现则生成 HTML 邮件报告并通过 Gmail 发送。支持 crontab 定时运行。

快速开始

克隆项目并进入目录：
cd ~/invasive_guard
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

配置 .env 文件：
API_KEY=你的大模型API密钥
EMAIL_SENDER=你的Gmail地址@gmail.com
EMAIL_PASSWORD=你的Gmail应用专用密码
EMAIL_RECEIVER=接收报告的邮箱

将 IUCN Red List 受威胁物种名录 CSV（含 scientific_name 和 category 列）放于项目根目录，命名为 iucn_threatened_species.csv。

运行：
python main.py           # 交互查询
python daily_monitor.py  # 每日监测

数据来源
数据源	说明	访问
iNaturalist	全球自然观察社区	免费 API
GBIF	全球生物多样性信息网络	免费 API
IUCN Red List	濒危物种红色名录	本地 CSV
DeepSeek	大模型生态学分析	API Key

技术栈
Python 3.10+ / DeepSeek API / requests / python-dotenv / smtplib

引用
IUCN 2025. IUCN Red List of Threatened Species. Version 2025-2
iNaturalist. https://www.inaturalist.org
GBIF. https://www.gbif.org
