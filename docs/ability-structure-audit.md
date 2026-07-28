# 特技结构审计报告

本报告来自当前数据库的 `description` 字段自动解析。它不会替代作者裁定，只用于把疑似结构问题集中列出来。

- 导入时间 UTC：`2026-07-27T15:41:34.266110+00:00`
- 卡牌数：541
- 抽取特技/说明块数：1988
- 结构化特技表：`data/cards.sqlite` / `card_abilities`
- JSONL：`data/cards_current/abilities.jsonl`

## 类型统计

- `字`: 543
- `招式`: 450
- `*`: 322
- `技能`: 200
- `武功`: 198
- `说明`: 140
- `内功`: 132
- `符卡`: 3

## 审计标记统计

- `implicit_word`: 531
- `inherited_kind`: 343
- `inherited_named_ability`: 339
- `exclusive_word`: 254
- `free_text`: 148
- `author_corrected`: 117
- `missing_indent_for_inherited`: 114
- `unit_specific_ability`: 104
- `nested_continuation_line`: 61
- `author_confirmed_structure`: 14
- `continuation_line`: 10
- `nested_named_line`: 7
- `nested_indented_line`: 5
- `known_unnamed_ability`: 5
- `unnamed_star_line`: 5
- `nested_named_line_without_indent`: 3
- `indented_implicit_word`: 1

## 无前缀但继承上一类型的特技

- 数量：339

### 风四娘 / 战斗人物!4:2

- 当前判断：`技能` / 名称：`爬最高的山`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：爬最高的山：场上人物一旦出场就不可换人

### 白飞飞 / 战斗人物!12:3

- 当前判断：`武功` / 名称：`无影鬼羽`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：无影鬼羽：可令全-100/回合，此攻击如果造成伤害，则敌不知

### 燕十三 / 战斗人物!15:2

- 当前判断：`招式` / 名称：`第十四剑`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：第十四剑：金- 100全狂 混克可放，放出后所有剑法混克可放（剑）

### 燕十三 / 战斗人物!15:3

- 当前判断：`招式` / 名称：`第十五剑`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：第十五剑：-- 敌死亡 放出后无法被响应更改；燕十三释放则为自杀于敌前（剑）

### 俞佩玉 / 战斗人物!28:2

- 当前判断：`武功` / 名称：`先天无极`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：先天无极：可以将任何一张卡的攻击力挪至另一张卡上

### 花满楼 / 战斗人物!31:2

- 当前判断：`招式` / 名称：`流云飞袖`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：流云飞袖：对阵双方所放卡不可改变

### 花满楼 / 战斗人物!31:3

- 当前判断：`招式` / 名称：`听风辨位`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：听风辨位：听出他人身份及招式卡

### 司空摘星 / 战斗人物!36:2

- 当前判断：`技能` / 名称：`偷王之王`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：偷王之王：随时可获取某人可见的一（特技，物品，基础卡），成功率起始各为（2/3，1，1），用一次降低1/6；对同一人物最多只拥有其一特技，对同一个人物多次使用需要多个身份；可还回

### 花无缺 / 战斗人物!41:2

- 当前判断：`内功` / 名称：`移花接玉`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：移花接玉：可反射不高于300的伤害

### 魏无牙 / 战斗人物!46:2

- 当前判断：`技能` / 名称：`机关学`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：机关学：只承受未攻击加成的基础对阵伤害，禁对阵动卡

### 魏无牙 / 战斗人物!46:3

- 当前判断：`技能` / 名称：`车子`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：车子：-500/回合（随机一敌）

### 魏无牙 / 战斗人物!46:4

- 当前判断：`技能` / 名称：`子鼠`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：子鼠：全过一轮，每人掷骰考验，未过2者生命减半，自+300以及他人总减血量（可用两次）

### 方宝玉 / 战斗人物!52:3

- 当前判断：`技能` / 名称：`浑身上下都是破绽`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：浑身上下都是破绽：回合中己可空门大开，则交手敌亦不敢放卡及对己使用非被动特技，对于不会武功者及疯子无效

### 紫衣侯 / 战斗人物!53:2

- 当前判断：`招式` / 名称：`一百九十三家秘门剑法`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：一百九十三家秘门剑法：- 1930（剑）

### 千手书生 / 战斗人物!56:2

- 当前判断：`武功` / 名称：`万流归宗`
- 标记：`author_corrected, inherited_kind, inherited_named_ability, missing_indent_for_inherited, unit_specific_ability`
- 原文：万流归宗：接下大招且视为成功施放

### 檀明 / 战斗人物!57:2

- 当前判断：`招式` / 名称：`空手入白刃`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：空手入白刃：水金 100 如敌持有兵刃则可直接释放

### 檀明 / 战斗人物!57:3

- 当前判断：`招式` / 名称：`神鹤掌`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：神鹤掌：水火 100

### 飧毒大师 / 战斗人物!69:2

- 当前判断：`招式` / 名称：`噬魂`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：噬魂：金土 使一人此后攻击所有人，且能用的一定要用出

### 飧毒大师 / 战斗人物!69:4

- 当前判断：`技能` / 名称：`无影毒`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：无影毒：可令场上全中毒200（不累叠）

### 飧毒大师 / 战斗人物!69:5

- 当前判断：`技能` / 名称：`毒药精研`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：毒药精研：-- 毒伤害+200（累积上本）

### 铁中棠 / 战斗人物!70:3

- 当前判断：`招式` / 名称：`病维摩拳`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：病维摩拳：对阵中交手n人则可打断2n条特技（两两互断）

### 云铮 / 战斗人物!72:2

- 当前判断：`武功` / 名称：`常春`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：常春：一次行动中一击*4

### 雷大鹏 / 战斗人物!74:2

- 当前判断：`内功` / 名称：`雷鸣`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：雷鸣：木- -木 伤害等同于本回合造成的普通内功伤害 全

### 项少龙 / 战斗人物!94:2

- 当前判断：`招式` / 名称：`【墨子剑法补遗】`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：【墨子剑法补遗】：墨子剑法开启状态可使敌受其攻击需格挡，敌消耗500/次（剑）（此刻指例如某张基础卡比对时为平，及自身攻击引发敌响应反击时）

### 项少龙 / 战斗人物!94:3

- 当前判断：`招式` / 名称：`百战刀法`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：百战刀法：回合开始前选择使用，则直到下回合开始前攻+（此前墨子剑及杀招触发格挡数*200），再次使用时无需重新计算格挡数（刀）

### 范良极 / 战斗人物!104:2

- 当前判断：`招式` / 名称：`烟管点穴`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：烟管点穴：-火 点*2，此点不受到解的影响

### 范良极 / 战斗人物!104:3

- 当前判断：`招式` / 名称：`烟箭`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：烟箭：每回合令敌先-100且本回合对己的随机一击失效

### 单玉如 / 战斗人物!106:2

- 当前判断：`武功` / 名称：`翠袖环`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：翠袖环：双环各依照五行生克关系（一环为生，一环为克）在双方放卡结果中各自穿：选择一卡作为开始，不重复地选取与上一张相生/克的基础卡，直至无卡可选，造成穿卡数*100的伤害

### 单玉如 / 战斗人物!106:3

- 当前判断：`武功` / 名称：`天魔遁`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：天魔遁：受到攻击/不利效果/参与战斗时，自-上限的50%，使此次攻击/不利效果/回合未发生，逃离战场直至来源死亡；对阵受到攻击/效果时，自-300，可于此时撤退

### 厉若海 / 战斗人物!114:3

- 当前判断：`招式` / 名称：`燎原百击·三十击`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：燎原百击·三十击： 一次性造成30击，每一击为厉若海克敌，伤害100（基础）

### 厉若海 / 战斗人物!114:4

- 当前判断：`招式` / 名称：`燎原百击·二十针`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：燎原百击·二十针： 可解除自身以及他人的非毒异常，禁制

### 跋锋寒 / 战斗人物!125:4

- 当前判断：`技能` / 名称：`射月神弓`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：射月神弓：场下可对敌造成不知来源的等同于自身攻击力的伤害（一定造成），限一次，每次上场恢复使用次数

### 寇仲 / 战斗人物!132:4

- 当前判断：`技能` / 名称：`井中月`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：井中月：对阵受到非对阵的干扰无效并攻击来源一井中八法；未对阵时受到波及可与来源战斗一回合

### 鲁妙子 / 战斗人物!135:2

- 当前判断：`技能` / 名称：`奇门异术`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：奇门异术：无法在侧面及非正常战斗中找到鲁妙子

### 石之轩 / 战斗人物!139:2

- 当前判断：`武功` / 名称：`幻魔身法`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：幻魔身法：一回合受到不超过2次攻击则闪避

### 宋缺 / 战斗人物!140:2

- 当前判断：`招式` / 名称：`得刀而忘刀`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：得刀而忘刀：-- 杀死一生命<2000者；发动成功后可立即再发动一次

### 婠婠 / 战斗人物!141:3

- 当前判断：`招式` / 名称：`纤手驭龙`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：纤手驭龙：每3回合可控制某次己不参与的战斗中敌双方一回合（奇门）

### 杨虚彦 / 战斗人物!145:3

- 当前判断：`招式` / 名称：`黑手魔功`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：黑手魔功：-- 200毒混，敌下两回合无攻击能力且克敌算平

### 祝玉妍 / 战斗人物!148:2

- 当前判断：`武功` / 名称：`天魔力场`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：天魔力场：可将敌内/招卡融为一张，敌被融卡互打一次；自身有受到禁制的趋势时，使该禁制作用于力场（禁制实际无效，发出者以为生效）

### 祝玉妍 / 战斗人物!148:3

- 当前判断：`武功` / 名称：`天魔焚身`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：天魔焚身：敌每有一空可令其-300乱

### 祝玉妍 / 战斗人物!148:4

- 当前判断：`武功` / 名称：`玉石俱焚`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：玉石俱焚：可与选中敌战斗两回合，如祝玉妍未死则敌受其发动玉石俱焚时生命两倍的一定造成伤害且祝玉妍死亡

### 孙恩 / 战斗人物!154:2

- 当前判断：`武功` / 名称：`黄天无极`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：黄天无极：孙恩回合中任意时刻可令所有敌流失（孙恩卡上火（4）+手中火基础卡+黄天中火）*100的生命，孙恩回复此数值的生命（可破上限）

### 燕飞 / 战斗人物!157:2

- 当前判断：`内功` / 名称：`金丹大法`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：金丹大法：此卡无法模仿☯生命不恰好到0则回满，不中异常

### 成昆 / 战斗人物!165:2

- 当前判断：`内功` / 名称：`少林九阳功`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：少林九阳功：攻防各+100

### 郭襄 / 战斗人物!169:3

- 当前判断：`招式` / 名称：`四象掌`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：四象掌：放卡为木金火水的任意排列则被克算平

### 郭襄 / 战斗人物!169:4

- 当前判断：`招式` / 名称：`金顶绵掌`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：金顶绵掌：金- 400 永迟

### 郭襄 / 战斗人物!169:5

- 当前判断：`招式` / 名称：`飘雪穿云掌`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：飘雪穿云掌：招式里出现水则敌冰

### 郭襄 / 战斗人物!169:6

- 当前判断：`招式` / 名称：`佛光普照`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：佛光普照：火土 700*出场回合 封

### 何足道 / 战斗人物!170:3

- 当前判断：`技能` / 名称：`百鸟朝凤`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：百鸟朝凤：弹奏一曲，场上所有懂音律者解除不利转态

### 灭绝师太 / 战斗人物!173:3

- 当前判断：`招式` / 名称：`金顶绵掌`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：金顶绵掌：金- 300 永迟

### 灭绝师太 / 战斗人物!173:4

- 当前判断：`招式` / 名称：`佛光普照`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：佛光普照：火土 800封

### 灭绝师太 / 战斗人物!173:5

- 当前判断：`招式` / 名称：`截手九式`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：截手九式：-火 400惊

### 灭绝师太 / 战斗人物!173:6

- 当前判断：`招式` / 名称：`飘雪穿云掌`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：飘雪穿云掌：水- 200冰

### 灭绝师太 / 战斗人物!173:7

- 当前判断：`招式` / 名称：`四象掌`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：四象掌：按“木金火水”放卡则被克算平

### 俞莲舟 / 战斗人物!174:2

- 当前判断：`招式` / 名称：`绵掌`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：绵掌：-木 木- 敌生命某位数字下回合后减少n，n为骰子数

### 俞莲舟 / 战斗人物!174:3

- 当前判断：`招式` / 名称：`虎爪绝户手`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：虎爪绝户手：杀死其的敌去除所有大招并此后受伤*失去大招数

### 杨逍 / 战斗人物!178:3

- 当前判断：`招式` / 名称：`二十二般兵刃，四十四套招式`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：二十二般兵刃，四十四套招式：可释放场上可见一主动招式、武功/回合，每个限一次（博）

### 殷梨亭 / 战斗人物!179:2

- 当前判断：`招式` / 名称：`神门十三剑`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：神门十三剑：-- 300；剑的攻击造成点

### 殷梨亭 / 战斗人物!179:3

- 当前判断：`招式` / 名称：`天地同寿`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：天地同寿：回合中与敌发生接触时（击中/被击中）可选择自身死亡（无法被梯云纵闪避），敌-90%*初始生命

### 张无忌 / 战斗人物!183:2

- 当前判断：`内功` / 名称：`乾坤大挪移`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：乾坤大挪移：受到单次攻击≤500则可转移到除来源外一处；可暗中学会场上使用过的招式；自身主动大招放法的五行变为-

### 张无忌 / 战斗人物!183:4

- 当前判断：`武功` / 名称：`圣火令神功`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：圣火令神功：不使用其他招式、武功，则可令敌本回合失去攻击、防御、精神控制类相关特技；使用的回合被佛门大招攻击则死

### 周芷若 / 战斗人物!185:3

- 当前判断：`招式` / 名称：`白蟒鞭`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：白蟒鞭：回合中禁敌闪避、撤退、动卡,战斗被干扰反击300*距离（奇门）

### 周芷若 / 战斗人物!185:4

- 当前判断：`招式` / 名称：`峨嵋剑法`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：峨嵋剑法：-木 300 伤害免疫（剑）

### 周芷若 / 战斗人物!185:5

- 当前判断：`招式` / 名称：`金顶绵掌`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：金顶绵掌：金- 400迟

### 宋远桥 / 战斗人物!186:3

- 当前判断：`招式` / 名称：`绵掌`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：绵掌：-木 木- 敌生命某位数字下回合后减少n，n为骰子数

### 宋远桥 / 战斗人物!186:5

- 当前判断：`武功` / 名称：`拂袖功`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：拂袖功：每回合可额外输出500至场上任一人物，若受到响应可收回视为未放

### 胡一刀 / 战斗人物!187:2

- 当前判断：`招式` / 名称：`苗家剑法`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：苗家剑法：300 惊愕，伤害不能抵挡；每回合可直接释放

### 苗人凤 / 战斗人物!188:2

- 当前判断：`招式` / 名称：`胡家刀法`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：胡家刀法：400 对方一大招无法再用(由被攻击者选择)；每回合可直接释放

