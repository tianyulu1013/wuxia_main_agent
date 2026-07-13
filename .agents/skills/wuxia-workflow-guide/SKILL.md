---
name: wuxia-workflow-guide
description: Global workflow guide and skill index for the 五行卡牌 project. Use this at the start of any conversation to understand the project workflows, data layers, and layout of other specialized skills.
---

# 五行卡牌全局工作流与技能索引 (Global Workflow Guide)

本技能为项目的“全局导航图”。每次新对话开启时，Agent 应首先加载此技能，以快速了解项目架构、核心数据层分布以及五个专业工作流（流）的调用指引，避免越权操作或混淆逻辑。

---

## 📂 项目核心架构与权威数据源

在处理任何请求前，请务必牢记以下数据层级划分，**严禁将 AI 的理解、分析、攻略写入源数据层**：

1.  **源数据层 (Source Data - 严禁污染)**：
    *   SQLite 数据库：[data/cards.sqlite](file:///d:/workspace/wuxia-card-agent/data/cards.sqlite)（当前线上及本地查询系统读取的最新数据）。
    *   JSONL 数据：[data/cards_current/](file:///d:/workspace/wuxia-card-agent/data/cards_current/) 下的结构化卡牌记录。
    *   Excel 表格：`outputs/2025-excel-sync-candidate/已制作_2025日志同步候选_PSD校准.xlsx`。
2.  **覆盖与裁定层 (Overrides - 记录作者明确决定)**：
    *   多人一卡、特技所属等纠偏：[data/card_unit_overrides.json](file:///d:/workspace/wuxia-card-agent/data/card_unit_overrides.json)。
    *   单字段修正：[data/card_field_overrides.json](file:///d:/workspace/wuxia-card-agent/data/card_field_overrides.json)。
    *   特技结构修正：[data/author_ability_overrides.json](file:///d:/workspace/wuxia-card-agent/data/author_ability_overrides.json)。
3.  **改卡候选层 (Change Candidates - 临时存放未确认设计)**：
    *   改卡候选 JSON：[data/change_candidates.json](file:///d:/workspace/wuxia-card-agent/data/change_candidates.json)。
4.  **评语与理解层 (Reviews & Notes - AI 攻略、分析与评语)**：
    *   AI 强度与定位评估：[data/card_reviews.json](file:///d:/workspace/wuxia-card-agent/data/card_reviews.json)。
    *   人类可读的单卡笔记：[data/review/card_notes/](file:///d:/workspace/wuxia-card-agent/data/review/card_notes/)。
    *   规则术语理解笔记：[data/review/rule_terms.json](file:///d:/workspace/wuxia-card-agent/data/review/rule_terms.json)。

---

## 🔄 五大核心工作流 (The Five Core Flows)

当收到用户的任务时，根据下表判定当前任务所属的“流”，并**主动加载对应的专属 Skill** 开启工作：

### 流 1：🗃️ 卡牌数据查阅流 (Query/Data Flow)
*   **适用场景**：用户想“查找某张卡牌的描述”、“统计某属性人数”、“查看某卡牌当前有什么裁定”。
*   **关联技能**：`wuxia-rule-understanding`
*   **工作指引**：
    *   优先通过 Python 脚本或 SQLite 语句查询本地 [data/cards.sqlite](file:///d:/workspace/wuxia-card-agent/data/cards.sqlite)。
    *   如果需要可视化调试或现场查阅，可以使用本地网页查询系统（本地入口：`http://127.0.0.1:8765`，通过运行 [Start-CardBrowser.cmd](file:///d:/workspace/wuxia-card-agent/Start-CardBrowser.cmd) 一键启动）。
    *   对于多人一卡、特技归属的查询，阅读 [docs/skills/wuxia-multi-unit.md](file:///d:/workspace/wuxia-card-agent/docs/skills/wuxia-multi-unit.md)。

### 流 2：📝 卡牌修改与候选迭代流 (Card Change/Candidate Flow)
*   **适用场景**：用户提出“修改某张卡的属性/技能数值”、“设计一张新卡”、“评估某个修改想法”。
*   **关联技能**：`wuxia-card-change-flow` (必须立即加载)
*   **工作指引**：
    *   **步骤**：分类请求 -> 查阅当前卡牌 -> 撰写 4 维度简评 (形象/强度/规则/清晰度) -> 给定 AI 态度 (support/caution/oppose) -> 生成候选文本与更新日志草稿 -> 写入候选层。
    *   **落地条件**：使用 [scripts/add_change_candidate.py](file:///d:/workspace/wuxia-card-agent/scripts/add_change_candidate.py) 将想法记录到 `change_candidates.json`。**在未获得作者明确口头确认前，绝对禁止修改任何源数据库、Excel 或 PSD 文件！**

### 流 3：🛡️ 卡牌强度评审与审计标定流 (Card Review/Calibration Flow)
*   **适用场景**：用户要求“给新一批卡做强度评估”、“写单卡攻略/定位”、“补充电子化风险评估”。
*   **关联技能**：`wuxia-card-review-calibration` (必须立即加载)
*   **工作指引**：
    *   **单卡原子审核**：评审以单卡为唯一推理和验收单位，禁止批量模板化生成评审。
    *   **客观物理精算**：分析“正面生存”与“侧面生存”分值（参照张三丰、无情等天花板卡牌），在“时序”（Turn/Round/抢先结算）与“穿透”维度下精算输出爆发。
    *   **严禁脑补网游词汇**（如坦克、后排输出），必须使用标准的桌游物理概念（首发人物、不利转移等）。
    *   **模块完整性**：评审报告必须完整且无一遗漏地包含正面生存、侧面生存、优点、缺点、规则风险和电子化风险。

### 流 4：🚀 版本发布与同步流 (Release/Publish Flow)
*   **适用场景**：用户要求“把现在的稳定版发给别人”、“上传 Git”、“部署上线”。
*   **关联技能**：`wuxia-release-flow` (必须立即加载)
*   **工作指引**：
    *   **绝对红线：未经作者明确授权和明确的推送指令，AI 绝对禁止在主仓库或静态发布仓库执行任何 git commit 或 git push 推送动作。**
    *   **版本控制**：区分“本地修复”与“正式发布”。临时 UI Bug 修复或缓存刷新不要修改公开的版本号（`library_version` / `site_version`）。
    *   **部署步骤**：确定要发布时，运行 [scripts/export_static_site.py](file:///d:/workspace/wuxia-card-agent/scripts/export_static_site.py) 导出纯静态站至 `site_export/`，再同步至静态发布仓库。

### 流 5：📖 底层规则与术语重构流 (Rulebook & Terminology Flow)
*   **适用场景**：用户想“整理游戏规则”、“解决技能之间的规则冲突”、“查阅某个生僻机制”。
*   **关联技能**：`wuxia-rule-understanding` (必须立即加载)
*   **工作指引**：
    *   **规则分级检索**：遵循 Lv1 核心骨架 ([rulebook-confirmed-rulings.md](file:///d:/workspace/wuxia-card-agent/docs/rulebook-confirmed-rulings.md)) -> 局部正文 -> Lv3 FAQ 裁定层的分级按需读取原则，防止 Context 爆仓。
    *   **中英文术语转换**：在思索（Thinking）和代码逻辑中推荐使用规范英文术语（如 `Turn`, `Round`, `Active`, `Void` 等），但在最终面向玩家的卡牌描述、规则书正文输出时，**必须转换为纯中文表述，零英文单词**。

---

## ⚠️ 终极红线约束 (Zero-Tolerance Rules)

1.  **用户是唯一作者**：用户的口头裁定为项目最高准则。不理解规则时必须主动询问，禁止自行脑补或去外部游戏套用规则。
2.  **Git 推送限制**：在没有收到作者明确允许的指令前，不得进行任何 git commit 或 git push。
3.  **Windows UTF-8 编码安全**：在读写任何中文 JSON/Markdown 文本时，严格遵守 `wuxia-windows-utf8-safety` 技能规范，优先使用 Python 或 patch 方式读写，禁止使用 PowerShell `>` 或 `Set-Content` 等重定向管道命令以防文本损坏。
