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

这两份文件是默认游戏流程与基础战斗的最小常驻核心。`docs/rulebook-confirmed-rulings.md`不再作为每次整份必读入口。

## 2. 卡牌类别路由

只读取当前卡牌对应的一个类别模块：

- 战斗人物：`docs/ai-understanding/evaluation/card-types/combat-character.md`
- 附加人物：`docs/ai-understanding/evaluation/card-types/attached-character.md`
- 物品：`docs/ai-understanding/evaluation/card-types/item.md`
- 称号：`docs/ai-understanding/evaluation/card-types/title.md`
- 场景：`docs/ai-understanding/evaluation/card-types/scene.md`

只有战斗人物竞争两张人物名额。附加人物、物品和称号摸到后直接进入本局；场景定义整局环境，不做普通强度评分。

## 3. 战斗人物功能路由

只有战斗人物继续读取`docs/ai-understanding/evaluation/functions/README.md`，判断主要功能和次要功能，再加载相关的小模块。

主要功能决定评价权重和横向案例。不得用正面输出直接判定辅助型、调度型或全局影响型人物的整卡强弱。

## 4. 专项规则、术语与案例

- 根据牌面关键词，通过`docs/ai-understanding/rules/README.md`只读取实际涉及的局部规则。
- `data/review/rule_terms.json`只在牌面出现特殊术语时定向查询对应条目。基础战斗、评价方法和具体人物计算不属于术语。
- `docs/ai-understanding/cases/`只加载同类别、同主要功能、同关键机制的少量案例。
- 本卡作者裁定和理解读取`data/review/card_understanding_notes.json`及对应单卡笔记。
- 玩家意愿和桌面心理读取`data/review/player_dynamics.json`，但不能当作自动规则。

禁止为了保险读取完整规则书、全部术语、全部案例或全部历史评审。

## 5. 新裁定归档

作者纠正后按内容归档：

- 普遍游戏流程或结算：核心规则或专项规则模块。
- 特殊词语的精确定义：术语层。
- 如何评价某类卡或某项功能：评价模块。
- 某张卡的完整推导：案例库与单卡理解。
- 玩家选择和桌面心理：玩家动态。

不得把所有作者反馈一律写入术语层。

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
