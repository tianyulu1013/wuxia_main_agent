---
name: wuxia-release-flow
description: Use when working on 五行卡牌 local web fixes, document-library changes, static exports, Git commits, GitHub pushes, Netlify/static publishing, cache-busting, or any question about whether to change site/library/document versions. This skill defines the release workflow and prevents internal repairs from being mistaken for public releases.
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

## 禁止事项

- 不要把“缓存参数变化”说成网站版本升级。
- 不要因为 Codex 内部修复就自动改 `site_version`。
- 不要未经确认推送 GitHub 或更新 Netlify。
- 不要把内部报告、待办、AI 理解默认放入对外资料库。

## 回复口径

```text
已本地修复并验证；未提交、未推送；公开版本号未变。
```