### 葵花老祖 / 战斗人物!194:8

- 当前判断：`技能` / 名称：`葵花宝典`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：葵花宝典：优先结算修习者的一切；有一次直接杀死所有对阵者的机会

### 令狐冲 / 战斗人物!197:2

- 当前判断：`内功` / 名称：`吸星大法`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：吸星大法：吸敌100攻击/回合，两轮后失去该攻击并再-100攻击

### 令狐冲 / 战斗人物!197:4

- 当前判断：`招式` / 名称：`五岳剑法`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：五岳剑法：-- 100*5

### 任我行 / 战斗人物!198:3

- 当前判断：`招式` / 名称：`风雷剑势`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：风雷剑势：己在回合中的攻击同时攻击全部对阵者（剑）

### 岳不群 / 战斗人物!199:3

- 当前判断：`招式` / 名称：`太岳三青峰`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：太岳三青峰：-土 300惊 不可闪避（剑）

### 岳不群 / 战斗人物!199:4

- 当前判断：`招式` / 名称：`五岳剑法`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：五岳剑法：-- 500迟（剑）

### 岳不群 / 战斗人物!199:5

- 当前判断：`招式` / 名称：`辟邪剑法`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：辟邪剑法：水金 800破 可前提两张释放，无剑亦可放（剑）

### 左冷禅 / 战斗人物!200:3

- 当前判断：`招式` / 名称：`嵩山剑法`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：嵩山剑法：-- 400混乱（剑）

### 左冷禅 / 战斗人物!200:4

- 当前判断：`招式` / 名称：`辟邪剑法`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：辟邪剑法：水木 随机抢敌一半基础卡（剑）

### 莫大先生 / 战斗人物!201:2

- 当前判断：`招式` / 名称：`百变千幻衡山云雾十三式`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：百变千幻衡山云雾十三式：木- 100*13 最多闪避其中的一击

### 田伯光 / 战斗人物!202:4

- 当前判断：`武功` / 名称：`万里独行`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：万里独行：一转轮可以找一女子作战（可以与白人作战，视为一女子），此次作战打得好且输出高则自身回满，该女子去除一条特技；作战后隐匿自身；

### 谢烟客 / 战斗人物!206:2

- 当前判断：`招式` / 名称：`弹指神通`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：弹指神通：-土 任意一敌200点

### 谢烟客 / 战斗人物!206:3

- 当前判断：`招式` / 名称：`控鹤功`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：控鹤功：接下一特技/回合

### 丁春秋 / 战斗人物!208:4

- 当前判断：`技能` / 名称：`连环腐尸毒`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：连环腐尸毒：用尸体或彻底牺牲队友使一敌-500毒（如连环使用腐尸毒，伤害较上一次伤害翻倍）

### 丁春秋 / 战斗人物!208:5

- 当前判断：`技能` / 名称：`三笑逍遥散`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：三笑逍遥散：暗中指定一人使用，该人三克他人后死亡；1/2被人得知，如被得知，则该人一回合后此毒解除；如未被得知则可再次使用

### 段延庆 / 战斗人物!209:2

- 当前判断：`招式` / 名称：`细铁杖`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：细铁杖：金土 200*5（棍杖）

### 慕容博 / 战斗人物!214:2

- 当前判断：`招式` / 名称：`斗转星移`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：斗转星移：可以敌大招反击敌；每次出战前可选择具有并直接使用一本局已用出过的大招，持续至下回合出战前（博）

### 慕容复 / 战斗人物!215:3

- 当前判断：`技能` / 名称：`悲酥清风`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：悲酥清风：一次性，令某回合中任意人物本回合不能用大招，且放卡最终视为空；己可解

### 天山童姥 / 战斗人物!216:3

- 当前判断：`招式` / 名称：`天山折梅手`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：天山折梅手：一回合中不使用天山六阳掌，则可随机抽取废牌中两个具有主动招式、武功的人物，每人任选一个主动招式、武功，将其施放的结果合成为一并在本回合直接施放

### 天山童姥 / 战斗人物!216:4

- 当前判断：`招式` / 名称：`生死符`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：生死符：-- 控制敌，敌可选择此后-400生命及上限/张以解除控制，无上限则死亡；己可选择为其解除控制

### 无崖子 / 战斗人物!217:3

- 当前判断：`技能` / 名称：`【珍珑】`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：【珍珑】：生命到0后，无攻击能力，【残】，战斗变为己放一张，敌猜其为五行一种；猜中则敌被逆运北冥；猜错则敌与自身相同幻象作战至胜出（杀死幻象或至打得好）（可出战次数为生命至0前己出场次数，有过珍珑者，自身死亡）

### 虚竹 / 战斗人物!220:3

- 当前判断：`招式` / 名称：`天山折梅手`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：天山折梅手：-- 抽取一主动大招并随机附加冰狂迟乱惊点中一种

### 虚竹 / 战斗人物!220:4

- 当前判断：`招式` / 名称：`生死符`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：生死符：-- 此后控制敌；若敌不受控制则-400上限/张，无上限则死亡，会天山六阳掌者可解除（虚竹只对【恶】使用）

### 玄慈 / 战斗人物!222:2

- 当前判断：`招式` / 名称：`般若掌`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：般若掌：自己为空时敌对应卡亦最终为空，无法响应

### 游坦之 / 战斗人物!223:3

- 当前判断：`武功` / 名称：`腐尸毒`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：腐尸毒：用尸体或彻底牺牲队友使一敌-500毒

### 陈家洛 / 战斗人物!225:2

- 当前判断：`招式` / 名称：`庖丁解牛掌`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：庖丁解牛掌：-- 招式两卡五行相生/相克/相同组合放出后打没敌自上而下首条/自下而上首条/中央特技；使用此特技时敌无法响应

### 陆菲青 / 战斗人物!226:2

- 当前判断：`招式` / 名称：`芙蓉金针`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：芙蓉金针：回合中使一对阵敌-骰子数*200

### 陆菲青 / 战斗人物!226:3

- 当前判断：`招式` / 名称：`无极玄功拳`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：无极玄功拳：当敌不持兵器时，敌单项输出削减100

### 纳斯尔丁·阿凡提 / 战斗人物!227:2

- 当前判断：`技能` / 名称：`戏耍`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：戏耍：戏耍另一人，可使其不能使用非大招，同时也可对其+/-互变，×/÷互变（不是禁制）；更换目标则上一目标清醒，不能在被戏耍者出战时变更目标

### 王维扬 / 战斗人物!228:2

- 当前判断：`招式` / 名称：`八卦刀`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：八卦刀：金火 300 攻击对阵所有敌；按照八卦刀放且未放出则刀中加镖变为75%命中

### 无尘道长 / 战斗人物!230:2

- 当前判断：`招式` / 名称：`连环迷踪腿`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：连环迷踪腿：-- 300 非两平可放；回合中每相克一次则主动释放时伤害上升300；受非兵器类攻击以此反击敌

### 赵半山 / 战斗人物!233:3

- 当前判断：`技能` / 名称：`回龙璧`
- 标记：`inherited_kind, inherited_named_ability`
- 原文：回龙璧：-- 600不能闪 击打选定路径或单目标回力（暗）

- 仅显示前 100 条，完整列表见 `data/cards_current/abilities.jsonl`。

## 继承上一类型但没有缩进

- 数量：114

### 花满楼 / 战斗人物!31:2

- 当前判断：`招式` / 名称：`流云飞袖`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：流云飞袖：对阵双方所放卡不可改变

### 花满楼 / 战斗人物!31:3

- 当前判断：`招式` / 名称：`听风辨位`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：听风辨位：听出他人身份及招式卡

### 司空摘星 / 战斗人物!36:2

- 当前判断：`技能` / 名称：`偷王之王`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：偷王之王：随时可获取某人可见的一（特技，物品，基础卡），成功率起始各为（2/3，1，1），用一次降低1/6；对同一人物最多只拥有其一特技，对同一个人物多次使用需要多个身份；可还回

### 花无缺 / 战斗人物!41:2

- 当前判断：`内功` / 名称：`移花接玉`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：移花接玉：可反射不高于300的伤害

### 魏无牙 / 战斗人物!46:2

- 当前判断：`技能` / 名称：`机关学`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：机关学：只承受未攻击加成的基础对阵伤害，禁对阵动卡

### 魏无牙 / 战斗人物!46:3

- 当前判断：`技能` / 名称：`车子`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：车子：-500/回合（随机一敌）

### 魏无牙 / 战斗人物!46:4

- 当前判断：`技能` / 名称：`子鼠`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：子鼠：全过一轮，每人掷骰考验，未过2者生命减半，自+300以及他人总减血量（可用两次）

### 紫衣侯 / 战斗人物!53:2

- 当前判断：`招式` / 名称：`一百九十三家秘门剑法`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：一百九十三家秘门剑法：- 1930（剑）

### 千手书生 / 战斗人物!56:2

- 当前判断：`武功` / 名称：`万流归宗`
- 标记：`author_corrected, inherited_kind, inherited_named_ability, missing_indent_for_inherited, unit_specific_ability`
- 原文：万流归宗：接下大招且视为成功施放

### 厉若海 / 战斗人物!114:3

- 当前判断：`招式` / 名称：`燎原百击·三十击`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：燎原百击·三十击： 一次性造成30击，每一击为厉若海克敌，伤害100（基础）

### 厉若海 / 战斗人物!114:4

- 当前判断：`招式` / 名称：`燎原百击·二十针`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：燎原百击·二十针： 可解除自身以及他人的非毒异常，禁制

### 寇仲 / 战斗人物!132:4

- 当前判断：`技能` / 名称：`井中月`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：井中月：对阵受到非对阵的干扰无效并攻击来源一井中八法；未对阵时受到波及可与来源战斗一回合

### 郭襄 / 战斗人物!169:3

- 当前判断：`招式` / 名称：`四象掌`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：四象掌：放卡为木金火水的任意排列则被克算平

### 郭襄 / 战斗人物!169:4

- 当前判断：`招式` / 名称：`金顶绵掌`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：金顶绵掌：金- 400 永迟

### 郭襄 / 战斗人物!169:5

- 当前判断：`招式` / 名称：`飘雪穿云掌`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：飘雪穿云掌：招式里出现水则敌冰

### 郭襄 / 战斗人物!169:6

- 当前判断：`招式` / 名称：`佛光普照`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：佛光普照：火土 700*出场回合 封

### 宋远桥 / 战斗人物!186:5

- 当前判断：`武功` / 名称：`拂袖功`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：拂袖功：每回合可额外输出500至场上任一人物，若受到响应可收回视为未放

### 葵花老祖 / 战斗人物!194:8

- 当前判断：`技能` / 名称：`葵花宝典`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：葵花宝典：优先结算修习者的一切；有一次直接杀死所有对阵者的机会

### 令狐冲 / 战斗人物!197:2

- 当前判断：`内功` / 名称：`吸星大法`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：吸星大法：吸敌100攻击/回合，两轮后失去该攻击并再-100攻击

### 岳不群 / 战斗人物!199:4

- 当前判断：`招式` / 名称：`五岳剑法`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：五岳剑法：-- 500迟（剑）

### 莫大先生 / 战斗人物!201:2

- 当前判断：`招式` / 名称：`百变千幻衡山云雾十三式`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：百变千幻衡山云雾十三式：木- 100*13 最多闪避其中的一击

### 田伯光 / 战斗人物!202:4

- 当前判断：`武功` / 名称：`万里独行`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：万里独行：一转轮可以找一女子作战（可以与白人作战，视为一女子），此次作战打得好且输出高则自身回满，该女子去除一条特技；作战后隐匿自身；

### 丁春秋 / 战斗人物!208:4

- 当前判断：`技能` / 名称：`连环腐尸毒`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：连环腐尸毒：用尸体或彻底牺牲队友使一敌-500毒（如连环使用腐尸毒，伤害较上一次伤害翻倍）

### 丁春秋 / 战斗人物!208:5

- 当前判断：`技能` / 名称：`三笑逍遥散`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：三笑逍遥散：暗中指定一人使用，该人三克他人后死亡；1/2被人得知，如被得知，则该人一回合后此毒解除；如未被得知则可再次使用

### 慕容复 / 战斗人物!215:3

- 当前判断：`技能` / 名称：`悲酥清风`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：悲酥清风：一次性，令某回合中任意人物本回合不能用大招，且放卡最终视为空；己可解

### 无崖子 / 战斗人物!217:3

- 当前判断：`技能` / 名称：`【珍珑】`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：【珍珑】：生命到0后，无攻击能力，【残】，战斗变为己放一张，敌猜其为五行一种；猜中则敌被逆运北冥；猜错则敌与自身相同幻象作战至胜出（杀死幻象或至打得好）（可出战次数为生命至0前己出场次数，有过珍珑者，自身死亡）

### 虚竹 / 战斗人物!220:3

- 当前判断：`招式` / 名称：`天山折梅手`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：天山折梅手：-- 抽取一主动大招并随机附加冰狂迟乱惊点中一种

### 虚竹 / 战斗人物!220:4

- 当前判断：`招式` / 名称：`生死符`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：生死符：-- 此后控制敌；若敌不受控制则-400上限/张，无上限则死亡，会天山六阳掌者可解除（虚竹只对【恶】使用）

### 公孙止 / 战斗人物!235:3

- 当前判断：`招式` / 名称：`阴阳倒乱刃`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：阴阳倒乱刃：可同时以招式换敌内功，内功换敌招式（一次或两次），每次交换对敌造成400伤害；可刀剑双持（刀，剑）

### 郭襄 / 战斗人物!236:3

- 当前判断：`招式` / 名称：`玉女剑法`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：玉女剑法：火金 200 乱

### 郭襄 / 战斗人物!236:4

- 当前判断：`招式` / 名称：`全真剑法`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：全真剑法：金木 100 狂

### 郭襄 / 战斗人物!236:5

- 当前判断：`招式` / 名称：`铁掌`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：铁掌：金土 土金 500*2

### 郭襄 / 战斗人物!236:6

- 当前判断：`招式` / 名称：`玉箫剑法`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：玉箫剑法：火木 100 狂×2

### 郭襄 / 战斗人物!236:7

- 当前判断：`招式` / 名称：`碧波掌法`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：碧波掌法：火水 200 封×2

### 郭襄 / 战斗人物!236:8

- 当前判断：`招式` / 名称：`兰花拂穴手`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：兰花拂穴手：-水 200点

### 郭襄 / 战斗人物!236:9

- 当前判断：`招式` / 名称：`罗汉拳`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：罗汉拳：木土 100×2

### 郭襄 / 战斗人物!236:10

- 当前判断：`招式` / 名称：`空明拳`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：空明拳：招式处可不放卡；空对敌500 封

### 郭襄 / 战斗人物!236:11

- 当前判断：`招式` / 名称：`打狗棒`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：打狗棒：结束时可多打一张招式 100 点

### 郭襄 / 战斗人物!236:12

- 当前判断：`招式` / 名称：`狂风绝技`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：狂风绝技：100 封 100 迟；敌可用特技挡

### 郭襄 / 战斗人物!236:13

