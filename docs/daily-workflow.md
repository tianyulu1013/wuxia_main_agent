# 日常工作流

## 查卡

1. 启动本地查询服务。
2. 打开 `http://127.0.0.1:8765`。
3. 使用字段级搜索。

常用方式：

- 找身份为 `【恶】`：范围选 `身份/属性`。
- 找针对 `【恶】` 的效果：范围选 `特技文本`。
- 找出处：范围选 `出处`。
- 找兵器：范围选 `兵器`。

## 改卡与编辑卡牌流程

当前项目提供三种相互兼容的卡牌编辑与更新途径。不论采用哪种途径，源数据（JSONL 文件）均是最高事实来源，修改后必须编译重构 SQLite 数据库。

### 途径 A：Web 网页独立编辑器暂存流（推荐：作者自主、高容错、字段级 Diff）

最常用且安全的本地自主编辑流程，使用基于 Staging（暂存）的设计：

1. **启动服务与访问**：
   * 启动本地服务后，打开 `http://127.0.0.1:8765/editor.html` 进入管理后台。
2. **可视化编辑**：
   * 可修改生命、身份（使用大文本域，支持多行规则录入）、性别、兵器等字段。
   * 特技管理：点击 `➕ 添加特技` 增加新特技；使用每一行特技右侧的 `🔼 上移` / `🔽 下移` 按钮调整顺序；所有特技的改动会自动毫秒级同步编排到底部的“原始卡面描述（Concatenated Description）”文本框中。
3. **安全暂存（Staging）**：
   * 点击表单右上角 **“💾 暂存修改”**。此时改动**绝不污染**物理源数据和 SQLite 数据库。
   * 改动以 `status: "draft"` 的草稿记录存入 `data/change_candidates.json`，并在 **`data/review/pending_changes.md`** 中自动生成清晰的字段级 Diff 对比表格（高亮呈现 `📝 修改`、`🆕 新建`、`⚙️ 结构修改`）。
4. **人工与 AI 共同审核确认**：
   * 打开 AI 聊天窗口，与 AI 沟通：“*看一下我的暂存修改，帮我评估一下*”。
   * 确认无误后，由 AI 运行合流脚本：
     ```powershell
     python scripts/apply_pending_changes.py
     ```
     一次性将所有草稿批量合并进底层 JSONL 物理源文件，并自动热编译重建数据库。

---

### 途径 B：与 AI 直接讨论合并流（讨论协作流）

适合在规则设计阶段，与 AI 碰撞想法时的流向：

1. **自然语言提出**：作者在聊天窗口直接提出修改想法（例如：“*段正淳血量改到 2800 吧*” 或 “*萧峰的降龙十八掌输出需要削弱*”）。
2. **AI 分析与评估**：AI 进行规则稳定性、艺术形象、玩法强度的综合评估，起草候选文本。
3. **写入候选层**：AI 将修改建议写入 `data/change_candidates.json` 候选层，等待作者确定。
4. **口头确认与应用**：作者口头同意后，AI 自动修改对应的 JSONL 源文件，并重新编译重建 SQLite 数据库。

---

### 途径 C：手动修改 Excel 批量强刷流（Excel 回退流）

仅在需要进行极大规模字段重排、物理卡牌顺序整理等大体量操作时使用：

1. **编辑 Excel**：直接使用 WPS/Excel 打开 `outputs/2025-excel-sync-candidate/已制作_2025日志同步候选_PSD校准.xlsx`，手动改动或增加卡牌行的字段，修改必须保留 `卡牌ID` 列的物理 UUID。
2. **强制逆向导入**：在终端运行：
   ```powershell
   python scripts/build_card_database.py --import-excel
   ```
   脚本会强制读取 Excel 表格内容，逆向覆盖 JSONL 物理文件，并同步重建 SQLite 数据库。

---

## 记录评语或裁定

完整评审、强度、定位、电子化风险和攻略写入：

- `data/review/card_evaluations.json`
- `data/review/card_notes/<卡名>.md`

单卡理解进入`data/review/card_understanding_notes.json`。`data/card_reviews.json`仅作历史兼容，不再是新评审默认入口。这些内容不改牌面，不进入源数据库。

## 规则书修订与优化流程

当游戏机制出现歧义、冲突或需要补充底层概念时，遵循以下重构与修订流程：

