# 战斗人物极简横向基线入口

状态：随逐卡作者校准持续增长。

默认只按当前维度读取一个文件：

- 正面输出：`data/review/comparison/front-output.json`
- 侧面输出：`data/review/comparison/side-output.json`
- 正面生存：`data/review/comparison/front-survival.json`
- 侧面生存：`data/review/comparison/side-survival.json`
- 全局影响：`data/review/comparison/global-influence.json`

输出横表只保留一个主期望、确定穿透输出、穿透率和一句说明。生存与全局影响横表只保留强弱和一句依据。

`data/review/calibrated_stats.json`和`data/review/combat_baselines.json`继续随每名人物逐人写入，作为详细统计归档，但不再默认读取。需要复算时再查询详细统计或进入`data/review/cards/<卡名>/`对应维度文件。
