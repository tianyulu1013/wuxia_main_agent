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

暂时继续使用本地动态版。

等查询体验稳定后，再做：

1. `scripts/export_static_site.py`
2. 把 SQLite 和 JSON 层导出为前端可读 JSON。
3. 复制当前卡面图片。
4. 生成 `site_export/`。
5. 上传到静态托管。

这样可以在线查看，但核心编辑工作仍然留在本地。