- 当前判断：`招式` / 名称：`泥鳅功`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：泥鳅功：每类攻击只承受其中一击

### 郭襄 / 战斗人物!236:14

- 当前判断：`招式` / 名称：`越女剑`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：越女剑：正好两克清除敌卡

### 林朝英 / 战斗人物!239:4

- 当前判断：`招式` / 名称：`全真剑法`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：全真剑法：-木 200狂（剑）

### 裘千尺 / 战斗人物!240:2

- 当前判断：`招式` / 名称：`阴阳倒乱刃`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：阴阳倒乱刃：内功、招式各与敌招式、内功互换最多两次，每次敌-200；可使人看破（刀剑双持）

### 裘千尺 / 战斗人物!240:3

- 当前判断：`招式` / 名称：`枣核钉`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：枣核钉：在任一张时攻击任一人使之-500；5张后可再用（暗）

### 穆人清 / 战斗人物!276:3

- 当前判断：`招式` / 名称：`华山剑法`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：华山剑法：火金 300 禁招

### 穆人清 / 战斗人物!276:4

- 当前判断：`招式` / 名称：`劈石破玉拳`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：劈石破玉拳：-土 400 破

### 穆人清 / 战斗人物!276:5

- 当前判断：`招式` / 名称：`混元掌`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：混元掌：木- 300

### 穆人清 / 战斗人物!276:6

- 当前判断：`招式` / 名称：`伏虎拳`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：伏虎拳：自身两卡相克（需放出）200

### 穆人清 / 战斗人物!276:7

- 当前判断：`招式` / 名称：`天外飞龙`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：天外飞龙：失去剑，使一敌-1000；若敌死亡则收回剑

### 袁承志 / 战斗人物!278:3

- 当前判断：`招式` / 名称：`金蛇剑法`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：金蛇剑法：土金 300×3 被击中者生命此后连带损失

### 袁承志 / 战斗人物!278:4

- 当前判断：`招式` / 名称：`劈石破玉拳`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：劈石破玉拳：-土 400 破

### 袁承志 / 战斗人物!278:5

- 当前判断：`招式` / 名称：`混元掌`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：混元掌：木- 300

### 袁承志 / 战斗人物!278:6

- 当前判断：`招式` / 名称：`伏虎拳`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：伏虎拳：自身两卡相克（需放出）200

### 袁承志 / 战斗人物!278:8

- 当前判断：`武功` / 名称：`神行百变`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：神行百变：复制场上可见动卡效果；任何一张招式后可撤退

### 李文秀 / 战斗人物!280:2

- 当前判断：`招式` / 名称：`流星锤`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：流星锤：200 出血（奇门）

### 李文秀 / 战斗人物!280:3

- 当前判断：`招式` / 名称：`黑血神针`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：黑血神针：一次性，1/3杀死一人，如敌未死亡，敌失去防御与回复能力（暗）

### 陆雪琪 / 战斗人物!300:3

- 当前判断：`武功` / 名称：`天书残卷`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：天书残卷：不对他人使用特技，不响应他人时不需翻出；

### 周一仙 / 战斗人物!302:4

- 当前判断：`技能` / 名称：`五丁金甲，小鬼搬运`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：五丁金甲，小鬼搬运：回合任意时刻可与敌拼点，不低于敌则中止战斗，若失败则剩余战斗期间无攻击能力

### 浦饭幽助 / 战斗人物!303:2

- 当前判断：`招式` / 名称：`【灵光波动拳】`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：【灵光波动拳】：消耗一发灵丸使自身一回合内击中数×3，且每次击中附加100额外伤害（不再算入击中）；附加的额外伤害一定造成

### 童林 / 战斗人物!304:2

- 当前判断：`招式` / 名称：`八法神钺`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：八法神钺：击中敌敌-200并出血；-金 金- 400破（奇门）

### 童林 / 战斗人物!304:3

- 当前判断：`招式` / 名称：`七十二式地行剑`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：七十二式地行剑： 金- -金 700迟

### 马保国 / 战斗人物!317:2

- 当前判断：`内功` / 名称：`松活弹抖劲儿`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：松活弹抖劲儿：回合中使自身的一次攻击发生弹抖，50%几率使之再计算一次

### 马保国 / 战斗人物!317:4

- 当前判断：`招式` / 名称：`浑元形意十三刀`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：浑元形意十三刀：金金 1300

### 马保国 / 战斗人物!317:5

- 当前判断：`招式` / 名称：`闪电指`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：闪电指：100 无法响应

### 岳飞 / 战斗人物!320:2

- 当前判断：`招式` / 名称：`岳家枪`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：岳家枪：-- 200

### 皇太极 / 战斗人物!328:3

- 当前判断：`武功` / 名称：`【大日烈焰刀】`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：【大日烈焰刀】：皇太极不能使用；不中禁制，攻*2且伤害一定造成

### 皇太极 / 战斗人物!328:5

- 当前判断：`技能` / 名称：`（技能`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：（技能：炼金术：一次性，可以令一人或物一刹那不存在或存在数量为2）并随机选取场上一人物，随机完美获取其一特技赋予机械（无视是否翻开）

### 雄霸 / 战斗人物!335:3

- 当前判断：`招式` / 名称：`排云掌`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：排云掌：--300；雄霸普攻可为排云掌

### 雄霸 / 战斗人物!335:4

- 当前判断：`招式` / 名称：`风神腿`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：风神腿：--100；雄霸每攻击一次可触发

### 雾雨魔理沙 / 战斗人物!336:2

- 当前判断：`符卡` / 名称：`究极火花`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：究极火花：对阵敌每打一张及使用一特技1/6死亡（一次性）

### 雾雨魔理沙 / 战斗人物!336:3

- 当前判断：`符卡` / 名称：`慧星`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：慧星：对阵每相关一次及每打一张场上所有敌-200（一次性）

### 任狂 / 战斗人物!347:3

- 当前判断：`招式` / 名称：`从心所欲`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：从心所欲：一次击中等同于任意次击中，敌若闪避则需闪避所有击中

### 狄飞惊 / 战斗人物!360:2

- 当前判断：`招式` / 名称：`眼刀`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：眼刀：对阵一敌损600惊，对瞎子无效（一次性）

### 方恨少 / 战斗人物!361:2

- 当前判断：`武功` / 名称：`一扇日月晴方好`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：一扇日月晴方好：受到攻击（回合/次）则可反击300

### 雷阵雨 / 战斗人物!365:3

- 当前判断：`招式` / 名称：`霹雳神火`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：霹雳神火：一次性使用，一回合中敌每次接触雷阵雨（攻击与被击中）受到n*100的伤害（n为第n次接触），突破防御；受到翻脸神功加成

### 天衣居士 / 战斗人物!369:3

- 当前判断：`招式` / 名称：`小相思刀，小销魂剑`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：小相思刀，小销魂剑：被己大招击中，敌当前回合未用出的特技此后废除（刀、剑）

### 元十三限 / 战斗人物!375:6

- 当前判断：`招式` / 名称：`一线杖`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：一线杖：敌大招攻击不超过800则反弹（棍杖）

### 元十三限 / 战斗人物!375:7

- 当前判断：`招式` / 名称：`一喝神功`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：一喝神功：可令敌回合开始先-300，击中则敌此回合无法释放主动特技

### 元十三限 / 战斗人物!375:8

- 当前判断：`招式` / 名称：`起承转合`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：起承转合：可放弃本回合其他攻击，对敌造成一定造成的100,200,300,400

### 元十三限 / 战斗人物!375:9

- 当前判断：`招式` / 名称：`伤心小箭`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：伤心小箭：-木 对任一敌造成生命上限的100%伤害（弓）

### 元十三限 / 战斗人物!375:10

- 当前判断：`招式` / 名称：`化影分身大法`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：化影分身大法：回合中不少于两被克可发动，令每个在场敌受到一个不具备达摩金身的元限分身的攻击，与之战斗一回合（分身不会再次分身）

### 唐老公公 / 战斗人物!386:2

- 当前判断：`武功` / 名称：`万一雷震子`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：万一雷震子：受到不利效果使敌中相同效果，且-1000

### 唐老太太 / 战斗人物!387:2

- 当前判断：`招式` / 名称：`泼墨神斧`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：泼墨神斧：双方每有一张基础卡，敌-200

### 唐老太太 / 战斗人物!387:3

- 当前判断：`招式` / 名称：`留白神箭`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：留白神箭：双方每有一空，敌-200

### 唐朋 / 战斗人物!388:2

- 当前判断：`招式` / 名称：`子母离魂镖`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：子母离魂镖：场上每次发生战斗时可对一敌射出子镖伤害200，被响应可使用母镖，母镖伤害2000但使用后失去此特技(暗)

### 燕狂徒 / 战斗人物!393:3

- 当前判断：`招式` / 名称：`玉石俱焚`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：玉石俱焚：火- - 火 2200

### 刘独峰 / 战斗人物!403:3

- 当前判断：`招式` / 名称：`风雷一剑`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：风雷一剑：相克引发的伤害为（之前未相克数+1）*400

### 刘独峰 / 战斗人物!403:5

- 当前判断：`技能` / 名称：`灭魔弹月弩+一丸神泥`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：灭魔弹月弩+一丸神泥：出场时可射出弹子攻击一敌，弹子总有1/2几率一分为二，每弹300伤害；击中敌则敌无攻击能力一回合

### 刘独峰 / 战斗人物!403:6

- 当前判断：`技能` / 名称：`后羿射阳箭+轩辕昊天镜`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：后羿射阳箭+轩辕昊天镜：连续对阵中敌战斗卡三不同一相同后敌死亡；敌受到与己相同的附加伤害

### 刘独峰 / 战斗人物!403:7

- 当前判断：`技能` / 名称：`秋鱼刀+春秋笔`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：秋鱼刀+春秋笔：每次击中使敌麻痹，自选一特技本回合不能使用（可以重复选择）；持外门兵器者对其无攻击能力

### 曾白水 / 战斗人物!411:2

- 当前判断：`招式` / 名称：`达摩秘拳`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：达摩秘拳：300 伤害无法减免

### 曾白水 / 战斗人物!411:3

- 当前判断：`招式` / 名称：`东海水云袖`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：东海水云袖：化去一次针对自身的攻击或效果／轮

### 曾白水 / 战斗人物!411:4

- 当前判断：`招式` / 名称：`长空神指`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：长空神指：击中后破除敌一切非内功、招式、武功特技

### 曾白水 / 战斗人物!411:5

- 当前判断：`招式` / 名称：`大石神功`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：大石神功：-- 600破

### 曾白水 / 战斗人物!411:6

- 当前判断：`招式` / 名称：`大漠神掌`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：大漠神掌：有被击中趋势敌-200

### 归辛树 / 战斗人物!415:3

- 当前判断：`招式` / 名称：`混元掌`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：混元掌：木- 300

### 归辛树 / 战斗人物!415:4

- 当前判断：`招式` / 名称：`伏虎拳`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：伏虎拳：自身两卡相克（需放出）200

### 归辛树 / 战斗人物!415:6

- 当前判断：`技能` / 名称：`【轻信人言】`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：【轻信人言】：敌可选择与归辛树拼点，使归辛树迟；若赢则将其作战目标改为他人（非【恶】不可将目标改为自己的队友）（身份）

### 四大恶人 / 战斗人物!418:4

- 当前判断：`招式` / 名称：`细铁杖`
- 标记：`author_corrected, inherited_kind, inherited_named_ability, missing_indent_for_inherited, unit_specific_ability`
- 原文：细铁杖：金土 200*5（棍杖）

### 四大恶人 / 战斗人物!418:6

- 当前判断：`字` / 名称：`【恶贯满盈】`
- 标记：`author_corrected, continuation_line, inherited_kind, inherited_named_ability, missing_indent_for_inherited, unit_specific_ability`
- 原文：【恶贯满盈】：可使用“恶贯满盈”特技各一次；起始不在场，如果其余三大恶人都至少出战过一回合则来到场上；最多出战两回合

### 四大恶人 / 战斗人物!418:10

- 当前判断：`字` / 名称：`【无恶不作】`
- 标记：`author_corrected, continuation_line, inherited_kind, inherited_named_ability, missing_indent_for_inherited, unit_specific_ability`
- 原文：【无恶不作】：队友【恶】出战，且己不出战一轮则掳来一个婴儿；每消耗一个婴儿可以出战一回合（身份）

### 四大恶人 / 战斗人物!418:14

- 当前判断：`招式` / 名称：`鳄尾鞭`
- 标记：`author_corrected, inherited_kind, inherited_named_ability, missing_indent_for_inherited, unit_specific_ability`
- 原文：鳄尾鞭：土- 100*3

### 四大恶人 / 战斗人物!418:16

- 当前判断：`技能` / 名称：`南海鳄神`
- 标记：`author_corrected, inherited_kind, inherited_named_ability, missing_indent_for_inherited, unit_specific_ability`
- 原文：南海鳄神：不能动卡，闪避，避战，撤退；双持鳄嘴剪和鳄尾鞭，这两个招式相互可连带放出；自身的全攻击力提高拥有的兵器数*100（博视为一种兵器）

### 四大恶人 / 战斗人物!418:17

- 当前判断：`字` / 名称：`【凶神恶煞】`
- 标记：`author_corrected, continuation_line, inherited_kind, inherited_named_ability, missing_indent_for_inherited, unit_specific_ability`
- 原文：【凶神恶煞】：可要求对方成为自己的徒弟，如果对方同意则不交手（最多只有一个徒弟，需要徒弟死亡才可招收新的徒弟）；最多出战2回合（身份）

### 四大恶人 / 战斗人物!418:22

- 当前判断：`字` / 名称：`【穷凶极恶】`
- 标记：`author_corrected, inherited_kind, inherited_named_ability, missing_indent_for_inherited, unit_specific_ability`
- 原文：【穷凶极恶】：无段延庆时不与岳老三同时出战；对阵女子则一定出战（此时无视岳老三是否出战），不计入自身出战的回合数；最多出战2回合（身份）

### 四大恶人 / 战斗人物!418:23

- 当前判断：`字` / 名称：`云中一鹤`
- 标记：`author_corrected, inherited_kind, inherited_named_ability, missing_indent_for_inherited, unit_specific_ability`
- 原文：云中一鹤：打的差则逃走：闪避本回合攻击且对敌普攻减半

### 石中玉 / 战斗人物!419:8

- 当前判断：`字` / 名称：`玄素庄主`
- 标记：`author_corrected, inherited_kind, inherited_named_ability, missing_indent_for_inherited, unit_specific_ability`
- 原文：玄素庄主：石清可以用本回合的攻击伤害抵挡本回合受到的伤害

### 石中玉 / 战斗人物!419:9

- 当前判断：`字` / 名称：`冰雪神剑`
- 标记：`author_corrected, inherited_kind, inherited_named_ability, missing_indent_for_inherited, unit_specific_ability`
- 原文：冰雪神剑：闵柔的攻击附带冰

### 燕南飞 / 战斗人物!420:4

