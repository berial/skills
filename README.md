# My Agent Skills

自定义 Agent Skills 集合，适用于 Codex / Claude Code 等 AI Agent。

## 安装

```bash
npx skills add berial/skills --skill '*' --agent universal --yes
```

## Skills

| Skill | 自动触发 | Description |
|-------|:---:|-------------|
| [dart-generate-doc-comments](skills/dart-generate-doc-comments/) | ✅ | 为 Dart/Flutter 代码生成有信息量的 Dartdoc 文档注释，写完代码自动生效，跳过自明元素，参数说明强制 `* [param]` 列表格式，中英文跟随对话语种 |
| [flutter-easy-refresh-standard](skills/flutter-easy-refresh-standard/) | ✅ | 自动化规范 EasyRefresh：检测分页接口、强制 EasyRefreshController、按对话语种生成本地化配置 |

## 自动触发说明

两个 skill 均支持 AI 自动调用，无需用户显式 `/use`：

- **dart-generate-doc-comments**：写完/改完任何 `.dart` 文件后自动触发，即使用户未提及"文档""注释"。注释语言跟随对话语种（中文→`zh`，英文→`en`）。参数说明（≥ 2 个参数时）必须用 `* [paramName]` Markdown 列表格式独立成段。
- **flutter-easy-refresh-standard**：项目依赖 `easy_refresh`、检测到分页 API（`page`/`pageSize`/`offset`/`limit`/`cursor`）、用户请求刷新/加载更多/分页、或代码中已有 EasyRefresh 用法时自动触发。

## License

[MIT](LICENSE)
