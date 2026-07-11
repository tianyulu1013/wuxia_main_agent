# 卡面待修改清单

这份文档只记录 PSD / release 牌面需要以后修改的问题。

数据库不以这些卡面错误为准：数据库已经按作者裁定保存为正确结构。这里的项目用于以后改 PSD、重新导出 release 图、生成玩家更新说明。

## 缺冒号 / 标点错误

- 赵德言 / `归魂十八爪`
  - 牌面图：[57_赵德言.png](D:/workspace/wuxia-card-agent/data/release_images/cards/黄易1/57_赵德言.png)
  - 数据库：招式 `归魂十八爪`，其下 `朱雀拒尸 / 玄武悲泣 / 青龙嫉主` 为姿态子项
  - 卡面待修：`招式：归魂十八爪 --` 应补清晰分隔；子项排版也需要整理

- 郭襄（小） / `瑜伽密乘`
  - 牌面图：[52_郭襄（小）.png](D:/workspace/wuxia-card-agent/data/release_images/cards/金庸1/52_郭襄（小）.png)
  - 数据库：内功 `瑜伽密乘`
  - 卡面待修：`内功：瑜伽密乘 1/3大招正常` 缺少特技名后的冒号

- 狄云 / `连城剑法`
  - 牌面图：[32_狄云.png](D:/workspace/wuxia-card-agent/data/release_images/cards/金庸1/32_狄云.png)
  - 数据库：招式 `连城剑法`
  - 卡面待修：`招式：连城剑法 金水 金木 300金` 缺少特技名后的冒号

- 金坷垃三人组 / `【东仙の手刀】`
  - 牌面图：[22_金坷垃三人组.png](D:/workspace/wuxia-card-agent/data/release_images/cards/现代1/22_金坷垃三人组.png)
  - 数据库：武功 `【东仙の手刀】`
  - 卡面待修：`武功：【东仙の手刀】，...` 应改为更清晰的特技名分隔

- 绝无神 / `杀拳`
  - 牌面图：[38_绝无神.png](D:/workspace/wuxia-card-agent/data/release_images/cards/其他1/38_绝无神.png)
  - 数据库：招式 `杀拳`
  - 卡面待修：`招式：杀拳 --` 缺少特技名后的冒号

## 缩进 / 子项排版

- 花无缺 / `移花接玉`
  - 牌面图：[51_花无缺.png](D:/workspace/wuxia-card-agent/data/release_images/cards/古龙1/51_花无缺.png)
  - 卡面待修：缩进/排版需整理

- 紫衣侯 / `一百九十三家秘门剑法`
  - 牌面图：[29_紫衣侯.png](D:/workspace/wuxia-card-agent/data/release_images/cards/古龙2/29_紫衣侯.png)
  - 卡面待修：缩进/排版需整理

- 郭襄（峨眉祖师） / `四象掌`、`金顶绵掌`、`飘雪穿云掌`、`佛光普照`
  - 牌面图：[53_郭襄（峨眉祖师）.png](D:/workspace/wuxia-card-agent/data/release_images/cards/金庸1/53_郭襄（峨眉祖师）.png)
  - 卡面待修：多条招式缩进/排版需整理

- 浦饭幽助 / `【灵光波动拳】`
  - 牌面图：[15_浦饭幽助.png](D:/workspace/wuxia-card-agent/data/release_images/cards/现代1/15_浦饭幽助.png)
  - 数据库：独立招式，不是 `百裂拳` 子项
  - 卡面待修：待作者查看牌面确认是否需要整理

## 多人一卡结构

- 全真七子
  - 牌面图：[04_全真七子.png](D:/workspace/wuxia-card-agent/data/release_images/cards/金庸3/04_全真七子.png)
  - 数据库：已将 `丹阳子 / 长春子 / 铁脚仙 / 玉阳子 / 长生子 / 长真子 / 广宁子 / 清净散人` 识别为具体特技名
  - 后续结构待扩展：需要正式表示“某条特技属于某个人物单元”

- 阿三阿四
  - 牌面图：[53_阿三阿四.png](D:/workspace/wuxia-card-agent/data/release_images/cards/其他1/53_阿三阿四.png)
  - 数据库：已将 `大悲掌` 和 `反通吃馆招式` 拆为两个招式特技
  - 后续结构待扩展：需要正式表示 `三撇老蛋 / 吹牛皮` 属于阿三，`拔毛剃刀 / 拍马屁` 属于阿四，`内斗` 属于二人共同