- 当前判断：`技能` / 名称：`【公子羽】`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：【公子羽】：获得公子羽称号，死亡前不会因为打得差失去此称号，杀死自身者获得公子羽称号且公子羽的死亡视为自杀；可以选择一人物（包括队友）进行一次决战，邀请6位观战者（每方最多邀请3人，邀请相关但不是不利），此战双方尽可能对对方不利，此战打得差则死亡（身份）

### 天龙六僧 / 战斗人物!421:3

- 当前判断：`字` / 名称：`六脉神剑经`
- 标记：`author_corrected, inherited_kind, inherited_named_ability, missing_indent_for_inherited, unit_specific_ability`
- 原文：六脉神剑经：不参与非正常对阵，所有作战均视为对手挑战自己；每被克一次,本回合减少一名僧人攻击敌人，被敌人攻击的僧人本回合不攻击敌人；当所有僧人都不攻击敌人，但仍有未能抵消的克或者被攻击时，焚毁六脉神剑经，此后六脉剑阵不再具有多倍攻击

### 段正明 / 战斗人物!422:4

- 当前判断：`字` / 名称：`【保定帝】`
- 标记：`author_corrected, inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：【保定帝】：可以将大理三公整体派到场上任一人物处或召回；可以令一名队友神速，辅助任一未与己方作战的人物一回合，无需该队友同意；该队友有出战次数限制时，消耗一次出战次数（身份）

### 段正明 / 战斗人物!422:5

- 当前判断：`字` / 名称：`避位为僧`
- 标记：`author_corrected, inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：避位为僧：段正明立即离场;下一局出现天龙六僧时，本尘视为由本局段正明的玩家担当；若两者不是同一玩家，则双方在下一局结盟

### 段正淳 / 战斗人物!423:5

