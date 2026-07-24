# 卡面图片更新流程

## 目标

作者每次可能交付一张 10×7、共 70 张卡的牌堆大图。系统要根据本次实际更新记录，只替换发生变化或新增的单卡图片，同时保留被替换卡牌的旧版网页图和完整旧卡数据。

本流程只处理卡面图片及其版本对应关系。作者最终卡面仍是权威来源；TODO 和候选文本只用于追踪，不得覆盖作者实际修改。

## 既有目录和记录

- 牌堆大图：`data/release_images/<release_id>/`
- 最新牌堆索引：`data/release_images/latest_decks.json`
- 当前单卡 PNG 母版：`data/release_images/cards/<牌堆>/`
- 当前网页 WebP：`data/release_images/cards_webp/<牌堆>/`
- 当前 PNG 切图清单：`data/release_images/card_crops.jsonl`
- 当前 WebP 清单：`data/release_images/web_card_images.jsonl`
- 历史单卡 WebP：`data/release_images/cards_history/<card_id>/pre-<release_id>.webp`
- 历史完整卡牌快照：`data/cards_history/card_versions.jsonl`
- 发布批次及新旧版本关系：`data/cards_history/releases.json`
- 历史层说明：`data/cards_history/README.md`
- 牌堆槽位顺序：`docs/tts-slot-orders-v0.1.md`

历史层从公开更新 `3.07` 开始，不向更早版本倒推。历史图片和历史卡牌快照一经建立不得覆盖。

## 一、确定本次换图范围

1. 读取本次实际更新日志；若整批日志尚未生成，读取已回录批次中的实际改动记录。
2. 为每张卡确认：
   - `card_id`
   - 卡名
   - `change_type`：修改、新增、删除或移位
   - `release_deck`
   - `slot`
   - 当前版本和将发布版本
3. 汇总 `affected_decks`，最终交付时列出本次有哪些牌堆发生改动。
4. 使用 `docs/tts-slot-orders-v0.1.md` 和当前 manifest 交叉核对槽位，不能只根据文件名或肉眼位置猜测。
5. 新增卡没有旧版本；只是移位但卡面未变时，不生成虚假的旧卡文本版本。是否保留旧槽位图片由发布记录明确说明。

更新日志或已回录批次决定“哪些卡需要换图”；牌堆大图只提供新版像素，不自行扩大改动范围。

## 二、替换前冻结旧版本

对每张已有卡且牌面发生变化的卡，在任何当前图片被覆盖前执行：

1. 从当前 `cards_webp` 找到该卡正在网页使用的 WebP。
2. 复制到 `data/release_images/cards_history/<card_id>/pre-<release_id>.webp`。
3. 计算 SHA-256，记录宽度、高度、WebP 质量、原当前图片路径、来源牌堆、来源版本、槽位和裁切框。
4. 把改前完整卡牌数据写入 `data/cards_history/card_versions.jsonl`，版本 ID 使用 `<card_id>@pre-<release_id>`。
5. 在 `data/cards_history/releases.json` 中记录：
   - `previous_version_id`
   - `current_version_id`
   - `release_deck`
   - `slot`
   - 更新日志路径
   - `affected_decks`
6. 检查历史目标文件和版本 ID 不存在；若已经存在，停止并核对，不得覆盖。

必须保存完整旧卡快照，不能依赖“旧文本 → 新文本”的差异日志在未来反向还原。

## 三、归档和索引 70 卡牌堆图

1. 将作者交付的大图原样保存到 `data/release_images/<release_id>/`。
2. 确认大图为 10 列×7 行，单格预期为 550×900；整图通常为 5500×6300。
3. 运行 `scripts/index_release_images.py`，更新：
   - `data/release_images/latest_decks.json`
   - `docs/release-image-index.md`
4. 核对索引选择的是本次目标版本和正确牌堆，不能仅因版本字符串较大就接受错误文件。

牌堆大图是发布母版，不直接作为网页逐卡图片。

## 四、按更新记录切出当前小图

裁切坐标按从左到右、从上到下编号：

```text
column = (slot - 1) % 10
row = (slot - 1) // 10
box = (column * 550, row * 900, (column + 1) * 550, (row + 1) * 900)
```

只把本次更新记录中的槽位写入 `data/release_images/cards/<牌堆>/`，并同步其 `card_crops.jsonl` 记录。每条记录至少保留来源大图、release 版本、牌堆、槽位、行列、裁切框、卡名和输出路径。

把本次作者确认的换图范围写入：

- `data/release_images/release_image_updates/<release_id>.json`

然后运行选择性切图和 WebP 登记：

```powershell
& "<项目使用的 Python>" scripts/apply_release_card_image_update.py data/release_images/release_image_updates/<release_id>.json
```

该脚本会在确认所需历史版本已经存在后，只处理登记文件中的卡牌，并同步当前 PNG、当前 WebP、两个图片 manifest 和 `data/cards_history/releases.json`。新增卡必须标记为不需要历史图；修改卡缺少历史数据或历史 WebP 时脚本必须停止。

`scripts/build_release_card_crops.py` 当前会按最新牌堆索引重建所有可识别牌堆的全部小图。使用它之前必须已经完成旧版本冻结；若本次只允许替换少量卡，应采用选择性裁切或先输出到暂存目录，不能无检查地覆盖整个当前目录。

## 五、生成网页 WebP

当前网页图片规范：

- 尺寸：550×900
- 格式：WebP
- 质量：85
- 色彩：RGB

从当前 PNG 母版生成 WebP：

```powershell
& "<项目使用的 Python>" scripts/build_web_card_images.py --quality 85
```

该脚本当前会重建整个 `cards_webp` 目录和 `web_card_images.jsonl`。运行前必须确认历史图已冻结；运行后用哈希核对本次未改卡的像素内容没有意外变化。

网页优先读取 `cards_webp`，PNG 仅作为当前单卡母版和兼容回退。历史页面必须根据历史版本记录读取 `cards_history` 中的旧版 WebP，不能指向当前图。

## 六、验收

逐项检查：

1. 更新记录中的每张修改卡都有旧版数据和旧版 WebP；新增卡没有伪造旧版本。
2. 新版图的牌堆、槽位、卡名和 `card_id` 对应正确。
3. 当前 WebP 均为 550×900、质量 85，清单中的哈希和实际文件一致。
4. 被修改卡的旧版页面显示旧图，当前页面显示新版图。
5. 未列入更新记录的卡没有被登记为发生版本变化。
6. 本地查询网站能够加载新版 WebP，文字清晰；优先抽查小字号卡。
7. 静态导出只引用可部署的 WebP 路径，不引用本机绝对路径。
8. 最终结论列出本次所有受影响牌堆及其中改动卡。

## 七、发布边界

完成图片归档、裁切、WebP 转换和本地验证，不等于正式发布。

- 用户未明确要求：不改公开版本号，不 commit，不 push，不部署。
- 用户要求生成可发布快照：重新生成并验证 `site_export/`。
- 用户明确要求正式发布：列出改动和版本号，得到明确指令后再执行 Git/静态站发布流程。
