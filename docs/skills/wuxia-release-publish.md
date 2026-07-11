# Skill: 静态发布

## 仓库分工

主工程：

```text
https://github.com/tianyulu1013/wuxia_main_agent
```

静态发布：

```text
https://github.com/tianyulu1013/wuxia_static_publish
```

## 本地目录

- 主工程：仓库根目录。
- 静态导出：`site_export/`
- 静态发布仓库：`static_publish_repo/`

`site_export/` 和 `static_publish_repo/` 被主工程 `.gitignore` 忽略。

## 导出流程

```powershell
python scripts/export_static_site.py
```

然后同步 `site_export/` 到 `static_publish_repo/`，在 `static_publish_repo/` 内提交并推送。

## Netlify 配置

```text
Build command: 留空
Publish directory: .
```

## 注意事项

- `web/card_browser/` 本身是本地动态版前端，不等于完整静态站。
- 发布站点应使用 `scripts/export_static_site.py` 生成的纯静态快照。
- 规则书、剧本书以后可以作为静态站页面加入，但不要把未确认的 AI 评语混为牌面事实。