- 当前判断：`字` / 名称：`【大理段二】`
- 标记：`author_corrected, inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：【大理段二】：当场上有人宣布某人为我父/母/养父/养母时，段正淳可无视实际人物关系，宣布自己是该人的亲爹并以高顺位结盟（身份）

### 葵花宝典 / 物品!37:8

- 当前判断：`技能` / 名称：`葵花宝典`
- 标记：`inherited_kind, inherited_named_ability, missing_indent_for_inherited`
- 原文：葵花宝典：优先结算修习者的一切；有一次直接杀死所有对阵者的机会

## 有缩进但按字处理

- 数量：1

### 胡青牛王难姑 / 附加人物!20:3

- 当前判断：`字` / 名称：`【蝶谷医仙】`
- 标记：`author_confirmed_structure, author_corrected, exclusive_word, implicit_word, indented_implicit_word, unit_specific_ability`
- 原文：【蝶谷医仙】：轮到本方行动时可以将一个人物刷新至初始状态

## 有类型前缀但特技名缺少冒号

- 数量：0

## 特技子项没有缩进

- 数量：3

### 柴玉关 / 战斗人物!8:1

- 当前判断：`*` / 名称：`快乐四使`
- 标记：`author_confirmed_structure, implicit_word, nested_indented_line, nested_named_line, nested_named_line_without_indent`
- 原文：*快乐四使：出战时随机从四使中选一，回合中不少于两克则四使本回合全具有 酒：全攻+200 色：对阵敌全攻-200 财：回合结束时自回复600 气：本回合不中非接触不利效果

### 风行烈 / 战斗人物!109:1

- 当前判断：`内功` / 名称：`三道真气`
- 标记：`author_confirmed_structure, inherited_kind, nested_named_line, nested_named_line_without_indent`
- 原文：内功：三道真气：庞斑：敌改变基础战斗方式的特技自-100，使之无效且不再中 厉若海：可支付500生命使燎原枪法被乘数永久+200 鹰缘：内功处只受普攻

### 杨逍 / 战斗人物!178:4

- 当前判断：`*` / 名称：`【五行旗】`
- 标记：`author_confirmed_structure, implicit_word, nested_indented_line, nested_named_line, nested_named_line_without_indent`
- 原文：*【五行旗】：可自弃一张五行卡，使一侧面攻击、不利效果或正面的回合转化为该五行旗与敌战斗： 五行旗生命5000不中即死： 锐金旗：敌先-500； 巨木旗：自伤害加倍，受伤减半； 厚土旗：单项伤害加深100，伤害一定造成； 洪水旗：战斗后敌1/3死； 烈火旗：破除敌防御效果

## 无前缀且按字处理的特技

- 数量：531

### 丁鹏 / 战斗人物!1:4

- 当前判断：`字` / 名称：`【魔刀】`
- 标记：`implicit_word, exclusive_word`
- 原文：【魔刀】：己造成的任意伤害最终不低于本局已知最高单项伤害

### 高渐飞 / 战斗人物!2:3

- 当前判断：`字` / 名称：`【泪痕剑主人】`
- 标记：`implicit_word, exclusive_word`
- 原文：【泪痕剑主人】：杀死萧大师之子则不算做输

### 萧泪血 / 战斗人物!3:2

- 当前判断：`字` / 名称：`浪子三唱，只唱英雄`
- 标记：`implicit_word`
- 原文：浪子三唱，只唱英雄：暗中选定一个人物，该人物死亡前己可不出战，且无法被他人找到，如果发现有泪痕剑，视为选定持有泪痕剑的人物

### 风四娘 / 战斗人物!4:5

- 当前判断：`字` / 名称：`玩最利的刀`
- 标记：`implicit_word`
- 原文：玩最利的刀：对阵时敌我受伤加倍（不需刀）

### 风四娘 / 战斗人物!4:6

- 当前判断：`字` / 名称：`杀最狠的人`
- 标记：`implicit_word`
- 原文：杀最狠的人：死亡时使场上总输出最高者死

### 哥舒天 / 战斗人物!5:3

- 当前判断：`字` / 名称：`【逍遥侯】`
- 标记：`implicit_word, exclusive_word`
- 原文：【逍遥侯】：每杀死一人，则玩偶山庄容量+1

### 哥舒天 / 战斗人物!5:4

- 当前判断：`字` / 名称：`天宗`
- 标记：`implicit_word`
- 原文：天宗：场上任何人可以杀死一人后，经哥舒天同意宣布为天宗人物；如此则该人从属于哥舒天

### 连城璧 / 战斗人物!6:2

- 当前判断：`字` / 名称：`【侠义双无】`
- 标记：`implicit_word, exclusive_word`
- 原文：【侠义双无】：舍弃掉侠义无双并令一非【恶】死亡，且视为另一人物所为（身份）；不可杀天宗中人

### 连城璧 / 战斗人物!6:3

- 当前判断：`字` / 名称：`天宗`
- 标记：`implicit_word`
- 原文：天宗：场上任何人可以杀死一人后宣布为天宗人物，如此局未死则可留至下一局中，本方从属于连城璧

### 萧十一郎 / 战斗人物!7:3

- 当前判断：`字` / 名称：`【人心怜羊，狼心独怆】`
- 标记：`implicit_word, exclusive_word`
- 原文：【人心怜羊，狼心独怆】：萧十一郎陷入单挑时视为敌先挑战；萧十一郎不中无法闪避、抵挡、一定造成、破

### 柴玉关 / 战斗人物!8:1

- 当前判断：`*` / 名称：`快乐四使`
- 标记：`author_confirmed_structure, implicit_word, nested_indented_line, nested_named_line, nested_named_line_without_indent`
- 原文：*快乐四使：出战时随机从四使中选一，回合中不少于两克则四使本回合全具有 酒：全攻+200 色：对阵敌全攻-200 财：回合结束时自回复600 气：本回合不中非接触不利效果

### 柴玉关 / 战斗人物!8:6

- 当前判断：`字` / 名称：`【万家生佛】`
- 标记：`implicit_word, exclusive_word`
- 原文：【万家生佛】：废牌中随机抽10张，学会其中的招式及武功；视为包含在此特技内的不可见的（可被响应）能力，失去此特技则习得的亦失去（博）

### 沈浪 / 战斗人物!9:3

- 当前判断：`字` / 名称：`结交天下`
- 标记：`implicit_word`
- 原文：结交天下：在某人物受到伤害时，可以与其平摊伤害，如此则此后该人有一次机会在己受到伤害时与己平摊伤害（此特技不受到深藏不露的作用），相互承担伤害后两人均同意则可不交手

### 熊猫儿 / 战斗人物!11:3

- 当前判断：`字` / 名称：`妙手空空儿`
- 标记：`implicit_word`
- 原文：妙手空空儿：偷来对阵者一物品，交给自己以外一没有物品的人

### 白飞飞 / 战斗人物!12:6

- 当前判断：`字` / 名称：`【孤身远引，至死不见】`
- 标记：`implicit_word, exclusive_word`
- 原文：【孤身远引，至死不见】：陷入单挑且对方为男子则离场（不算做胜利）

### 傅红雪 / 战斗人物!13:5

- 当前判断：`字` / 名称：`【复仇之神】`
- 标记：`implicit_word, exclusive_word`
- 原文：【复仇之神】（身份）：可与人死战；开场可暗中指定一个仇敌，可以暗中将杀死队友者认为仇敌；有仇敌时则出战先选择仇敌死战，有仇敌则自身在非复仇过程中不会因非仇敌的攻击/效果而死亡/离场（强制留1血，不会被一定造成，破杀死）；杀死仇敌则自身回满（即使当回合傅红雪死亡）

### 谢晓峰 / 战斗人物!14:3

- 当前判断：`字` / 名称：`剑非剑，我非我`
- 标记：`implicit_word`
- 原文：剑非剑，我非我：对阵者立即封，普攻附封，不中封，使用剑法无需【剑】

### 燕十三 / 战斗人物!15:4

- 当前判断：`字` / 名称：`燕十三`
- 标记：`implicit_word`
- 原文：燕十三：普攻附“封”，不中封

### 宫锦弼 / 战斗人物!18:2

- 当前判断：`字` / 名称：`【孙女】`
- 标记：`implicit_word, exclusive_word`
- 原文：【孙女】：第一次杀死人或濒死，视为杀死了孙女，自身生命回满，并暴怒，此后伤害一定造成；致其孙女死亡者（被其杀死或导致宫锦弼濒死）下局少抓一卡

### 蓝天鎚 / 战斗人物!19:2

- 当前判断：`字` / 名称：`【天鎚道人】`
- 标记：`implicit_word, exclusive_word`
- 原文：【天鎚道人】：敌五行或基础卡与蓝大相同时-300；按照基础卡位置计算，若敌在某一位置受伤≥300，则该位置基础卡发生爆炸；爆炸使敌额外-300，同时永久失去该位置的基础卡；爆炸会波及起前后各一位的基础卡，使敌在该两位置再-200；爆炸伤害一定造成

### 展梦白 / 战斗人物!20:2

- 当前判断：`字` / 名称：`【怒】`
- 标记：`implicit_word, exclusive_word`
- 原文：【怒】：受他人相关效果/有被禁制、看不见趋势/对阵【恶】时怒，与之死战，1/3对象错误，在其余人中随机选择；死战中自身乱放且不重新计算怒，回合结束时1/3清醒死战停止；死战错误两次后于清醒时自杀

### 白玉京 / 战斗人物!21:3

- 当前判断：`字` / 名称：`天上白玉京`
- 标记：`implicit_word`
- 原文：天上白玉京：若白玉京每次出战均保持微笑，则不算最后一位输（Tabletop时没法认证）

### 狄青麟 / 战斗人物!22:3

- 当前判断：`字` / 名称：`【侯门深似海】`
- 标记：`implicit_word, exclusive_word`
- 原文：【侯门深似海】：受到非基础卡伤害或受效果则来源敌死亡

### 高立 / 战斗人物!23:3

- 当前判断：`字` / 名称：`平凡`
- 标记：`implicit_word`
- 原文：平凡：可以不使用双枪，不需声明或翻开；带异常的攻击对其无效，伤害>=500的大招对其无效；触发平凡后恢复自信

### 萧少英 / 战斗人物!24:3

- 当前判断：`字` / 名称：`【复仇】`
- 标记：`implicit_word, exclusive_word`
- 原文：【复仇】：队友彻底死亡时，可投入杀死队友一方伺机复仇（与一或多敌死战，生命拉至相同水平，共享不利）；杀死敌自身刷满返回；敌不能派遣萧少英出战（可主动出战）；无论最终萧少英复仇终结后在何方，均为控制方胜利

### 杨铮 / 战斗人物!25:2

- 当前判断：`字` / 名称：`黯然销魂者唯别而已`
- 标记：`implicit_word`
- 原文：黯然销魂者唯别而已：敌对其造成伤害/不利效果趋势时亦受等值伤害（一定造成）/相同不利效果（无视免疫），不会不能响应；可与任一敌死战，无论该人在何处

### 杨铮 / 战斗人物!25:3

- 当前判断：`字` / 名称：`相聚离别`
- 标记：`implicit_word`
- 原文：相聚离别：每次与人死战有一次自-当前生命1/3令敌-当前生命1/2的机会（向上取整），受到不利效果可自损当前生命1/4（向上取整）抵挡该效果（离别钩）

### 柳长街 / 战斗人物!26:2

- 当前判断：`字` / 名称：`【世上的英雄豪杰却已太多了】`
- 标记：`implicit_word, exclusive_word`
- 原文：【世上的英雄豪杰却已太多了】：得知本局所有人物身份的6回合后离去

### 凤三 / 战斗人物!27:2

- 当前判断：`字` / 名称：`【垂天大星江南凤，凤鸣千里天地动】`
- 标记：`implicit_word, exclusive_word`
- 原文：【垂天大星江南凤，凤鸣千里天地动】：非凤三阵营人物与己阵营人物对阵时，输出若不比该人物上回合输出高则攻击与不利效果无效，凤三阵营人物与敌方对阵时，输出至少高出上回合100（如果无法高出，则造成差额的流失，如果无法流失则算作悖论）；一局中如出现悖论、无限循环、卡住导致和局，则相关卡片（除凤三）被扔出游戏不能响应

### 俞佩玉 / 战斗人物!28:4

- 当前判断：`字` / 名称：`【疤痕】`
- 标记：`implicit_word, exclusive_word`
- 原文：【疤痕】：同时拥有假身份俞佩玉，侧面伤害以及全部不利相关效果作用于假身份，正面受伤则己与假身份均承受；当假身份死亡时，假身份以己生命上限重生，当本体死亡时如本体与假身份血量不同（回合中按照回克开始时的血量计算），则本体以己生命上限重生；假身份重生一次后才具有阎王债

### 俞佩玉 / 战斗人物!28:5

- 当前判断：`字` / 名称：`【温柔敦厚】`
- 标记：`implicit_word, exclusive_word`
- 原文：【温柔敦厚】：可使任何特技可控（无视阎王债）

### 宫九 / 战斗人物!29:1

- 当前判断：`字` / 名称：`【自虐】`
- 标记：`implicit_word, exclusive_word`
- 原文：【自虐】：受到攻击视为加血，不利状态转化为当前生命加倍；每三回合结束时取出自身所有生命，并使敌自减该值1/4的伤害，此时生命为0，直至下次回合结束前不会因为生命为0死亡（第一次出场前视为宫九刚刚自虐完）（身份）

### 宫九 / 战斗人物!29:2

- 当前判断：`字` / 名称：`【太平王世子】`
- 标记：`implicit_word, exclusive_word`
- 原文：【太平王世子】：宫九未翻开前可不与人交手，使用此特技不必翻开

### 公孙大娘 / 战斗人物!30:4

- 当前判断：`字` / 名称：`【红鞋子】`
- 标记：`implicit_word, exclusive_word`
- 原文：【红鞋子】：公孙大娘可获得场上女子加入己方，加入的战斗人物角色仍由原玩家控制，若存活至结束可比公孙大娘低一顺位结盟

### 花满楼 / 战斗人物!31:5

- 当前判断：`字` / 名称：`【花满楼】`
- 标记：`implicit_word, exclusive_word`
- 原文：【花满楼】：双方战斗伤害可取最小值；与人永远不相关

### 金九龄 / 战斗人物!32:2

- 当前判断：`字` / 名称：`【绣花大盗】`
- 标记：`implicit_word, exclusive_word`
- 原文：【绣花大盗】：可以绣花大盗出战/切入；自身一切不中；大盗时克敌敌立即瞎，全未被克敌回合后瞎；瞎攻击50%落空，瞎时特技尽可能对对阵者使用，回合内未使用特技一条-300；对瞎无敌（陆小凤识破）；以绣花大盗出场后需要至少以总捕出场一次后才能再次以绣花大盗身份出场

### 老实和尚 / 战斗人物!33:2

- 当前判断：`字` / 名称：`老实和尚的秘密`
- 标记：`implicit_word`
- 原文：老实和尚的秘密：可以丢弃两张基础卡使一事件不失效但算作未发生

### 老实和尚 / 战斗人物!33:3

- 当前判断：`字` / 名称：`老实和尚不老实`
- 标记：`implicit_word`
- 原文：老实和尚不老实：他人可以将基础卡交给老实和尚

### 陆小凤 / 战斗人物!34:3

- 当前判断：`字` / 名称：`【四条眉毛】`
- 标记：`implicit_word, exclusive_word`
- 原文：【四条眉毛】：可主动将被灵犀一指夹住的兵器还回，如敌同意，则己获得一次与之避战的机会；可将自身从针对多个目标且包含自己的伤害/效果中移除（身份）

### 木道人 / 战斗人物!35:2

- 当前判断：`字` / 名称：`老刀把子`
- 标记：`implicit_word`
- 原文：老刀把子：每一转轮可策划一次幽灵山庄中人物对一山庄外人物的围攻（可对不在场使用），策划时，先指定一人物并得知其身份、状态、物品、称号等，然后可以选择发起或不发起围攻（均视作消耗掉本转轮的策划），起始一次，可指定哪些人参与围攻；幽灵山庄中有人物，则木道人可不出战，且他人无法找到木道人（身份）

### 木道人 / 战斗人物!35:3

- 当前判断：`字` / 名称：`【幽灵山庄】`
- 标记：`implicit_word, exclusive_word`
- 原文：【幽灵山庄】：木道人可允许一人物加入山庄，永久隐藏身份，去除不利状态；在山庄中人物可与其结盟胜利（顺位低），木道人须指定一敌对人物为其目标，该人物杀死木道人指定的目标会提高在山庄中的顺位（与木道人持平）；队友起始可认定为已加入山庄，木道人死后幽灵山庄解散

### 司空摘星 / 战斗人物!36:4

- 当前判断：`字` / 名称：`司空猴精`
- 标记：`implicit_word`
- 原文：司空猴精：可选择与非己方一人物比骰子大小，胜方可要求失败方做一件力所能及的事情；对一人物赢后不可再赌

### 西门吹雪 / 战斗人物!37:3

- 当前判断：`字` / 名称：`万梅山庄`
- 标记：`implicit_word`
- 原文：万梅山庄：任何人可挑战西门吹雪，挑战中他看不见一切敌特技；侧面影响西门吹雪转化为一回合对其挑战

### 叶孤城 / 战斗人物!38:3

- 当前判断：`字` / 名称：`决战紫禁之巅`
- 标记：`implicit_word`
- 原文：决战紫禁之巅：可与任一敌决战，如果敌死亡或离场时叶孤城仍然在场，则胜利；胜后比该玩家高一顺位，离场；先与西门吹雪决战，不论结果如何都视为未胜

### 叶孤城 / 战斗人物!38:4

- 当前判断：`字` / 名称：`【白云城主】`
- 标记：`implicit_word, exclusive_word`
- 原文：【白云城主】：每使用一特技，己全攻击+200（单回合计算，本特技不计算在内）

### 孟星魂 / 战斗人物!39:2

- 当前判断：`字` / 名称：`流星蝴蝶剑`
- 标记：`implicit_word`
- 原文：流星蝴蝶剑：翻开后开始刺杀，掷1骰子，n为队友出场数，若≥（6-n）则刺杀成功；掷n个骰子，其中最大结果为可刺杀目标数；彻底杀死该结果数量的人物（无论其在不在场）；若孟星魂一次性杀死3名及以上人物，或杀死所有已存敌，本局孟星魂所在方胜利；刺杀失败孟星魂离场

### 黑蜘蛛 / 战斗人物!40:3

- 当前判断：`字` / 名称：`【黑大哥】`
- 标记：`implicit_word, exclusive_word`
- 原文：【黑大哥】：叫其大哥则不切入攻击该人也不对其使用银丝飞蛛，但此后对其不愿使用任何不利

### 花无缺 / 战斗人物!41:3

- 当前判断：`字` / 名称：`谦谦君子`
- 标记：`implicit_word`
- 原文：谦谦君子：花无缺与人战斗可令双方平不损血，不使用特技；不中狂乱混封

### 花无缺 / 战斗人物!41:4

- 当前判断：`字` / 名称：`【无缺公子】`
- 标记：`implicit_word, exclusive_word`
- 原文：【无缺公子】：可在己未参与的战斗中替他人承担所有不利，如该不利既可造成原承受者死亡亦可造成花无缺死亡，则双方结盟，以花无缺为主

### 江别鹤 / 战斗人物!42:2

- 当前判断：`字` / 名称：`【江南大侠】`
- 标记：`implicit_word, exclusive_word`
- 原文：【江南大侠】：相克不减血，接下大招，与人交手后算作相结交（直接结交队友，不需翻开）；隐去【恶】

### 江别鹤 / 战斗人物!42:3

- 当前判断：`字` / 名称：`伪君子`
- 标记：`implicit_word`
- 原文：伪君子：结交的对象与他人战斗时可出卖之，令其受伤*2，暂时失去防御相关特技及对江用过的特技，但江不可再对被出卖者使用江南大侠，此人得知江别鹤为【恶】；可将之前因江南大侠未损的血于对阵时一次性输出，如对阵者未死则永久失去江南大侠

### 江小鱼 / 战斗人物!43:4

- 当前判断：`字` / 名称：`【小鱼儿】`
- 标记：`implicit_word, exclusive_word`
- 原文：【小鱼儿】：对阵多人时，敌对江小鱼的攻击仅有1/n机会命中（n为对阵的人数）；不中狂、乱、迟、封、混、禁制以及等同于这些异常的效果；不中流失（身份）

### 魏无牙 / 战斗人物!46:8

- 当前判断：`字` / 名称：`天外天`
- 标记：`implicit_word`
- 原文：天外天：未使用钻，则回合结束可使自己和对阵敌困于天外天（一次性）；内部仍然可发生战斗，但是每转轮后所有人生命减半（向上取整），无生命者死亡（江小鱼可离开）;天外天内无其他人物后，魏无牙可以离开天外天

### 叶开 / 战斗人物!49:4

- 当前判断：`字` / 名称：`【树叶的叶，开心的开】`
- 标记：`implicit_word, exclusive_word`
- 原文：【树叶的叶，开心的开】：每上场一次多一次小李飞刀，起始一次；小李飞刀不能替【恶】抵挡致命或打断针对【恶】的特技

### 芮伟 / 战斗人物!50:2

- 当前判断：`字` / 名称：`【大悲剧】`
- 标记：`implicit_word, exclusive_word`
- 原文：【大悲剧】：对芮伟来说看不见的人不存在于本局游戏；弃掉的芮伟无法找回

### 东海白衣人 / 战斗人物!51:2

- 当前判断：`字` / 名称：`寂寞高手`
- 标记：`implicit_word`
- 原文：寂寞高手：第一次上场从扶桑而来，之前不在场；此后强制上场至打得差，返回扶桑，且有一回合再来的机会，此回合中一剑光寒十九州攻+n*200

### 紫衣侯 / 战斗人物!53:3

- 当前判断：`字` / 名称：`五色帆船主`
- 标记：`implicit_word`
- 原文：五色帆船主：紫衣侯不上陆（平时不在场，与其作战在东海之滨）；己不中招式特技；每一转轮结束时他人可登船拜访，此时可用一件物品请求紫衣侯教授破解一指定招式的法门（破解视为该招式对该人物无效）

### 欢乐英雄 / 战斗人物!54:1

- 当前判断：`字` / 名称：`郭大路是个很大路的人`
- 标记：`author_corrected, implicit_word, unit_specific_ability`
- 原文：郭大路是个很大路的人：可屏蔽一类特技（定好后不能改）

### 欢乐英雄 / 战斗人物!54:2

- 当前判断：`字` / 名称：`王动却不动`
- 标记：`author_corrected, implicit_word, unit_specific_ability`
- 原文：王动却不动：对阵可倒置伤害

### 欢乐英雄 / 战斗人物!54:3

- 当前判断：`字` / 名称：`燕七的秘密`
- 标记：`author_corrected, implicit_word, unit_specific_ability`
- 原文：燕七的秘密：可防*2，若不*2则对阵敌不能使用效果【暗】

### 欢乐英雄 / 战斗人物!54:4

- 当前判断：`字` / 名称：`林太平的身份`
- 标记：`author_corrected, implicit_word, unit_specific_ability`
- 原文：林太平的身份：可攻*2；使四人不受禁制【剑】

### 欢乐英雄 / 战斗人物!54:5

- 当前判断：`字` / 名称：`【欢乐英雄】`
- 标记：`author_corrected, exclusive_word, implicit_word, unit_specific_ability`
- 原文：【欢乐英雄】：出战可更换人物，一人死亡时若其他三人存活，则该人重生，其余三人各-300

### 裴珏 / 战斗人物!55:2

- 当前判断：`字` / 名称：`坚韧宽恕`
- 标记：`implicit_word`
- 原文：坚韧宽恕：已损血者的不利对裴珏无效；裴珏攻击任何人都会强制剩一滴血，裴珏不会杀死人

### 千手书生 / 战斗人物!56:3

- 当前判断：`字` / 名称：`【千手书生】`
- 标记：`author_corrected, exclusive_word, implicit_word, unit_specific_ability`
- 原文：【千手书生】：如打得好，断敌一手，使敌失去攻防加成，随机失去两张基础战斗卡，-300/轮；如敌已被己断一手，且再打得好，可再断之一手，使敌失去攻防能力，再随机失去三张基础战斗卡，多-400/轮

### 檀明 / 战斗人物!57:5

- 当前判断：`字` / 名称：`飞龙镖局总镖头`
- 标记：`implicit_word`
- 原文：飞龙镖局总镖头：敌对檀明使用非被动大招则死亡；檀明受伤害时只承受其中某非0位*100

### 李坏 / 战斗人物!58:3

- 当前判断：`字` / 名称：`【飞刀，又见飞刀】`
- 标记：`implicit_word, exclusive_word`
- 原文：【飞刀，又见飞刀】：第一次放出小李飞刀对方死亡；可宣布与一人决战使两人消失

### 月神 / 战斗人物!59:2

- 当前判断：`字` / 名称：`【月神】`
- 标记：`implicit_word, exclusive_word`
- 原文：【月神】：出战时可点名挑战，若如此做则该战斗无他人在场（点名须叫出对手名字，对于未亮出，未在场者有效）

### 郭嵩阳 / 战斗人物!62:2

- 当前判断：`字` / 名称：`【舍生取义】`
- 标记：`implicit_word, exclusive_word`
- 原文：【舍生取义】：可要求与某人比武，此战中该人尽量对郭嵩阳不利，使用过的特技、物品对郭指定的人不再有效

### 荆无命 / 战斗人物!63:2

- 当前判断：`字` / 名称：`【右手的秘密】`
- 标记：`implicit_word, exclusive_word`
- 原文：【右手的秘密】：有濒死趋势则附加【残】，生命为0，失去左手剑，抵御死亡，如在战斗中则中止战斗，直至下次受到伤害则死亡；期间每回合攻击视为攻击次数不变，总伤害为所有单项伤害之积的攻击，至少一次攻击命中则可造成总伤害，且后发先至，不可闪避，转（剑）

### 林仙儿 / 战斗人物!65:3

- 当前判断：`字` / 名称：`梅花盗`
- 标记：`implicit_word`
- 原文：梅花盗：场上攻击加成及分段攻击不可用（可控）；本局无其他小偷则可偷来全部宝物，自-200/个

### 上官金虹 / 战斗人物!66:3

- 当前判断：`字` / 名称：`【金钱帮主】`
- 标记：`implicit_word, exclusive_word`
- 原文：【金钱帮主】：可将招式和对阵敌内功整体互换；可支付1500收买一恶人；不上场一轮则金钱+300

### 花双霜 / 战斗人物!67:3

- 当前判断：`字` / 名称：`【忆女成狂】`
- 标记：`implicit_word, exclusive_word`
- 原文：【忆女成狂】：非大旗英雄传美丽女性可认母（至多一女）；不分敌我攻击全体，不攻击女儿

### 日后 / 战斗人物!68:4

- 当前判断：`字` / 名称：`常春岛主`
- 标记：`implicit_word`
- 原文：常春岛主：日后亮出后获得弃牌中的女子，己方的女性不会改变所在方

### 飧毒大师 / 战斗人物!69:7

- 当前判断：`字` / 名称：`【毒神现体】`
- 标记：`implicit_word, exclusive_word`
- 原文：【毒神现体】：被飧毒大师杀死、毒死者化为毒神：生命2000，不中普攻、异常，毒神战斗全为招式，攻击附毒

### 铁中棠 / 战斗人物!70:5

- 当前判断：`字` / 名称：`铁血大旗门`
- 标记：`implicit_word`
- 原文：铁血大旗门：铁中棠仅计算受到过的一人物对己的总伤害，其余搁置，如该人死亡则伤害勾销

### 云铮 / 战斗人物!72:3

- 当前判断：`字` / 名称：`【激烈暴躁，冲动易怒】`
- 标记：`implicit_word, exclusive_word`
- 原文：【激烈暴躁，冲动易怒】：受攻击及不利效果1/6直接放一大招（目标一定包含影响他的人），每曾有一人影响过概率上升1/6；强制出战

### 朱藻 / 战斗人物!73:4

- 当前判断：`字` / 名称：`麻衣客`
- 标记：`implicit_word`
- 原文：麻衣客：对阵战斗每张卡与某敌结算结果（平、克、被克）不全相同则可以与该敌立刻额外战斗一回合

### 朱藻 / 战斗人物!73:5

- 当前判断：`字` / 名称：`小皇子`
- 标记：`implicit_word`
- 原文：小皇子：对阵（回合）或非对阵（单次）可以伤害倒置

### 朱藻 / 战斗人物!73:6

- 当前判断：`字` / 名称：`武林鬼才`
- 标记：`implicit_word`
- 原文：武林鬼才：可见的特技自身均额外拥有一份，视为-- （100*特技名字字数）的大招（种类随意选择，不能更改；不是学会，无视专属或人物特征，不相关，包含在此特技中，使用一次后从此特技中抹去）；可以耗费一轮将一个此特技中的大招教给另一人物（无视专属特征，可以教给麾下仙女），从此特技中抹去，学会的人物使用该特技不用抹去

### 雷大鹏 / 战斗人物!74:3

- 当前判断：`字` / 名称：`【雷鞭落星雨】`
- 标记：`implicit_word, exclusive_word`
- 原文：【雷鞭落星雨】：照面敌麻，攻击附麻；自身每两次击中敌中间受到的伤害将作为伤害加深累积到第二击中（触发时才算做使用，身份）

- 仅显示前 80 条，完整列表见 `data/cards_current/abilities.jsonl`。

## 带【】的字

- 数量：254

### 丁鹏 / 战斗人物!1:4

- 当前判断：`字` / 名称：`【魔刀】`
- 标记：`implicit_word, exclusive_word`
- 原文：【魔刀】：己造成的任意伤害最终不低于本局已知最高单项伤害

### 高渐飞 / 战斗人物!2:3

- 当前判断：`字` / 名称：`【泪痕剑主人】`
- 标记：`implicit_word, exclusive_word`
- 原文：【泪痕剑主人】：杀死萧大师之子则不算做输

### 哥舒天 / 战斗人物!5:3

- 当前判断：`字` / 名称：`【逍遥侯】`
- 标记：`implicit_word, exclusive_word`
- 原文：【逍遥侯】：每杀死一人，则玩偶山庄容量+1

### 连城璧 / 战斗人物!6:2

- 当前判断：`字` / 名称：`【侠义双无】`
- 标记：`implicit_word, exclusive_word`
- 原文：【侠义双无】：舍弃掉侠义无双并令一非【恶】死亡，且视为另一人物所为（身份）；不可杀天宗中人

### 萧十一郎 / 战斗人物!7:3

- 当前判断：`字` / 名称：`【人心怜羊，狼心独怆】`
- 标记：`implicit_word, exclusive_word`
- 原文：【人心怜羊，狼心独怆】：萧十一郎陷入单挑时视为敌先挑战；萧十一郎不中无法闪避、抵挡、一定造成、破

### 柴玉关 / 战斗人物!8:6

- 当前判断：`字` / 名称：`【万家生佛】`
- 标记：`implicit_word, exclusive_word`
- 原文：【万家生佛】：废牌中随机抽10张，学会其中的招式及武功；视为包含在此特技内的不可见的（可被响应）能力，失去此特技则习得的亦失去（博）

### 白飞飞 / 战斗人物!12:6

- 当前判断：`字` / 名称：`【孤身远引，至死不见】`
- 标记：`implicit_word, exclusive_word`
- 原文：【孤身远引，至死不见】：陷入单挑且对方为男子则离场（不算做胜利）

### 傅红雪 / 战斗人物!13:5

- 当前判断：`字` / 名称：`【复仇之神】`
- 标记：`implicit_word, exclusive_word`
- 原文：【复仇之神】（身份）：可与人死战；开场可暗中指定一个仇敌，可以暗中将杀死队友者认为仇敌；有仇敌时则出战先选择仇敌死战，有仇敌则自身在非复仇过程中不会因非仇敌的攻击/效果而死亡/离场（强制留1血，不会被一定造成，破杀死）；杀死仇敌则自身回满（即使当回合傅红雪死亡）

### 宫锦弼 / 战斗人物!18:2

- 当前判断：`字` / 名称：`【孙女】`
- 标记：`implicit_word, exclusive_word`
- 原文：【孙女】：第一次杀死人或濒死，视为杀死了孙女，自身生命回满，并暴怒，此后伤害一定造成；致其孙女死亡者（被其杀死或导致宫锦弼濒死）下局少抓一卡

### 蓝天鎚 / 战斗人物!19:2

- 当前判断：`字` / 名称：`【天鎚道人】`
- 标记：`implicit_word, exclusive_word`
- 原文：【天鎚道人】：敌五行或基础卡与蓝大相同时-300；按照基础卡位置计算，若敌在某一位置受伤≥300，则该位置基础卡发生爆炸；爆炸使敌额外-300，同时永久失去该位置的基础卡；爆炸会波及起前后各一位的基础卡，使敌在该两位置再-200；爆炸伤害一定造成

### 展梦白 / 战斗人物!20:2

- 当前判断：`字` / 名称：`【怒】`
- 标记：`implicit_word, exclusive_word`
- 原文：【怒】：受他人相关效果/有被禁制、看不见趋势/对阵【恶】时怒，与之死战，1/3对象错误，在其余人中随机选择；死战中自身乱放且不重新计算怒，回合结束时1/3清醒死战停止；死战错误两次后于清醒时自杀

### 狄青麟 / 战斗人物!22:3

- 当前判断：`字` / 名称：`【侯门深似海】`
- 标记：`implicit_word, exclusive_word`
- 原文：【侯门深似海】：受到非基础卡伤害或受效果则来源敌死亡

### 萧少英 / 战斗人物!24:3

- 当前判断：`字` / 名称：`【复仇】`
- 标记：`implicit_word, exclusive_word`
- 原文：【复仇】：队友彻底死亡时，可投入杀死队友一方伺机复仇（与一或多敌死战，生命拉至相同水平，共享不利）；杀死敌自身刷满返回；敌不能派遣萧少英出战（可主动出战）；无论最终萧少英复仇终结后在何方，均为控制方胜利

### 柳长街 / 战斗人物!26:2

- 当前判断：`字` / 名称：`【世上的英雄豪杰却已太多了】`
- 标记：`implicit_word, exclusive_word`
- 原文：【世上的英雄豪杰却已太多了】：得知本局所有人物身份的6回合后离去

### 凤三 / 战斗人物!27:2

- 当前判断：`字` / 名称：`【垂天大星江南凤，凤鸣千里天地动】`
- 标记：`implicit_word, exclusive_word`
- 原文：【垂天大星江南凤，凤鸣千里天地动】：非凤三阵营人物与己阵营人物对阵时，输出若不比该人物上回合输出高则攻击与不利效果无效，凤三阵营人物与敌方对阵时，输出至少高出上回合100（如果无法高出，则造成差额的流失，如果无法流失则算作悖论）；一局中如出现悖论、无限循环、卡住导致和局，则相关卡片（除凤三）被扔出游戏不能响应

### 俞佩玉 / 战斗人物!28:4

- 当前判断：`字` / 名称：`【疤痕】`
- 标记：`implicit_word, exclusive_word`
- 原文：【疤痕】：同时拥有假身份俞佩玉，侧面伤害以及全部不利相关效果作用于假身份，正面受伤则己与假身份均承受；当假身份死亡时，假身份以己生命上限重生，当本体死亡时如本体与假身份血量不同（回合中按照回克开始时的血量计算），则本体以己生命上限重生；假身份重生一次后才具有阎王债

### 俞佩玉 / 战斗人物!28:5

- 当前判断：`字` / 名称：`【温柔敦厚】`
- 标记：`implicit_word, exclusive_word`
- 原文：【温柔敦厚】：可使任何特技可控（无视阎王债）

### 宫九 / 战斗人物!29:1

- 当前判断：`字` / 名称：`【自虐】`
- 标记：`implicit_word, exclusive_word`
- 原文：【自虐】：受到攻击视为加血，不利状态转化为当前生命加倍；每三回合结束时取出自身所有生命，并使敌自减该值1/4的伤害，此时生命为0，直至下次回合结束前不会因为生命为0死亡（第一次出场前视为宫九刚刚自虐完）（身份）

### 宫九 / 战斗人物!29:2

- 当前判断：`字` / 名称：`【太平王世子】`
- 标记：`implicit_word, exclusive_word`
- 原文：【太平王世子】：宫九未翻开前可不与人交手，使用此特技不必翻开

### 公孙大娘 / 战斗人物!30:4

- 当前判断：`字` / 名称：`【红鞋子】`
- 标记：`implicit_word, exclusive_word`
- 原文：【红鞋子】：公孙大娘可获得场上女子加入己方，加入的战斗人物角色仍由原玩家控制，若存活至结束可比公孙大娘低一顺位结盟

### 花满楼 / 战斗人物!31:5

- 当前判断：`字` / 名称：`【花满楼】`
- 标记：`implicit_word, exclusive_word`
- 原文：【花满楼】：双方战斗伤害可取最小值；与人永远不相关

### 金九龄 / 战斗人物!32:2

- 当前判断：`字` / 名称：`【绣花大盗】`
- 标记：`implicit_word, exclusive_word`
- 原文：【绣花大盗】：可以绣花大盗出战/切入；自身一切不中；大盗时克敌敌立即瞎，全未被克敌回合后瞎；瞎攻击50%落空，瞎时特技尽可能对对阵者使用，回合内未使用特技一条-300；对瞎无敌（陆小凤识破）；以绣花大盗出场后需要至少以总捕出场一次后才能再次以绣花大盗身份出场

### 陆小凤 / 战斗人物!34:3

- 当前判断：`字` / 名称：`【四条眉毛】`
- 标记：`implicit_word, exclusive_word`
- 原文：【四条眉毛】：可主动将被灵犀一指夹住的兵器还回，如敌同意，则己获得一次与之避战的机会；可将自身从针对多个目标且包含自己的伤害/效果中移除（身份）

### 木道人 / 战斗人物!35:3

- 当前判断：`字` / 名称：`【幽灵山庄】`
- 标记：`implicit_word, exclusive_word`
- 原文：【幽灵山庄】：木道人可允许一人物加入山庄，永久隐藏身份，去除不利状态；在山庄中人物可与其结盟胜利（顺位低），木道人须指定一敌对人物为其目标，该人物杀死木道人指定的目标会提高在山庄中的顺位（与木道人持平）；队友起始可认定为已加入山庄，木道人死后幽灵山庄解散

### 叶孤城 / 战斗人物!38:4

- 当前判断：`字` / 名称：`【白云城主】`
- 标记：`implicit_word, exclusive_word`
- 原文：【白云城主】：每使用一特技，己全攻击+200（单回合计算，本特技不计算在内）

### 黑蜘蛛 / 战斗人物!40:3

- 当前判断：`字` / 名称：`【黑大哥】`
- 标记：`implicit_word, exclusive_word`
- 原文：【黑大哥】：叫其大哥则不切入攻击该人也不对其使用银丝飞蛛，但此后对其不愿使用任何不利

### 花无缺 / 战斗人物!41:4

- 当前判断：`字` / 名称：`【无缺公子】`
- 标记：`implicit_word, exclusive_word`
- 原文：【无缺公子】：可在己未参与的战斗中替他人承担所有不利，如该不利既可造成原承受者死亡亦可造成花无缺死亡，则双方结盟，以花无缺为主

### 江别鹤 / 战斗人物!42:2

- 当前判断：`字` / 名称：`【江南大侠】`
- 标记：`implicit_word, exclusive_word`
- 原文：【江南大侠】：相克不减血，接下大招，与人交手后算作相结交（直接结交队友，不需翻开）；隐去【恶】

### 江小鱼 / 战斗人物!43:4

- 当前判断：`字` / 名称：`【小鱼儿】`
- 标记：`implicit_word, exclusive_word`
- 原文：【小鱼儿】：对阵多人时，敌对江小鱼的攻击仅有1/n机会命中（n为对阵的人数）；不中狂、乱、迟、封、混、禁制以及等同于这些异常的效果；不中流失（身份）

### 叶开 / 战斗人物!49:4

- 当前判断：`字` / 名称：`【树叶的叶，开心的开】`
- 标记：`implicit_word, exclusive_word`
- 原文：【树叶的叶，开心的开】：每上场一次多一次小李飞刀，起始一次；小李飞刀不能替【恶】抵挡致命或打断针对【恶】的特技

### 芮伟 / 战斗人物!50:2

- 当前判断：`字` / 名称：`【大悲剧】`
- 标记：`implicit_word, exclusive_word`
- 原文：【大悲剧】：对芮伟来说看不见的人不存在于本局游戏；弃掉的芮伟无法找回

### 欢乐英雄 / 战斗人物!54:5

- 当前判断：`字` / 名称：`【欢乐英雄】`
- 标记：`author_corrected, exclusive_word, implicit_word, unit_specific_ability`
- 原文：【欢乐英雄】：出战可更换人物，一人死亡时若其他三人存活，则该人重生，其余三人各-300

### 千手书生 / 战斗人物!56:3

- 当前判断：`字` / 名称：`【千手书生】`
- 标记：`author_corrected, exclusive_word, implicit_word, unit_specific_ability`
- 原文：【千手书生】：如打得好，断敌一手，使敌失去攻防加成，随机失去两张基础战斗卡，-300/轮；如敌已被己断一手，且再打得好，可再断之一手，使敌失去攻防能力，再随机失去三张基础战斗卡，多-400/轮

### 李坏 / 战斗人物!58:3

- 当前判断：`字` / 名称：`【飞刀，又见飞刀】`
- 标记：`implicit_word, exclusive_word`
- 原文：【飞刀，又见飞刀】：第一次放出小李飞刀对方死亡；可宣布与一人决战使两人消失

### 月神 / 战斗人物!59:2

- 当前判断：`字` / 名称：`【月神】`
- 标记：`implicit_word, exclusive_word`
- 原文：【月神】：出战时可点名挑战，若如此做则该战斗无他人在场（点名须叫出对手名字，对于未亮出，未在场者有效）

### 郭嵩阳 / 战斗人物!62:2

- 当前判断：`字` / 名称：`【舍生取义】`
- 标记：`implicit_word, exclusive_word`
- 原文：【舍生取义】：可要求与某人比武，此战中该人尽量对郭嵩阳不利，使用过的特技、物品对郭指定的人不再有效

### 荆无命 / 战斗人物!63:2

- 当前判断：`字` / 名称：`【右手的秘密】`
- 标记：`implicit_word, exclusive_word`
- 原文：【右手的秘密】：有濒死趋势则附加【残】，生命为0，失去左手剑，抵御死亡，如在战斗中则中止战斗，直至下次受到伤害则死亡；期间每回合攻击视为攻击次数不变，总伤害为所有单项伤害之积的攻击，至少一次攻击命中则可造成总伤害，且后发先至，不可闪避，转（剑）

### 上官金虹 / 战斗人物!66:3

- 当前判断：`字` / 名称：`【金钱帮主】`
- 标记：`implicit_word, exclusive_word`
- 原文：【金钱帮主】：可将招式和对阵敌内功整体互换；可支付1500收买一恶人；不上场一轮则金钱+300

### 花双霜 / 战斗人物!67:3

- 当前判断：`字` / 名称：`【忆女成狂】`
- 标记：`implicit_word, exclusive_word`
- 原文：【忆女成狂】：非大旗英雄传美丽女性可认母（至多一女）；不分敌我攻击全体，不攻击女儿

### 飧毒大师 / 战斗人物!69:7

- 当前判断：`字` / 名称：`【毒神现体】`
- 标记：`implicit_word, exclusive_word`
- 原文：【毒神现体】：被飧毒大师杀死、毒死者化为毒神：生命2000，不中普攻、异常，毒神战斗全为招式，攻击附毒

### 云铮 / 战斗人物!72:3

- 当前判断：`字` / 名称：`【激烈暴躁，冲动易怒】`
- 标记：`implicit_word, exclusive_word`
- 原文：【激烈暴躁，冲动易怒】：受攻击及不利效果1/6直接放一大招（目标一定包含影响他的人），每曾有一人影响过概率上升1/6；强制出战

### 雷大鹏 / 战斗人物!74:3

- 当前判断：`字` / 名称：`【雷鞭落星雨】`
- 标记：`implicit_word, exclusive_word`
- 原文：【雷鞭落星雨】：照面敌麻，攻击附麻；自身每两次击中敌中间受到的伤害将作为伤害加深累积到第二击中（触发时才算做使用，身份）

### 卓三娘 / 战斗人物!76:2

- 当前判断：`字` / 名称：`【闪电卓三娘】`
- 标记：`implicit_word, exclusive_word`
- 原文：【闪电卓三娘】：每回合可放一空；自身每放一次空则可对一敌造成一次不可闪避的攻击，攻击力为自身放过的空*100 ；自身未对阵则场上的空可视为自身所放

### 班察巴那 / 战斗人物!78:4

- 当前判断：`字` / 名称：`【五花箭神】`
- 标记：`implicit_word, exclusive_word`
- 原文：【五花箭神】：受到攻击可由队友承担，不出战则不在场

### 小方 / 战斗人物!80:2

- 当前判断：`字` / 名称：`【想江南】`
- 标记：`implicit_word, exclusive_word`
- 原文：【想江南】：开局暗中指定一人物；如其死亡且所在方获胜，则小方也获胜；如其未死，则小方可低之一位获胜

### 楚留香 / 战斗人物!81:5

- 当前判断：`字` / 名称：`【红颜】`
- 标记：`author_confirmed_structure, exclusive_word, implicit_word, nested_indented_line, nested_named_line`
- 原文：【红颜】：苏蓉蓉：可揭破易容，可为己解除毒与毒药 李红袖：识破对阵敌身份，场上使用特技必须要翻出（不相关） 宋甜儿：对己使用语言类特技无效且敌惊（身份）

### 胡铁花 / 战斗人物!82:3

- 当前判断：`字` / 名称：`【潇湘侠盗】`
- 标记：`implicit_word, exclusive_word`
- 原文：【潇湘侠盗】：可选择偷走对阵一人物一件物品或一兵器或一张基础卡，如该人非【恶】则需在己与之作战一回合后归还（对每一人物限一次）

### 胡铁花 / 战斗人物!82:4

- 当前判断：`字` / 名称：`【花蝴蝶】`
- 标记：`implicit_word, exclusive_word`
- 原文：【花蝴蝶】：侧面受到效果可重新投掷2骰子，所组成数字×100成为自身血量（同时改变上限）

### 无花 / 战斗人物!84:3

- 当前判断：`字` / 名称：`【妙僧】`
- 标记：`implicit_word, exclusive_word`
- 原文：【妙僧】：各条命各有一次无敌至下次与人交手前的机会，无敌后可于任意时刻与某敌交手一合，视为上回合释放过迎风一刀斩

### 薛笑人 / 战斗人物!85:2

- 当前判断：`字` / 名称：`【杀手集团】`
- 标记：`implicit_word, exclusive_word`
- 原文：【杀手集团】：每以薛宝宝出战一回合薛笑人手下多一刺客，可派出刺客袭击某个与薛宝宝交手者一回合（非正常战斗）；刺客无生命，具有招式“快剑：战斗结束时敌-n×100，n为刺客出场次数（不同刺客共同计算）”

### 阴姬 / 战斗人物!86:4

- 当前判断：`字` / 名称：`【水母】`
- 标记：`implicit_word, exclusive_word`
- 原文：【水母】：回合开始先吸与一人水差*100（身份）

### 中原一点红 / 战斗人物!88:4

- 当前判断：`字` / 名称：`【若求杀人手，但寻一点红】`
- 标记：`implicit_word, exclusive_word`
- 原文：【若求杀人手，但寻一点红】：随时可暗中指定一人为杀人目标，目标死后才能指定新目标，对目标实际伤害加倍；目标被他人杀死时快剑系数+200，亲手杀死目标时快剑系数+400，生命回满；濒死时与目标战斗一回合，此回合结束前自身不会死亡且能通过杀死目标回满

### 赵无忌 / 战斗人物!91:3

- 当前判断：`字` / 名称：`【结】`
- 标记：`implicit_word, exclusive_word`
- 原文：【结】：出场在生命某数字间隔中添上一个数字，下次出场在非首尾数字中去掉一个（身份）

### 曹秋道 / 战斗人物!93:2

- 当前判断：`字` / 名称：`【剑圣】`
- 标记：`implicit_word, exclusive_word`
- 原文：【剑圣】：曹秋道可宣布与一敌人决战（含白猿）（基础一次，每决战外出战一次则多一次），决战无他人，双方暂时去除不利状态且全部特技失灵（敌方也去除有利状态），进行n+1回合战斗；若决战中杀死对方则攻+300，曹秋道回100*n于决战后；一切涉及曹秋道的非正常战斗与单挑都会变化为决战

### 法明 / 战斗人物!95:3

- 当前判断：`字` / 名称：`【僧王】`
- 标记：`implicit_word, exclusive_word`
- 原文：【僧王】：所有非恶佛门与其结盟，有人非死亡离场则法明此后不在场且不出战

### 蒙赤行 / 战斗人物!99:1

- 当前判断：`字` / 名称：`【第六感】`
- 标记：`implicit_word, exclusive_word`
- 原文：【第六感】：敌延迟放卡、机械技术无效；于战斗开始前预知敌未用卡

### 蒙赤行 / 战斗人物!99:2

- 当前判断：`字` / 名称：`【第七感】`
- 标记：`implicit_word, exclusive_word`
- 原文：【第七感】：与战斗开始前预知敌某五行位置

### 蒙赤行 / 战斗人物!99:3

- 当前判断：`字` / 名称：`【精神物质化】`
- 标记：`implicit_word, exclusive_word`
- 原文：【精神物质化】：与战斗开始前预测敌放卡，正确敌流失400且该卡被克；当收到侧面伤害或侧面不利效果，可化为自流400，且该特技算生效

### 蒙赤行 / 战斗人物!99:4

- 当前判断：`字` / 名称：`【魔宗】`
- 标记：`implicit_word, exclusive_word`
- 原文：【魔宗】：特技收放自如，可将组成自身血量的数字重排一次

### 范良极 / 战斗人物!104:5

- 当前判断：`字` / 名称：`【独行盗】`
- 标记：`implicit_word, exclusive_word`
- 原文：【独行盗】：交手后偷走敌一特技，一回合后归还，偷来的消耗技被己使用过还回不计算损耗

### 赤尊信 / 战斗人物!105:1

- 当前判断：`字` / 名称：`【盗霸】`
- 标记：`author_confirmed_structure, author_corrected, exclusive_word, implicit_word`
- 原文：【盗霸】：每张自由切换武器，回合中每出现一种武器攻击倍数+1，不能连用同一武器；兵器物品与此特技共同作用（博） 剑：本张禁敌闪避，下张兵器效果*2 刀：本张破防，下张抢先攻击 枪：本回合攻击倍数+1 弓：本张无攻击力，非对阵一人-500 棍杖：本张处抵挡一不利效果（包括本张结束处施放的特技）；受攻击反击300 奇门（不享受剑*2）：本张封敌一特技（异常），下...

### 方夜羽 / 战斗人物!107:3

- 当前判断：`字` / 名称：`【黄金家族后裔】`
- 标记：`implicit_word, exclusive_word`
- 原文：【黄金家族后裔】：每次出战后从本局弃牌中找回一张非汉族人物卡，本方除自己外每有一非汉族人自攻防各+100（身份）

### 韩柏 / 战斗人物!110:3

- 当前判断：`字` / 名称：`【赤尊信元神】`
- 标记：`implicit_word, exclusive_word`
- 原文：【赤尊信元神】：武器物品无负面效果，无视敌武器物品（博）

### 厉若海 / 战斗人物!114:7

- 当前判断：`字` / 名称：`【邪灵】`
- 标记：`implicit_word, exclusive_word`
- 原文：【邪灵】：可一次性令他人攻+500；不会从属他人，不会改换阵营，不会被人控制；男女关系类效果对自身无效

### 烈震北 / 战斗人物!115:3

- 当前判断：`字` / 名称：`【回光返照】`
- 标记：`implicit_word, exclusive_word`
- 原文：【回光返照】：生命<=1800 自动开启，之后三回合内受伤全为加血；可自己主动使用，至下回合结束前受伤视为加血（一次性）

### 年怜丹 / 战斗人物!116:4

- 当前判断：`字` / 名称：`【花仙】`
- 标记：`implicit_word, exclusive_word`
- 原文：【花仙】：杀死一女子则生命状态刷满，且玄铁剑中数字全部加倍；场上女子死亡年怜丹总视为自己杀死

### 乾罗 / 战斗人物!119:3

- 当前判断：`字` / 名称：`【毒手乾罗】`
- 标记：`implicit_word, exclusive_word`
- 原文：【毒手乾罗】：正常回合结束后可再行动一回合，与任意处任意敌战斗，此回合该敌无攻击力；有受到侧面伤害的趋势时，可以使用乾罗的矛抵挡或反击

### 鹰缘 / 战斗人物!123:2

- 当前判断：`字` / 名称：`【鹰刀】`
- 标记：`implicit_word, exclusive_word`
- 原文：【鹰刀】：自带鹰刀，可将之给予他人（自己不使用鹰刀）

### 鹰缘 / 战斗人物!123:3

- 当前判断：`字` / 名称：`【活佛】`
- 标记：`implicit_word, exclusive_word`
- 原文：【活佛】：自身或他人出现非死亡离场，鹰缘飞升

### 杜伏威 / 战斗人物!128:2

- 当前判断：`字` / 名称：`【江淮军总管】`
- 标记：`implicit_word, exclusive_word`
- 原文：【江淮军总管】：有一次袭击某人，战斗结束后无敌至下次出场的机会；有一次无敌并立即袭击某人的机会

### 傅采林 / 战斗人物!129:3

- 当前判断：`字` / 名称：`【弈剑大师】`
- 标记：`implicit_word, exclusive_word`
- 原文：【弈剑大师】：每张战斗卡翻开前，规定敌放卡（除第一张外）与上张需满足生/克关系，如不满足算作被己克；延迟放卡；可禁止场上倒置伤害，转移攻击，动卡，避战

### 寇仲 / 战斗人物!132:5

- 当前判断：`字` / 名称：`【少帅】`
- 标记：`implicit_word, exclusive_word`
- 原文：【少帅】：一局中累计损失生命＞1000，攻*2，＞2000，攻*4；濒死反击井中八法

### 曲傲 / 战斗人物!137:4

- 当前判断：`字` / 名称：`【铁勒飞鹰】`
- 标记：`implicit_word, exclusive_word`
- 原文：【铁勒飞鹰】：第一次出战前不在场，曲傲的凝真九变伤害上限锁定为999

### 师妃暄 / 战斗人物!138:3

- 当前判断：`字` / 名称：`【静斋传人】`
- 标记：`implicit_word, exclusive_word`
- 原文：【静斋传人】：非对阵不在场；每出战一回合可请人替己作战一次

### 宋缺 / 战斗人物!140:5

- 当前判断：`字` / 名称：`【宋阀之主】`
- 标记：`implicit_word, exclusive_word`
- 原文：【宋阀之主】：非对阵影响宋缺的不利化为一次其他人物均不知的战斗

### 席应 / 战斗人物!142:2

- 当前判断：`字` / 名称：`【天君】`
- 标记：`implicit_word, exclusive_word`
- 原文：【天君】：席应第一次出场前在西域

### 杨虚彦 / 战斗人物!145:5

- 当前判断：`字` / 名称：`【影子剑客】`
- 标记：`implicit_word, exclusive_word`
- 原文：【影子剑客】：基础1影，克敌及杀人+1；可消耗一个影子攻击一敌，造成无法响应的（影子数+1）*100伤害，若自未出战可选择与目标立刻战斗一回合，此回合影子累积数*2（对某战斗中敌发动将直接切入攻击之，战斗剩余卡）

### 赵德言 / 战斗人物!147:6

- 当前判断：`字` / 名称：`【魔帅】`
- 标记：`implicit_word, exclusive_word`
- 原文：【魔帅】：起始不在场；有一回合归魂十八爪具有全部姿态的机会；

### 任遥 / 战斗人物!153:3

- 当前判断：`字` / 名称：`【逍遥帝君】`
- 标记：`implicit_word, exclusive_word`
- 原文：【逍遥帝君】：结盟时如顺位较低则立即破除盟约（身份）

### 孙恩 / 战斗人物!154:3

- 当前判断：`字` / 名称：`【天师】`
- 标记：`implicit_word, exclusive_word`
- 原文：【天师】：生命小于孙恩者无法禁制孙恩；孙恩的一回合中出现了全部八种基础战斗卡则孙恩可破空飞去

- 仅显示前 80 条，完整列表见 `data/cards_current/abilities.jsonl`。

## 有类型前缀但未识别出特技名

- 数量：0

## 说明性文本块

- 数量：148

### 薛笑人 / 战斗人物!85:3

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：薛宝宝 拥有一生命为1800的假身份薛宝宝；以此身份出现时，不使用杀手剑，任何人不愿对其使用特技；薛笑人可切入追杀曾与薛宝宝交手之人；不出场时默认为薛宝宝

### 光神 / 战斗人物!102:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：开局分发除光神外人物个数张基础卡，作为生命能，事先暗中指定其中一卡结果，作为光神要求的生命能标准；找到该人物后，光神携带之飞往宇宙的倾斜，光神与之列为前两位胜利者；如果凌渡宇存在，则凌渡宇为选中者，但凌渡宇一定拒绝光神的邀请，光神独自离开，不作为胜利者

### 光神 / 战斗人物!102:2

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：光神起始得知己方人物的生命能卡；当一人物彻底死亡时，光神可以查看该人物的生命能卡，如果符合，则清除其死亡来源一方所有卡片，然后离开；

### 光神 / 战斗人物!102:3

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：光神具有光能，每在场下一轮，光能+100；光神可以消耗300光能来查看一个目标的生命能卡片；光神可以消耗100光能，使一人物一刹那不存在在任何一个地方

### 光神 / 战斗人物!102:4

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：光神上场战斗，则敌生命及上限因衰老减少100，衰老无法用任何方式避免（对不中效果，无敌等均有效）

### 光神 / 战斗人物!102:5

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：光神10轮未找到生命能达标者则离开，此卡不会受到任何其他卡片的效果、机制的影响

### 葵花老祖 / 战斗人物!194:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：欲练此功，必先自宫 由葵花宝典习得的特技视为身份技

### 丁春秋 / 战斗人物!208:7

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：虚竹可对其直接施放生死符

### 五个人头 / 战斗人物!318:6

- 当前判断：`说明` / 名称：`—`
- 标记：`author_corrected, free_text, unit_specific_ability`
- 原文：：场上所有无名“字”

### 唐老太太 / 战斗人物!387:6

- 当前判断：`字` / 名称：`【唐门六识】`
- 标记：`exclusive_word, free_text, implicit_word, nested_continuation_line`
- 原文：【唐门六识】：唐老太太死亡或离场时生命不为0，则诅咒引发自己死亡/离场之人；被诅咒者陷于唐门地下，不能影响本局游戏直至： 1. 场上所有队友全部非【恶】； 2. 某一回合中总输出≥4000； 3. 有至少2人因为此输出死亡； 则该人物解脱；若被诅咒者至本局结束未能解脱，则顺位低于唐老太太方

### 四大恶人 / 战斗人物!418:1

- 当前判断：`说明` / 名称：`—`
- 标记：`author_corrected, free_text, nested_continuation_line, unit_specific_ability`
- 原文：四大恶人可以同时出战任意多个，同时攻击；起始不需要声明哪个恶人出战，直至本卡翻开

### 石中玉 / 战斗人物!419:1

- 当前判断：`说明` / 名称：`—`
- 标记：`author_corrected, free_text, nested_continuation_line, unit_specific_ability`
- 原文：本方遗失一件物品，一个附加人物，一人物的一张基础卡牌，一个人物的一个特技失灵（均视为针对玩家的效果，不能选择石中玉或石清、闵柔自身的牌或特技） 玩家可以在石中玉不出战的一轮中选择己方某人物杀死石中玉或进行判定：1/2 石中玉逃走到另一方（石中玉不会重复逃回已经待过的一方），1/2无效 杀死石中玉则石清闵柔与其死战，石中玉被迫出战时则可以请石清闵柔出战一回合（...

### 龟孙子大老爷 / 附加人物!1:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：不需要附加在战斗人物之上

### 割头小鬼 / 附加人物!7:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：不需要附加在战斗人物之上

### 割头小鬼 / 附加人物!7:2

- 当前判断：`字` / 名称：`割头`
- 标记：`free_text, implicit_word, nested_continuation_line`
- 原文：割头：无视是否在场，观察一切战斗；若战斗中满足“攻击/伤害/效果作用于一等血量白人身上会致死”，则割头使该攻击/伤害/效果一定造成无视防御。 若某人在他人眼中死亡（可以为假死），割头使其真正死亡且无法复活；此效果无视防御，无法响应

### 阿朱 / 附加人物!9:2

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：易容无视性别但考虑特征

### 花铁干 / 附加人物!10:3

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：持有者强制上场

### 程英 / 附加人物!11:3

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：选人阶段时可选择一已出现过的场景

### 王语嫣 / 附加人物!13:3

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：与慕容复，慕容惜花结盟

### 无名老僧 / 附加人物!15:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：不需要附加在战斗人物之上

### 喀丝丽 / 附加人物!16:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：造成附加此卡者死亡的人物掳走此卡

### 胡青牛王难姑 / 附加人物!20:7

- 当前判断：`字` / 名称：`【毒仙】`
- 标记：`author_corrected, exclusive_word, free_text, implicit_word, nested_continuation_line, unit_specific_ability`
- 原文：【毒仙】：轮到本方行动时，给一人物下毒（可对己阵营使用），使之随机选择： 毒200（逼毒只能免除一次判定不能根治）， 毒掉一个字（王难姑选择毒掉哪个字）， 无攻击能力一转轮， 无法响应一转轮， 不对除自己外明教人物使用

### 计晓军 / 附加人物!24:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：不需要附加在战斗人物之上 开始时可亮出，当满足惩罚条件时则必须亮出

### 计晓军 / 附加人物!24:3

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：改变基础战斗方式使用后流失100/张，再用多流失100/次（四张起）

### 计晓军 / 附加人物!24:4

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：代替他人战斗，累进流失2次

### 计晓军 / 附加人物!24:5

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：此卡一定能用出（同场景） 流失一定会造成，且同时针对上限

### 张磊 / 附加人物!26:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：自输出与受伤*2，攻击全体化，转

### 张磊 / 附加人物!26:4

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：将十大恶人锁定为杜杀，自身杠杀失效

### 张愚 / 附加人物!27:11

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：顶替掉五个人头，疯张愚

### 江玉郎 / 附加人物!30:4

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：与江别鹤结盟；特技对江小鱼无效，江小鱼可以识破其虚假结果

### 金蚕蛊毒 / 物品!1:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：不需要人物持有，需要人物使用 直接杀死对阵一敌（含多人一卡）；使用后下局己少抓一卡；杀死为彻底杀死，满血者可将此毒逼出；对避毒者无效

### 子露风疸 / 物品!2:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：不需要人物持有，需要人物使用 中者每回合-已用特技数*300，若全部特技均用过或无特技则立即死亡

### 百病百疼催生丸 / 物品!3:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：不需要人物持有，需要人物使用 使一未出战者失去响应能力，苏樱可解除

### 三尸脑神丹 / 物品!4:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：不需要人物持有，需要人物使用 一次性，可在他人同意情况下令其服下，并从属于本方

### 续命八丸 / 物品!5:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：开局使用，使用者为玩家 生命最高两位补齐

### 生生造化丹 / 物品!6:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：不需要人物持有，使用者为作用对象本人 战斗开始前或场下可给某人服用，若该人在下一个回合结束前死亡则重生

### 金坷垃 / 物品!7:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：不需要人物持有，使用者为作用对象本人 使自身一特技在一回合/一次中发挥至可能的地步；此物品不能被制作，找回，复制，模拟，多次使用等

### 极乐丸 / 物品!8:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：自-1基础卡强制令一人服用，不可自服，使用此宝物则附【恶】（仅有一次）

### 极乐丸 / 物品!8:2

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：该人服后首轮恢复手卡，伤害一定造成，不受禁制，第2，3轮手卡随机减2，特技随机减1，生命减上限10%（再服时轮数重新计算） 该人在123轮中可选择屈服，再服食极乐丸不消耗手卡（但失去的特技不恢复）；屈服者不与极乐丸主人交手亦不对主人不利，失去人物关系，主人可令其代己出战，如果服食者一方仅剩自己，则算做从属于主人

### 阴阳和合散 / 物品!9:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：可以开场使用，对一至两方至多不同两人使用，视为由玩家使用 之后可以由一人物持有，对场上一人物使用

### 阴阳和合散 / 物品!9:3

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：有毒药和春药两效果，避毒和免疫异常者不中毒药效果

### 百日十龙丸 / 物品!10:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：不需要人物持有，需要人物使用 生命+1500 攻*4 大招攻+400 此后每回合生命（上限）-500 对避毒无效 可给他人服用 方歌吟食之不减血

### 三日必死丸 / 物品!11:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：不需要人物持有，需要人物使用 随时可以服用；服下后去除全部不利，接下来三回合结束前不会死亡，结束时立即彻底死亡（无法通过任何方式抵挡）

### 逆乾坤 / 物品!12:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：不需要人物持有，使用者为作用对象本人 生命到0后重生，攻+400，生命上限-2000；重生后药效仍在，直至生命上限为0后彻底死亡

### 豹胎易筋丸*2 / 物品!13:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：抓卡后开局使用，使用者为玩家 使一人物生命最高两位互换 其中有一枚需先对非己方使用 不能两枚给同一人

### 豹胎易筋丸*2 / 物品!13:5

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：洪安通收走之并可控制生效时机

### 战鹰 / 物品!14:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：不需要持有，需要人物使用，对不在场者有效 按某路径依次刺探其他玩家人物卡身份，算作相关，受攻击死亡，成功回到原主手中时带回情报

### 圣帝舍利 / 物品!15:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：必须选择人物持有之；

### 圣帝舍利 / 物品!15:2

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：当持有者使用大招/被大招攻击时，舍利由持有者/攻击者开启，使用的大招视为注入舍利；舍利开启时持有者若在战斗中则立刻终止当前战斗 舍利开启后持有者连续3次回合失去响应能力、迟混、自身基础卡结算为空，且每回合开始前先受到注入舍利中的随机一大招攻击；此时攻击持有者亦会受到舍利中随机一大招攻击（可选择不攻击）；3回合后若持有者仍存活则视为成功吸收舍利内元精，自身状态...

### 圣帝舍利 / 物品!15:4

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：若一局游戏中无人成功开启舍利，则由本局游戏的胜者决定舍利是否留至下一局以及下一局舍利的归属

### 圣帝舍利 / 物品!15:5

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：双龙持有舍利可选择直接开启，且直接成功吸收元精；石之轩抢来舍利一轮后直接吸收元精，使自身卡上所有数字翻倍且自身同时具有邪王及落魄文士的正面效果（不具有“自身状态刷满且可将自身一特技发挥至任意层次”）；鲁妙子直接收来舍利，自身不使用但可给予他人；向雨田直接收来舍利并成功吸收元精，自身习得当前舍利中所有大招（习得大招不会因为道心种魔而消失或共享给他人；不具有“自...

### 天下英雄令 / 物品!16:2

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：如携带者死亡，致其死亡者可夺走天下英雄令

### 燕南天藏宝图 / 物品!17:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：不需要持有，由玩家使用，对不在场者有效 所有人各掷一骰子，持有者选定一数字，此数字±1的所有人于藏宝处混战一回合（藏宝图相关效果视为无来源）

### 燕南天藏宝图 / 物品!17:3

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：被燕南天揭破；被江别鹤收走，使用时可选定对谁使用，且可选定到数字结果±2；江小鱼无视数字选人混战；花无缺一定出现在混战

### 血鹦鹉 / 物品!18:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：开场亮明，在持有此卡的玩家所处的场上，场上变换场景则血鹦鹉也到达新场景

### 血鹦鹉 / 物品!18:3

- 当前判断：`字` / 名称：`回合开始时可支付当前全部生命`
- 标记：`free_text, implicit_word, nested_continuation_line`
- 原文：回合开始时可支付当前全部生命：兑去任一敌相等生命，减少下局一卡 场上每因血鹦鹉死亡一人，全-500

### 隐蛊 / 物品!19:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：不需要人物持有，使用者为作用对象本人 使用后使一人物翻为背面且立刻从游戏中所有人物眼前消失，对任何人物来说此卡均不可见，使用任何特技及物品均不需翻开，有一次使用特技他人无法响应的机会，与人对阵时由于己不可见，敌无法放卡 隐形时间持续至下一次出现回合结束

### 缠天七缩扣 / 物品!20:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：不需要人物持有，由玩家使用

### 缠天七缩扣 / 物品!20:2

- 当前判断：`字` / 名称：`使一人物被锁住`
- 标记：`free_text, implicit_word, nested_continuation_line`
- 原文：使一人物被锁住：无法使用闪避轻功类特技，无法不在场，无法动卡撤退，无法不中或削减侧面及受到波及的攻击和效果，且每回合受到对阵各方全部输出总和/10的伤害；破除不中效果、无敌；最多同时锁住1人 杨小邪被锁可以解开并获得缠天七缩扣 杨小邪可持之作为鞭使用

### 雍正剑侠图 / 物品!21:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：不需要持有，由玩家使用，上图与玩家相关

### 雍正剑侠图 / 物品!21:2

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：抓到后亮出，视为拥有剑侠图主人雍正，与康熙,童林结盟（不计人数）

### 雍正剑侠图 / 物品!21:3

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：任意玩家可将己方非恶，非反清且有外号的人姓名登至剑侠图；登剑侠图无需亮明身份，仅需姓名（累积，每大局刷新）；剑侠图主人可允许一个【恶】人登上剑侠图 交战时如两人物在剑侠图上且均同意，则可不交手；若玩家所有人物均在图上，则玩家与剑侠图一方结盟直至无第三方

### 雍正剑侠图 / 物品!21:5

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：任意时刻剑侠图主人可毁去剑侠图，毁去因剑侠图产生的结盟，并同时直接彻底杀死剑侠图上所有人。若如此做，则每因此杀死一人下局少抓一卡

### 雍正剑侠图 / 物品!21:6

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：（此宝物不会被偷走、借走或收走，亦无法被复制或找回（除童林外））

### 人皮面具 / 物品!22:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：轮到本玩家时可戴上（本局起始时亦可），随时可脱下；戴上面具时隐藏人物关系及【恶】，使用特技不翻开；

### 神木王鼎 / 物品!23:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：神木王鼎 每轮多一毒虫，上限5只，每只毒虫选择附冰狂毒混乱中任意一项；可吸收场上相应异常状态并转化为毒虫；毒虫可抵挡伤害，每只100（抵挡伤害毒虫不减）；场下消耗1只毒虫可增加100攻击力 可使自己输出的毒伤加深毒虫×100附毒虫状态

### 神木王鼎 / 物品!23:5

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：丁春秋持有，化功大法附加毒虫×100附毒虫状态

### 龙元 / 物品!24:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：不需要人物持有，使用者为作用对象本人 生命变为无上限，当前生命增加1000 使自身一个特技全部数字翻倍（几率则向有利方向增加或缩小）

### 龙元 / 物品!24:4

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：每人物最多服下一个

### 黑玫瑰 / 物品!26:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：一张招式后可撤退 可牺牲黑玫瑰抵挡一次攻击

### 汗血宝马 / 物品!27:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：能找到不在场的人，每一转轮中可直接对某敌发动袭击

### 白马 / 物品!28:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：非对阵找不到

### 易筋经 / 物品!30:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：自身攻击能力不减弱，不中流失、异常、吸取 或生命+初始值的100%

### 九阴真经 / 物品!33:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：直接习得1条特技，每过一轮出战习得2条，不出战则习得1条。按照金字塔结构学习进阶能力。

### 怜花宝鉴 / 物品!34:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：从废牌中随机选择一人物，习得其一特技 可以用自身特技交换抽取人物的一个特技，如使用身份技替换，则身份技消失，换来的特技视为身份技

### 怜花宝鉴 / 物品!34:3

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：王怜花不需要失去自身特技即可得到抽取人物的特技

### 忘情天书 / 物品!35:4

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：一人只能学会其中之一，对多人卡有效

### 辟邪剑谱 / 物品!36:2

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：连续不出战两轮才可习得 他人不知此为物品

### 葵花宝典 / 物品!37:1

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text, nested_continuation_line`
- 原文：欲练此功，必先自宫；持有者每轮自上向下学会一个特技；起始即习得内功；东方不败跳过招式、武功、（字）学习 由葵花宝典习得的特技视为身份技

### 葵花宝典 / 物品!37:9

- 当前判断：`说明` / 名称：`—`
- 标记：`free_text`
- 原文：方证，冲虚，风清扬，令狐冲，任我行可不练

- 仅显示前 80 条，完整列表见 `data/cards_current/abilities.jsonl`。