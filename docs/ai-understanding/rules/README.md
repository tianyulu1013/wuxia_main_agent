# 专项规则路由

核心流程和基础战斗之外的规则按关键词加载。不得整份读取全部专项规则。

## 当前路由

| 牌面内容 | 定向读取 |
|---|---|
| 兵器、武器、刀、剑、拳掌、双持、博 | `weapons.md` |
| 结算顺序、优先级、抢先、无法响应、嵌套 | `resolution-priority.md` |
| 冰、狂、混、乱、毒、麻、迟、点、惊、封、禁咒、异常、不利、移除不利、解、转、出血 | `status-effects.md` |
| 在场、不在场、破空、找不到、无此人 | `space-states.md` |
| 结盟、阵营、本方、敌方、队友、从属、称号关系 | `alliance-faction.md` |
| 攻击、伤害、受伤、减伤、反伤 | `attack-damage-and-injury.md` |
| 无敌、不中、防御状态何时生效 | `defensive-states.md` |
| 相关、不相关、派出、派遣、借出、召回 | `related-response-and-dispatch.md` |
| 未注明时点的回合中攻击或一击 | `default-late-timing.md` |
| 学会、复制、模拟、完美学会等特殊词 | 定向查询 `data/review/rule_terms.json` 中对应术语，不读取全部术语 |

## 模块迁移原则

以后新增或校准某一专项规则时，应建立或更新本目录下对应的小文件，并将本表指向该文件。不要继续把所有裁定追加到 `docs/rulebook-confirmed-rulings.md`。

专项文件应只包含：

- 该机制的普遍规则。
- 已确认的边界。
- 触发关键词。
- 与其他模块的接口。

具体卡牌计算进入案例库；玩家选择进入玩家动态；特殊词义进入术语层。