1. **收集未决例外 / 口头裁定**：由 Agent 或作者在对话中指出哪些规则术语或段落存在冲突（例如：“找不到”与“波及”的相互关系）。
2. **商议与直接修正**：不委曲求全去“变通绕过”，而是采取“直接重构规则或修改卡牌本身”的方式，从底层把逻辑梳理干净自洽。
3. **分层记录确认内容**：普遍流程进入`docs/ai-understanding/core/`，局部机制进入专项规则，特殊词义进入术语层，评价方法进入类别/功能模块，具体人物计算进入案例和单卡理解，玩家意愿进入玩家动态。
4. **修订规则书（Markdown 源文件）**：根据最新的目录大纲，在 `docs/rulebook-refactored.md` 中进行对应的正文重构、细节说明与合并重写，确保内容无一遗漏。
5. **编译输出 docx**：运行转换脚本，将最新的 Markdown 规则书重新生成覆盖为 `五行卡牌规则.docx`。

## Release 后更新卡面

卡面更新流程已经固化在：

- `.agents/skills/wuxia-release-flow/SKILL.md`
- `.agents/skills/wuxia-release-flow/references/card-image-release.md`

作者交付 TTS 用的 10×7、共 70 张卡的牌堆大图后：

1. 根据实际更新日志或已回录批次确定需要替换的卡、牌堆和槽位。
2. 在覆盖当前图片前，将修改卡的旧版 WebP 和完整旧卡数据冻结到历史层。
3. 归档并索引新版牌堆大图。
4. 只切出更新记录涉及的槽位，写入当前单卡 PNG 母版。
5. 生成 550×900、质量 85 的当前 WebP，并更新图片清单。
6. 核对旧版页面使用历史图、当前页面使用新版图，最后汇总本次受影响牌堆。

当前网页优先读取 `data/release_images/cards_webp/`，`data/release_images/cards/` 中的 PNG 是当前单卡母版和兼容回退。没有用户明确发布指令时，只做本地更新和验证。

## 发布静态快照

运行：

```powershell
& "C:\Users\biaaa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts/export_static_site.py
```

生成：

- `site_export/`

这个目录是纯静态网站，可以拖到 Netlify，或同步到单独的静态发布 Git 仓库。

## 版本管理

当前 Git 快照应该保存：

- `scripts/`
- `web/`
- `docs/`
- `data/*.json`
- `data/*.sqlite`
- `data/cards_current/*.jsonl`

不建议普通 Git 直接保存：

- PSD
- 70 张 release 大图
- `node_modules`
- 临时输出

这些大文件以后如需版本化，建议单独归档或使用 Git LFS。

---

## 卡牌评审流程

卡牌评审只有一套有效流程：

- 规范：`docs/skills/wuxia-card-calibration-sop.md`
- 单卡工作卡：`docs/skills/wuxia-card-review-workcard.md`
- 校准技能：`.agents/skills/wuxia-card-review-calibration/SKILL.md`
- AI理解入口：`docs/ai-understanding/README.md`

强制要求：

1. 一张卡是唯一推理和验收单位；10张仅是最终汇编单位。
2. 当前卡未通过完整语义验收，不得开始下一张。
3. 单卡工作卡的栏目必须逐项独立填写，禁止合并栏目、用综合段落替代或缩写成摘要。
4. 禁止用脚本、关键词、模板或批量生成器自动产生评审正文、分数、优缺点、玩法、问题或`locked`状态。
5. 脚本只可用于只读提取牌面、检索规则、核对作者裁定、检查编码和检查栏目完整性。
6. 规则不明时先查规则书、术语层、作者裁定和玩家动态；仍不能回答且会改变结论时，才列为待校准问题。
7. 作者校准必须逐条原样保留。任何自动化过程不得覆盖、清空、摘要替代或降级作者裁定。
8. 只有源数据层需要作者明确确认后才能修改；评审工作写入评语/理解层，但仍不得伪造作者裁定。
9. 在卡牌评审数据库的 `full_text` 字段、单卡 Markdown 人类可读笔记 `data/review/card_notes/<卡名>.md`、以及最终的批次评审报告中，必须完整且无一遗漏地包含**正面生存**、**侧面生存**、**优点**、**缺点**、**规则风险**和**电子化风险**等核心评估模块，严禁合并、简化或遗漏。
