# Flutter EasyRefresh 自动化规范 / Automated EasyRefresh Standardization

> Auto-detect paginated APIs, enforce `EasyRefreshController`, and auto-generate localization config.
> 自动检测分页接口、强制 EasyRefreshController、自动生成本地化配置。

[![Flutter](https://img.shields.io/badge/Flutter-%3E%3D3.10-blue)](https://flutter.dev)
[![easy_refresh](https://img.shields.io/badge/easy_refresh-%5E3.5.1-brightgreen)](https://pub.dev/packages/easy_refresh)

---

## 三个核心目的 / Three Core Purposes

| # | 目的 | 说明 |
|---|------|------|
| 1 | 🔍 自动检测分页接口 | 识别 API 中的 `page`/`offset`/`cursor` 等分页参数，自动改造为 EasyRefresh 分页模式 |
| 2 | 🎮 强制 EasyRefreshController | 所有 EasyRefresh 必须通过 Controller 控制状态，`controlFinish*` 双 `true` |
| 3 | 🌐 自动生成 EasyRefreshConfig | 根据项目语种自动创建本地化配置文件，在 `main()` 中初始化 |

## 快速开始 / Quick Start

```bash
flutter pub add easy_refresh
```

之后只需编写带分页参数的接口调用，AI 会自动完成以下改造：

```
检测到分页参数 → 添加 Controller → 包装 EasyRefresh → 生成配置 → main() 初始化
```

## 改造效果 / Before → After

### Before（手动分页）
```dart
Future<void> _fetchData(int page) async {
  final result = await api.getItems(page: page, pageSize: 20);
  setState(() => _items = [..._items, ...result.items]);
}
// ... 手动在 ListView builder 中触发加载
```

### After（EasyRefresh + Controller）
```dart
late final EasyRefreshController _controller = EasyRefreshController(
  controlFinishRefresh: true,
  controlFinishLoad: true,
);

Future<void> _onRefresh() async { /* 重置 + finishRefresh + resetFooter */ }
Future<void> _onLoad() async { /* 追加 + finishLoad */ }

EasyRefresh(controller: _controller, onRefresh: _onRefresh, onLoad: _onLoad, ...)
```

## 自动生成配置 / Auto-generated Config

```dart
// lib/common/easy_refresh_config.dart（自动创建）

class EasyRefreshConfig {
  static void init() {
    EasyRefresh.defaultHeaderBuilder = () => ClassicHeader(
      pulledText: '下拉刷新',      // 中文/英文自动适配
      // ...
    );
    EasyRefresh.defaultFooterBuilder = () => ClassicFooter(
      noMoreText: '— 已经到底了 —',
      // ...
    );
  }
}
```

```dart
// lib/main.dart（自动添加）
void main() {
  EasyRefreshConfig.init();  // 自动在 runApp 前调用
  runApp(const MyApp());
}
```

## 改造检查清单 / Refactoring Checklist

- [ ] `controlFinishRefresh: true`
- [ ] `controlFinishLoad: true`
- [ ] `dispose()` 释放 Controller
- [ ] `_onRefresh()` 中调用 `resetFooter()`
- [ ] `_onLoad()` 失败时 `_page--`
- [ ] 异步回调中 `if (!mounted) return;`
- [ ] 首次加载单独处理（`_initialLoading`）
- [ ] `easy_refresh_config.dart` 已创建
- [ ] `main()` 中调用了 `EasyRefreshConfig.init()`

## License

MIT
