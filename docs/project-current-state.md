# 项目当前状态

新对话优先阅读根目录的 `PROJECT_STATE.md`。本文是更详细的当前状态补充。

本文记录当前工具已经形成的稳定起点。

## 当前目标

本项目暂时不是电脑游戏，也不是完整规则引擎。

当前目标是：

- 整理五行卡牌的源数据。
- 提供本地查询网页。
- 支持多人一卡、字段级搜索、卡面查看。
- 建立不污染源数据的评语层和改卡候选层。

## 数据层

### 源数据层

- `data/cards.sqlite`
- `data/cards_current/*.jsonl`
- Excel 导入和更新日志同步生成的数据

这层表示当前卡牌事实。AI 评语、强度判断、电子化推测不得写入这一层。

### 覆盖层

- `data/card_unit_overrides.json`
- `data/author_ability_overrides.json`

用于记录作者已经裁定的结构化事实，例如多人一卡 unit、特技所属、共享生命等。

### 评语层

- `data/card_reviews.json`

用于记录作者裁定、AI 评语、强度、定位、设计风险、电子化风险、攻略。它不是牌面事实。

### 改卡候选层

- `data/change_candidates.json`

用于记录尚未确认或已经确认的改卡候选。候选不等于已经改牌，必须经作者确认后才进入 PSD、Excel、数据库更新流程。

### 卡面资产层

- `data/release_images/cards/`

当前查询网页直接读取这里的单卡 PNG。以后 release 后，只要更新这里的单卡图，网页会自动读取新图。

## 查询网页

入口：

- `http://127.0.0.1:8765`

启动脚本：

- `scripts/serve_card_browser.py`

已支持：

- 卡名/全文查询
- 字段级查询：名称、身份/属性、兵器、出处、关系、特技文本
- 默认隐藏废弃卡
- 多人一卡 unit 展示
- 卡面 PNG 展示
- 评语/裁定展示
- 改卡候选展示

## 多人一卡状态

多人一卡第一轮已经整理完成。

原则：

- `共同特技` 只是显示分组，不是事实层 unit。
- 特技所属使用真实 unit 名单。
- 普通单人卡不需要显式 unit 配置。
- `五个人头` 按一个 unit 处理，但计人数为 5。

## 在线化状态

当前查询网页有两种形态。

### 本地动态版

它依赖 Python 后端读取 SQLite、JSON 和本地图片，因此不能直接把 `web/card_browser/` 上传到普通静态托管就完整运行。

已经提供静态导出脚本：

- `scripts/export_static_site.py`

运行后生成：

- `site_export/`

静态导出版会：

- 把 SQLite 查询结果导出成 JSON。
- 把卡面图片复制到静态目录。
- 前端只读取静态 JSON 和图片。
- 可以部署到 Netlify 等普通静态网站。

### 已建立的 Git 仓库

主工程仓库：

- `https://github.com/tianyulu1013/wuxia_main_agent`

静态发布仓库：

- `https://github.com/tianyulu1013/wuxia_static_publish`

本地静态发布仓库目录：

- `static_publish_repo/`

它是独立 Git 仓库，并被主工程 `.gitignore` 忽略。
