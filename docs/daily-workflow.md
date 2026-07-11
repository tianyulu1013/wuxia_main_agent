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

## 提出改卡意见

作者可以直接用自然语言描述，例如：

> 周芷若是不是太弱，九阴白骨爪输出提高 100 怎么样？

处理方式：

1. 先查当前卡牌文本和卡面。
2. 分析是否符合艺术形象、规则稳定性、文本清晰度、实际玩法。
3. 生成候选新版文本。
4. 写入 `data/change_candidates.json`。
5. 等作者确认。

## 确认改卡

作者确认后，才进入源数据更新流程：

1. 修改 PSD。
2. 更新 Excel。
3. 重建数据库。
4. 生成玩家更新说明。
5. 更新 release 卡面图。

## 记录评语或裁定

评语、裁定、强度、定位、电子化风险、攻略写入：

- `data/card_reviews.json`

这些内容不改牌面，不进入源数据库。

## Release 后更新卡面

当前网页读取：

- `data/release_images/cards/`

如果已经有单卡 PNG，只要更新对应图片即可。

如果只有 TTS 用的 70 张大图，未来应使用固定切图脚本生成单卡 PNG。这个流程还未固化。

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
