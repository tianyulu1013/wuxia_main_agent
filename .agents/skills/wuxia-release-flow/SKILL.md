---
name: wuxia-release-flow
description: Use when working on 五行卡牌 local web fixes, 70-card deck image imports, selective card cropping, WebP conversion, historical card images, document-library changes, static exports, Git commits, GitHub pushes, Netlify/static publishing, cache-busting, or any question about whether to change site/library/document versions. This skill defines the image and release workflow and prevents internal repairs from being mistaken for public releases.
---

# 五行卡牌发布流程

## 核心原则

版本号只表示“对外可见发布状态”，不表示每一次本地内部修改。

不要因为以下操作升级 `library_version`、`site_version` 或文档版本：

- 本地 UI bug 修复。
- CSS/布局调整。
- 接口临时修复。
- 本地服务重启。
- 浏览器缓存规避。
- Codex 自己验证页面。
- 未经用户确认的实验性改动。

除非用户明确说“发布”“给别人看”“上传 Git/Netlify”“生成可发布快照”，否则只把工作视为本地修复。

**绝对限制：在没有获得用户明确允许和清晰的推送指令前，AI 绝对禁止在主仓库或静态发布仓库执行任何 git commit 或 git push 推送动作。所有的改动和打包测试默认仅作为本地文件修复。**

## 版本类型

- `library_version`：资料库内容结构或资料库对外组织方式的发布版本。
- `site_version`：网页功能和交互的对外发布版本。
- 文档 `version`：规则书、剧本等文档自身的作者版本。
- 前端资源查询参数：`app.js?v=...`、`styles.css?v=...` 只是缓存破除标记，不等于公开版本号。

## 工作分级

### 1. 本地修复

- 不升级 `library_version`、`site_version`、文档 `version`。
- 可以修改前端资源查询参数来避开浏览器缓存。
- 不提交、不推送，除非用户明确要求。
- 最终回复要说明“本地已修复，未提交未推送”。

### 2. 可发布快照

用户说“本地稳定了，可以准备发给别人看”或要求生成 `site_export/` 时才进入此流程。先确认是否需要升级 `library_version` 或 `site_version`，然后再导出和验证。

### 3. 正式发布

只有用户明确要求上传 Git、推送 GitHub、部署 Netlify 或发布新版时才执行。发布前列出改动，确认版本号，再提交和推送。

## 70 张牌堆图更新

当作者交付一张 10×7、共 70 张卡的新版牌堆大图时，必须遵循：

1. 读取实际更新日志或已回录批次，得到改动卡、受影响牌堆和槽位；作者最终卡面是权威来源。
2. 在替换当前图片前，先冻结每张被修改旧卡的当前 WebP 和完整旧卡数据。
3. 把牌堆大图归档到对应 release 版本目录。
4. 只把更新记录涉及的槽位切成当前单卡图；不得把同牌堆其余未改卡误记为发生版本变化。
5. 将当前单卡图转成 550×900、质量 85 的 WebP，并更新图片清单。
6. 核对历史图、当前图、卡牌 ID、牌堆、槽位、裁切框和更新记录能够相互对应。
7. 先在本地网页和静态导出中验证；用户未明确要求时，不提交、不推送、不发布。

完整路径、数据结构、命令边界和验收规则见 [卡面图片更新流程](references/card-image-release.md)。

## 禁止事项

- 不要把“缓存参数变化”说成网站版本升级。
- 不要因为 Codex 内部修复就自动改 `site_version`。
- 不要未经确认推送 GitHub 或更新 Netlify。
- 不要把内部报告、待办、AI 理解默认放入对外资料库。
- 不要先覆盖当前小图，再补做旧版历史图。
- 不要仅凭整张牌堆大图推断全部 70 张卡都发生了改动。
- 不要在没有核对更新记录和槽位顺序时批量切图。

## 回复口径

```text
已本地修复并验证；未提交、未推送；公开版本号未变。
```
