# 专项规则路由

核心流程和基础战斗之外的规则按关键词加载。不得整份读取全部专项规则。

## 当前路由

| 牌面内容 | 定向读取 |
|---|---|
| 攻击、伤害、受伤、减伤、反伤 | `attack-damage-and-injury.md` |
| 相关、不相关、派出、派遣、借出、召回 | `related-response-and-dispatch.md` |
| 未注明时点的回合中攻击或一击 | `default-late-timing.md` |
| 人物、卡、多人一卡、共同特技、计人数 | `docs/skills/wuxia-multi-unit.md`，以及 `docs/rulebook-refactored.md` 对应人物容器章节 |
| 伤害、生命流失、杀死、生命为0、复活 | `docs/rulebook-refactored.md` 的生命与防御相关章节 |
| 死亡、离场、不在场、找不到、破空、清除 | `docs/rulebook-refactored.md` 的时空、存在状态和死亡章节 |
| 回合、轮、转轮、战斗嵌套 | `docs/rulebook-refactored.md` 的时间和战斗章节 |
| 结盟、阵营、名次、围攻、玩家顺序 | `docs/rulebook-refactored.md` 的玩家、阵营和胜负章节 |
| 抢先、无法响应、不中、无效 | `docs/rulebook-refactored.md` 的结算顺序与优先级章节 |
| 学会、复制、模拟、完美学会等特殊词 | `data/review/rule_terms.json` 中对应术语，不读取全部术语 |
| 删字、改字、改数字、只剩某行 | `docs/rulebook-refactored.md` 的人工裁定与FAQ |

## 模块迁移原则

以后新增或校准某一专项规则时，应建立或更新本目录下对应的小文件，并将本表指向该文件。不要继续把所有裁定追加到 `docs/rulebook-confirmed-rulings.md`。

专项文件应只包含：

- 该机制的普遍规则。
- 已确认的边界。
- 触发关键词。
- 与其他模块的接口。

具体卡牌计算进入案例库；玩家选择进入玩家动态；特殊词义进入术语层。
