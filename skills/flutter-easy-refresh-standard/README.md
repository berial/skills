# Flutter EasyRefresh 自动化规范 / Automated EasyRefresh Standardization

> Auto-detect paginated APIs, enforce EasyRefreshController, auto-generate localization config.
> 自动检测分页接口、强制 EasyRefreshController、自动生成本地化配置。

[![Flutter](https://img.shields.io/badge/Flutter-%3E%3D3.10-blue)](https://flutter.dev)
[![easy_refresh](https://img.shields.io/badge/easy_refresh-%5E3.5.1-brightgreen)](https://pub.dev/packages/easy_refresh)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## 三个核心目的 / Three Core Purposes

| # | 目的 | 自动化行为 |
|---|------|-----------|
| 1 | 🔍 自动检测分页接口 → 包装 EasyRefresh | 识别 `page`/`offset`/`cursor` 参数，改造为 EasyRefresh + Controller |
| 2 | 🎮 强制使用 EasyRefreshController | `controlFinishRefresh: true` 始终需要；`controlFinishLoad` 仅分页场景为 true |
| 3 | 🌐 自动生成 EasyRefreshConfig | 根据**用户对话语种**（优先）自动创建本地化文件，在 `main()` 中初始化 |

## 触发条件 / Trigger Conditions

| 场景 | 示例 |
|------|------|
| 用户要求添加刷新/加载更多 | "加个下拉刷新"、"需要上拉加载更多"、"add pull-to-refresh" |
| 代码中检测到分页接口 | API 含 `page`/`pageSize`/`offset`/`limit`/`cursor` |
| 代码中使用了 EasyRefresh | 自动检查 Controller 配置是否符合规范 |
| 用户提到相关关键词 | "刷新"、"加载更多"、"分页"、"EasyRefresh"、"easy_refresh" |

## 快速开始 / Quick Start

```bash
flutter pub add easy_refresh
```

之后只需编写带分页参数或需要刷新的接口调用，AI 自动：

```
检测到分页/刷新需求 → 创建 Controller（按场景配置 control*）→ 包装 EasyRefresh → 生成 EasyRefreshConfig → main() 初始化
```

## 改造效果 / Before → After

### 仅刷新场景

```dart
// Before — 无刷新能力
Future<void> _loadData() async {
  _items = await api.getItems();
}

// After — EasyRefresh + Controller（仅 controlFinishRefresh: true）
late final _controller = EasyRefreshController(controlFinishRefresh: true);
EasyRefresh(controller: _controller, onRefresh: _onRefresh, child: ListView(...))
```

### 分页场景

```dart
// Before — 手动分页
Future<void> _fetchData(int page) async {
  final result = await api.getItems(page: page, pageSize: 20);
  setState(() => _items = [..._items, ...result.items]);
}

// After — EasyRefresh + Controller（双 control: true）
late final _controller = EasyRefreshController(
  controlFinishRefresh: true, controlFinishLoad: true,
);
EasyRefresh(controller: _controller, onRefresh: _onRefresh, onLoad: _onLoad, ...)
```

### ViewModel 架构

```dart
// EasyRefreshController 在 ViewModel 中创建、调用、回收
class MyViewModel {
  final controller = EasyRefreshController(controlFinishRefresh: true);
  Future<void> onRefresh() async { /* ... */ controller.finishRefresh(); }
  void dispose() => controller.dispose();
}

// View 层只做绑定
EasyRefresh(controller: _vm.controller, onRefresh: _vm.onRefresh, ...)
```

## Controller 参数速查 / Controller Quick Reference

| 场景 | controlFinishRefresh | controlFinishLoad | resetFooter |
|------|:---:|:---:|:---:|
| 仅刷新（无 onLoad） | ✅ true | ❌ | ❌ |
| 刷新 + 分页（有 onLoad） | ✅ true | ✅ true | ✅ |
| ViewModel 架构 | ViewModel 中创建 | ViewModel 中创建 | ViewModel 中调用 |

## 自动生成配置 / Auto-generated Config

```dart
// lib/common/easy_refresh_config.dart（自动创建，语种跟随用户对话语种）

class EasyRefreshConfig {
  static void init() {
    EasyRefresh.defaultHeaderBuilder = () => ClassicHeader(
      pulledText: '下拉刷新',        // 中文/英文自动适配
      processingText: '正在刷新...',
      // ...
    );
    EasyRefresh.defaultFooterBuilder = () => ClassicFooter(
      noMoreText: '— 已经到底了 —',
      loadingText: '加载中...',
      // ...
    );
  }
}
```

```dart
// lib/main.dart（自动添加）
void main() {
  EasyRefreshConfig.init();    // ⚠️ 必须在 runApp 之前
  runApp(const MyApp());
}
```

## 改造检查清单 / Refactoring Checklist

### 分页场景
- [ ] `controlFinishRefresh: true` + `controlFinishLoad: true`
- [ ] `dispose()` 释放 Controller
- [ ] `_onRefresh()` 中调用 `resetFooter()`
- [ ] `_onLoad()` 失败时 `_page--`
- [ ] 异步回调中 `if (!mounted) return;`
- [ ] 首次加载单独处理（`_initialLoading`）

### 仅刷新场景
- [ ] `controlFinishRefresh: true`（不设置 `controlFinishLoad`）
- [ ] `dispose()` 释放 Controller
- [ ] 不设置 `onLoad`

### 通用
- [ ] `easy_refresh_config.dart` 已创建
- [ ] `main()` 中调用了 `EasyRefreshConfig.init()`

## 参考资源 / References

- **Skill 详细文档**: [SKILL.md](SKILL.md)
- **代码模式速查**: [references/easy_refresh_patterns.md](references/easy_refresh_patterns.md)
- **EasyRefresh 官方**: https://pub.dev/packages/easy_refresh
- **API 文档**: https://pub.dev/documentation/easy_refresh/latest/
- **GitHub**: https://github.com/xuelongqy/flutter_easy_refresh

## License

MIT
