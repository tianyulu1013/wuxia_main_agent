---
name: wuxia-rule-understanding
description: Guides the agent on how to retrieve and understand 五行卡牌 rules hierarchically to prevent context bloat, using English internally and Outputting Chinese.
---

# 五行卡牌规则按需理解

本技能要求先理解默认游戏流程，再按卡牌类别、战斗人物功能和实际机制逐层加载。规则、术语、评价方法、具体案例和玩家心理必须分层保存。

## 1. 最小常驻核心

处理设计、改卡或评价时，先完整读取：

- `docs/ai-understanding/core/game-flow.md`
- `docs/ai-understanding/core/combat-baseline.md`
- `docs/ai-understanding/parser-guide.md`

这三份文件是默认游戏流程、基础战斗及卡面翻译常识的最小常驻核心。AI 在评审卡牌时，**必须基于 `parser-guide.md` 的规范在评审报告中增设“模糊表述与修改建议”专项栏目**。`docs/rulebook-confirmed-rulings.md` 不再作为默认必读入口。

## 2. 卡牌类别与主要功能路由

1. **选择评估方法 (evaluation/)**：根据卡牌类别和功能，只读取一个专门的评估指南：
   * 正面比拼战斗人物：`docs/ai-understanding/evaluation/frontal-combat.md` (包含白人期望计算及王重阳案例锚点)。
   * 全局影响/场景人物：`docs/ai-understanding/evaluation/global-effects.md` (包含时空、结盟避让、规则改写评估)。
   * 辅助随从/物品/称号：`docs/ai-understanding/evaluation/support-and-items.md` (评估直接入局白嫖空间)。
2. **选择专项规则 (rules/)**：根据牌面关键词，通过 `docs/ai-understanding/rules/README.md` 路由，定向只读取发生关联的机制文件，**绝对禁止**加载整份规则书：
   * 出现 兵器/双持/博 等：读取 `docs/ai-understanding/rules/weapons.md`（多兵器互斥及复制虚拟持有规则）。
   * 出现 优先级/抢先/无法响应/嵌套 等：读取 `docs/ai-understanding/rules/resolution-priority.md`（12层特技优先级级联与嵌套禁止）。
   * 出现 冰狂混乱惊毒迟封等13种异常/解/转/出血 等：读取 `docs/ai-understanding/rules/status-effects.md`（三级异常判定与非异常结算）。
   * 出现 在场/不在场/找不到/无此人/破空 等：读取 `docs/ai-understanding/rules/space-states.md`（定位修饰与放逐空间）。

## 3. 术语与案例独立隔离

* **术语层只定名不写逻辑**：`data/review/rule_terms.json` 仅作为特殊词义的权威字词解释（用于前端高亮与词义检索），**禁止**在术语层记录庞杂的结算流程、期望计算或防脑补限制。
* **单卡案例锚点归档**：具体卡牌的完整数值推导、公式演算及不可迁移边界归于 `docs/ai-understanding/cases/`，不与通用规则混合。
* **作者裁定**：读取本卡的单独笔记 `data/review/card_notes/<卡名>.md` 或者是 `data/card_unit_overrides.json` 等级联卡牌。

## 4. 新反馈归档原则

当作者对卡牌或规则给出口头裁定/修正后，AI 必须严格按下述分类逻辑进行增量归档：
* 若属于基础流程或通用结算：更新 `rules/` 下对应的机制小文件。
* 若属于纯词条释义：更新术语字典 `rule_terms.json`。
* 若属于某项功能的打分准则：更新 `evaluation/` 下的评估方法小文件。
* 若属于具体某张卡的计算：更新 `cases/` 或单卡理解笔记。

禁止为了“省事”或“安全”将一切反馈无脑塞进术语表中，以维持整个规则树的立体与轻量。

## 6. 语言规范：内部英文推导，输出全中文规则

-   **内部推理与代码逻辑 (中 $\rightarrow$ 英)**：
    -   为了保证逻辑判断的严密性和变量命名的一致性，Agent 在写内部代码（如后端 SQL、前端 JS）、数据模型（JSON）和在思索（Thinking）中进行逻辑链推导时，**支持并推荐使用清晰的英文术语**进行命名和映射。
    -   标准术语映射表：
        -   回合 $\rightarrow$ `Turn`
        -   轮 $\rightarrow$ `Round`
        -   转轮 $\rightarrow$ `Cycle`
        -   在场 $\rightarrow$ `Active`
        -   不在场 $\rightarrow$ `Inactive`
        -   破空 $\rightarrow$ `Void`
        -   离场 $\rightarrow$ `Left`
        -   找不到 $\rightarrow$ `Untargetable`
        -   生命流失 $\rightarrow$ `LifeLoss`
        -   弃牌堆 $\rightarrow$ `DiscardPile`
        -   除外区 (本局弃卡) $\rightarrow$ `RemovedFromGame`
        -   人物单元 $\rightarrow$ `Unit`
        -   物理卡牌 $\rightarrow$ `Card`
-   **输出与规则重写 (英 $\rightarrow$ 中，零英文)**：
    -   当 Agent **输出最终的卡牌新文案、重新编译生成规则书或向用户回复文案时，必须保持纯粹的中文环境**。
    -   **禁忌**：禁止在最终规则书或卡牌描述中包含任何英文术语（如不能在特技描述里写 "Round 结束"、"Unit 死亡" 等，必须严格翻译为对应的 "轮结束"、"单元死亡"）。保证玩家最纯粹的武侠沉浸感。
