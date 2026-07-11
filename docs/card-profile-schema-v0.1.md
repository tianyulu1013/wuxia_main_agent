# 卡牌画像格式 v0.1

目标：让 AI 助手在评审新卡时，不只做字段检索，而是有一层可读的“牌面理解笔记”。

原则：

- 牌面原文永远优先，画像只是辅助理解。
- 画像必须标明不确定处，不能把推测写成规则。
- 画像用于发现混淆、相关概念、电子化风险、评审关注点。

## 字段

- `title`：卡牌名。
- `source_ref`：数据库来源位置。
- `core_identity`：一句话描述这张卡在游戏中的核心定位。
- `mechanic_summary`：机制摘要，按主动、被动、身份、关系、资源、胜负条件等拆分。
- `keywords`：从牌面抽出的规则关键词。
- `risk_flags`：可能造成解释分歧、循环、跨规则破坏、人工裁定的点。
- `related_concepts`：这张卡会帮助我们理解的全局规则概念。
- `digitalization_notes`：未来电子化时需要建模或人工裁定的点。
- `open_questions`：需要作者裁定或未来规则库记录的问题。

## 示例结构

```json
{
  "title": "示例",
  "source_ref": "战斗人物!1",
  "core_identity": "一句话定位。",
  "mechanic_summary": {
    "active": [],
    "passive": [],
    "identity_or_special": [],
    "relationships": []
  },
  "keywords": [],
  "risk_flags": [],
  "related_concepts": [],
  "digitalization_notes": [],
  "open_questions": []
}
```
