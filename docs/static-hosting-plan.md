# 静态在线版方案

当前查询工具是本地动态服务：

- Python 后端提供 API。
- 后端读取 SQLite、JSON、卡面 PNG。
- 前端通过 `/api/search` 和 `/api/card/{id}` 查询。

因此它不能直接作为普通静态网站上传。

## 可行方向

可以制作一个静态导出版，供在线查看。

导出版结构示例：

```text
site_export/
  index.html
  app.js
  styles.css
  data/
    meta.json
    cards.json
    search-index.json
  card-images/
    金庸1/
    古龙1/
```

## 静态版能力

静态版可以支持：

- 本地/在线搜索
- 字段级筛选
- 查看详情
- 查看卡面
- 查看评语和改卡候选

静态版不适合直接支持：

- 在线写入候选
- 自动修改数据库
- 自动同步 Excel/PSD

这些仍应在本地工具里完成。

## 推荐路线

本地编辑和数据整理继续使用动态版。

对外查看使用静态快照。

## 当前导出流程

运行：

```powershell
& "C:\Users\biaaa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts/export_static_site.py
```

输出：

- `site_export/`

当前快照规模约 245 MB，其中绝大多数是单卡 PNG。

`site_export/` 可以直接作为纯静态网站发布。

## Netlify 发布

可以用两种方式：

1. 手动发布：在 Netlify 的 Deploys 页面拖拽 `site_export/`。
2. Git 发布：另建一个静态快照仓库，把 `site_export/` 的内容提交到该仓库，Netlify 连接这个仓库自动部署。

更推荐 Git 发布，因为以后只需要：

1. 本地重新运行 `scripts/export_static_site.py`。
2. 同步 `site_export/` 到静态快照仓库。
3. 提交并 push。
4. Netlify 自动更新线上站。

## 注意

不要把 `site_export/` 提交到本工作仓库。它是生成物，已经在 `.gitignore` 中忽略。

如果静态快照仓库长期保留所有历史图片，仓库会逐渐变大。未来可考虑：

- 静态仓库只保留当前版本。
- 旧版卡面单独归档。
- 或者用对象存储/CDN 管图片。
