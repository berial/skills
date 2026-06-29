---
name: flutter-easy-refresh-standard
description: >
  When the project depends on easy_refresh, standardize list pages with three rules:

  1. Auto-detect paginated APIs — Refactor pages calling APIs with pagination params (page/pageSize/offset/limit/cursor) to use EasyRefresh.
  2. Enforce EasyRefreshController — All EasyRefresh usage MUST use an EasyRefreshController. `controlFinishRefresh: true` always; `controlFinishLoad: true` ONLY when onLoad (pagination) is present. Dispose it, and call resetFooter() after refresh in paginated pages.
  3. Auto-generate EasyRefreshConfig — Locale follows the user's conversation language first (Chinese→zh, English→en), then project settings; auto-create the config for Header/Footer localization and call setup in main() before runApp().

  Trigger when: the project depends on easy_refresh; a page calls a paginated API; the user requests 刷新/加载更多/下拉刷新/上拉加载/分页/load more/pull-to-refresh/pagination, or asks to add refresh/load-more to a list/page; or code contains EasyRefresh or easy_refresh usage.
---

# Flutter EasyRefresh 自动化规范 / Automated EasyRefresh Standardization

## 概述 / Overview

此 skill 在项目已依赖 `easy_refresh` 的前提下，对**列表页面**自动完成三项标准化改造。触发条件覆盖：

| 触发场景 | 示例 |
|----------|------|
| 用户要求添加刷新/加载更多 | "加个下拉刷新"、"需要上拉加载更多"、"add refresh"、"load more" |
| 代码中检测到分页接口 | API 含 `page`/`pageSize`/`offset`/`limit`/`cursor` 参数 |
| 代码中使用了 EasyRefresh | 自动检查 Controller 配置是否符合规范 |
| 用户提到相关关键词 | "刷新"、"分页"、"下拉"、"上拉"、"EasyRefresh"、"easy_refresh" |

| # | 目的 | 触发方式 |
|---|------|----------|
| 1 | 自动包装 EasyRefresh 处理刷新/分页 | 用户请求刷新/加载更多，或检测到分页 API |
| 2 | 强制使用 EasyRefreshController | 每次生成或修改 EasyRefresh 代码时自动执行 |
| 3 | 自动创建 EasyRefreshConfig 本地化 | 首次使用时检测项目语种并生成配置 |

---

## 工作流程 / Workflow

```
┌─────────────────────────────────────────────────┐
│  Step 1: 检测项目是否依赖 easy_refresh           │
│    → 检查 pubspec.yaml                          │
│    → 如未依赖，提示 flutter pub add easy_refresh │
├─────────────────────────────────────────────────┤
│  Step 2: 检测页面是否调用了分页 API               │
│    → 扫描函数签名含 page/pageSize/offset/limit   │
│    → 或 API 路径含 ?page= / &offset= 等参数       │
├─────────────────────────────────────────────────┤
│  Step 3: 改造为 EasyRefresh + Controller 模式    │
│    → 创建 EasyRefreshController                    │
│    → 有分页: controlFinishLoad=true               │
│    → 无分页: 仅 controlFinishRefresh=true          │
│    → 提取 _onRefresh / _onLoad 方法（按需）        │
│    → 用 EasyRefresh 包裹列表组件                  │
│    → 添加 dispose 释放 Controller                │
├─────────────────────────────────────────────────┤
│  Step 4: 检测/创建 EasyRefreshConfig              │
│    → 检查项目中是否已有 config 文件               │
│    → 根据用户对话语种（P0）自动生成本地化文本       │
│    → 在 main() 中调用 EasyRefreshConfig.init()    │
└─────────────────────────────────────────────────┘
```

---

## 目的一：使用 EasyRefresh 处理列表刷新和分页

### 1.1 分页参数识别规则 / Pagination Detection Rules

当页面代码中出现以下**任一模式**时，即判定为分页接口，按分页场景改造（1.3）：

#### 直接参数模式
```dart
// 检测到 page + pageSize 参数
Future<Response> fetchList(int page, int pageSize) { ... }
Future<Response> getData({int pageNum = 1, int pageSize = 20}) { ... }
Future<Response> loadItems(int current, int limit) { ... }

// 检测到 offset + limit 参数
Future<Response> query(int offset, int limit) { ... }

// 检测到 cursor 参数
Future<Response> fetch(String? cursor) { ... }
```

#### API URL 模式
```dart
// 检测到 URL 中包含分页 query 参数
final url = '/api/items?page=$page&pageSize=$pageSize';
final url = '/api/items?offset=$offset&limit=20';
```

#### 请求体模式
```dart
// 检测到请求体包含分页字段
final body = {'page': page, 'pageSize': pageSize};
final body = {'pagination': {'page': 1, 'size': 20}};
```

### 1.2 仅刷新场景（无分页） / Refresh-Only Scenario

当页面只需要下拉刷新、不涉及分页加载时，按以下模板改造。

#### Before（改造前 — 无刷新）
```dart
class SimpleListPage extends StatefulWidget {
  const SimpleListPage({super.key});
  @override State<SimpleListPage> createState() => _SimpleListPageState();
}

class _SimpleListPageState extends State<SimpleListPage> {
  List<Item> _items = [];
  bool _loading = true;

  Future<void> _loadData() async {
    setState(() => _loading = true);
    _items = await api.getItems();
    if (mounted) setState(() => _loading = false);
  }

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('列表')),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              itemCount: _items.length,
              itemBuilder: (_, i) => ListTile(title: Text(_items[i].name)),
            ),
    );
  }
}
```

#### After（改造后 — EasyRefresh + Controller，仅刷新）
```dart
class SimpleListPage extends StatefulWidget {
  const SimpleListPage({super.key});
  @override State<SimpleListPage> createState() => _SimpleListPageState();
}

class _SimpleListPageState extends State<SimpleListPage> {
  /// EasyRefresh 控制器 — 仅刷新，不需要 controlFinishLoad
  late final EasyRefreshController _controller = EasyRefreshController(
    controlFinishRefresh: true,
    // ⚠️ 不设置 controlFinishLoad，因为没有 onLoad
  );

  List<Item> _items = [];
  bool _initialLoading = true;

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    try {
      _items = await api.getItems();
    } catch (e) {
      // 错误处理
    } finally {
      if (mounted) setState(() => _initialLoading = false);
    }
  }

  Future<void> _onRefresh() async {
    try {
      final result = await api.getItems();
      if (!mounted) return;
      setState(() => _items = result);
      _controller.finishRefresh();
    } catch (e) {
      if (!mounted) return;
      _controller.finishRefresh(IndicatorResult.fail);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('列表')),
      body: _initialLoading
          ? const Center(child: CircularProgressIndicator())
          : EasyRefresh(
              controller: _controller,
              onRefresh: _onRefresh,
              // ⚠️ 不设置 onLoad
              child: ListView.builder(
                itemCount: _items.length,
                itemBuilder: (_, i) => ListTile(title: Text(_items[i].name)),
              ),
            ),
    );
  }
}
```

> **关键差异**：仅刷新场景 Controller 不设置 `controlFinishLoad`，EasyRefresh 不设置 `onLoad`。

### 1.3 分页场景改造 / Paginated Refactoring

检测到分页参数后，按以下步骤改造：

#### Before（改造前 — 手动分页）
```dart
class MyListPage extends StatefulWidget {
  const MyListPage({super.key});
  @override State<MyListPage> createState() => _MyListPageState();
}

class _MyListPageState extends State<MyListPage> {
  List<Item> _items = [];
  int _page = 1;
  final int _pageSize = 20;
  bool _hasMore = true;
  bool _loading = false;

  Future<void> _fetchData(int page) async {
    setState(() => _loading = true);
    final result = await api.getItems(page: page, pageSize: _pageSize);
    setState(() {
      _items = page == 1 ? result.items : [..._items, ...result.items];
      _hasMore = result.hasMore;
      _loading = false;
    });
  }

  @override
  void initState() {
    super.initState();
    _fetchData(1);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('列表')),
      body: ListView.builder(
        itemCount: _items.length + (_hasMore ? 1 : 0),
        itemBuilder: (context, index) {
          if (index == _items.length) {
            _fetchData(_page + 1); // ❌ 手动在 build 中触发了加载
            return const Center(child: CircularProgressIndicator());
          }
          return ListTile(title: Text(_items[index].name));
        },
      ),
    );
  }
}
```

#### After（改造后 — EasyRefresh + Controller）
```dart
import 'package:easy_refresh/easy_refresh.dart';
import 'package:flutter_easy_refresh/easy_refresh_config.dart'; // 自动生成的配置

class MyListPage extends StatefulWidget {
  const MyListPage({super.key});
  @override State<MyListPage> createState() => _MyListPageState();
}

class _MyListPageState extends State<MyListPage> {
  /// EasyRefresh 控制器 — 分页场景，两者均为 true
  late final EasyRefreshController _controller = EasyRefreshController(
    controlFinishRefresh: true,   // ⚠️ 必须为 true
    controlFinishLoad: true,      // ⚠️ 分页场景必须为 true
  );

  final List<Item> _items = [];
  int _page = 1;
  static const int _pageSize = 20;
  bool _hasMore = true;
  bool _initialLoading = true;

  @override
  void dispose() {
    _controller.dispose();        // ⚠️ 必须释放
    super.dispose();
  }

  @override
  void initState() {
    super.initState();
    _fetchFirstPage();
  }

  /// 首次加载（无刷新动画）
  Future<void> _fetchFirstPage() async {
    try {
      final result = await api.getItems(page: 1, pageSize: _pageSize);
      if (!mounted) return;
      setState(() {
        _items.addAll(result.items);
        _hasMore = result.hasMore;
        _initialLoading = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() => _initialLoading = false);
    }
  }

  /// 下拉刷新 — 重置并重新加载第一页
  Future<void> _onRefresh() async {
    _page = 1;
    try {
      final result = await api.getItems(page: 1, pageSize: _pageSize);
      if (!mounted) return;
      setState(() {
        _items
          ..clear()
          ..addAll(result.items);
        _hasMore = result.hasMore;
      });
      _controller.finishRefresh();
      _controller.resetFooter();  // ⚠️ 刷新后必须重置 Footer
    } catch (e) {
      if (!mounted) return;
      _controller.finishRefresh(IndicatorResult.fail);
    }
  }

  /// 上拉加载更多 — 追加下一页
  Future<void> _onLoad() async {
    if (!_hasMore) return;
    _page++;
    try {
      final result = await api.getItems(page: _page, pageSize: _pageSize);
      if (!mounted) return;
      setState(() {
        _items.addAll(result.items);
        _hasMore = result.hasMore;
      });
      if (_hasMore) {
        _controller.finishLoad();
      } else {
        _controller.finishLoad(IndicatorResult.noMore);
      }
    } catch (e) {
      if (!mounted) return;
      _page--; // ⚠️ 失败时回退页码
      _controller.finishLoad(IndicatorResult.fail);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('列表')),
      body: _initialLoading
          ? const Center(child: CircularProgressIndicator())
          : EasyRefresh(
              controller: _controller,
              onRefresh: _onRefresh,
              onLoad: _onLoad,
              child: ListView.builder(
                itemCount: _items.length,
                itemBuilder: (context, index) {
                  return ListTile(title: Text(_items[index].name));
                },
              ),
            ),
    );
  }
}
```

### 1.4 改造清单 / Refactoring Checklist

改造时必须逐项确认：

**有分页场景（含 onLoad）：**
- [ ] 添加 `import 'package:easy_refresh/easy_refresh.dart';`
- [ ] 添加 `import 'package:.../easy_refresh_config.dart';`（如已生成）
- [ ] 创建 `EasyRefreshController`（`controlFinishRefresh: true`, `controlFinishLoad: true`）
- [ ] 添加 `dispose()` 释放 Controller
- [ ] 新增 `_onRefresh()` 方法：重置 `_page=1`，clear + addAll，调用 `finishRefresh()` + `resetFooter()`
- [ ] 新增 `_onLoad()` 方法：`_page++`，addAll，判断 `_hasMore` 调用 `finishLoad()`
- [ ] 失败处理：`_onRefresh` 失败调 `finishRefresh(IndicatorResult.fail)`，`_onLoad` 失败调 `finishLoad(IndicatorResult.fail)` 并 `_page--`
- [ ] 首次加载与 EasyRefresh 分离（`_initialLoading` 状态单独处理）
- [ ] 用 `EasyRefresh(controller:)` 包裹列表组件
- [ ] 移除原手动分页代码（build 中的触发逻辑、旧回调等）

**仅刷新场景（无 onLoad，无分页）：**
- [ ] 创建 `EasyRefreshController`（**仅** `controlFinishRefresh: true`，不设置 `controlFinishLoad`）
- [ ] 添加 `dispose()` 释放 Controller
- [ ] `onRefresh` 完成后调用 `_controller.finishRefresh()`
- [ ] 用 `EasyRefresh(controller:)` 包裹列表组件，**不设置 `onLoad`**

### 1.5 分层架构（ViewModel / Controller / Presenter） / Layered Architecture

当项目使用 MVVM、MVC、MVP 等分层架构时，**EasyRefreshController 的创建、调用、回收应放在业务逻辑层**（ViewModel / Presenter / PageController），View 层只消费暴露的接口。

#### 仅刷新 — ViewModel 模式

```dart
// === ViewModel 层 ===
import 'package:easy_refresh/easy_refresh.dart';

class ItemListViewModel {
  /// EasyRefreshController 在 ViewModel 中创建和管理
  final EasyRefreshController refreshController = EasyRefreshController(
    controlFinishRefresh: true,
    // 无分页，不设置 controlFinishLoad
  );

  final List<Item> items = [];
  bool initialLoading = true;

  Future<void> loadData() async {
    initialLoading = true;
    items.clear();
    try {
      final result = await api.getItems();
      items.addAll(result);
    } finally {
      initialLoading = false;
    }
  }

  Future<void> onRefresh() async {
    try {
      final result = await api.getItems();
      items
        ..clear()
        ..addAll(result);
      refreshController.finishRefresh();
    } catch (e) {
      refreshController.finishRefresh(IndicatorResult.fail);
    }
  }

  /// ViewModel 层负责释放 Controller
  void dispose() {
    refreshController.dispose();
  }
}

// === View 层 ===
class ItemListPage extends StatefulWidget {
  const ItemListPage({super.key});
  @override State<ItemListPage> createState() => _ItemListPageState();
}

class _ItemListPageState extends State<ItemListPage> {
  late final ItemListViewModel _viewModel;

  @override
  void initState() {
    super.initState();
    _viewModel = ItemListViewModel()..loadData();
    _viewModel.addListener(() {
      if (mounted) setState(() {});
    });
  }

  @override
  void dispose() {
    _viewModel.dispose();  // ViewModel 释放 → 内部释放 Controller
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('列表')),
      body: _viewModel.initialLoading
          ? const Center(child: CircularProgressIndicator())
          : EasyRefresh(
              controller: _viewModel.refreshController,  // 从 ViewModel 获取
              onRefresh: _viewModel.onRefresh,
              child: ListView.builder(
                itemCount: _viewModel.items.length,
                itemBuilder: (_, i) => ListTile(title: Text(_viewModel.items[i].name)),
              ),
            ),
    );
  }
}
```

#### 分页 — ViewModel 模式

```dart
// === ViewModel 层 ===
class PagedListViewModel {
  /// EasyRefreshController 在 ViewModel 中创建和管理
  final EasyRefreshController refreshController = EasyRefreshController(
    controlFinishRefresh: true,
    controlFinishLoad: true,    // 分页场景
  );

  final List<Item> items = [];
  int page = 1;
  bool hasMore = true;
  bool initialLoading = true;
  static const int pageSize = 20;

  Future<void> loadFirstPage() async {
    try {
      final result = await api.getItems(page: 1, pageSize: pageSize);
      items.addAll(result.items);
      hasMore = result.hasMore;
    } finally {
      initialLoading = false;
    }
  }

  Future<void> onRefresh() async {
    page = 1;
    try {
      final result = await api.getItems(page: 1, pageSize: pageSize);
      items
        ..clear()
        ..addAll(result.items);
      hasMore = result.hasMore;
      refreshController.finishRefresh();
      refreshController.resetFooter();
    } catch (e) {
      refreshController.finishRefresh(IndicatorResult.fail);
    }
  }

  Future<void> onLoad() async {
    if (!hasMore) return;
    page++;
    try {
      final result = await api.getItems(page: page, pageSize: pageSize);
      items.addAll(result.items);
      hasMore = result.hasMore;
      hasMore
          ? refreshController.finishLoad()
          : refreshController.finishLoad(IndicatorResult.noMore);
    } catch (e) {
      page--;
      refreshController.finishLoad(IndicatorResult.fail);
    }
  }

  void dispose() {
    refreshController.dispose();
  }
}

// === View 层 ===
class PagedListPage extends StatefulWidget {
  const PagedListPage({super.key});
  @override State<PagedListPage> createState() => _PagedListPageState();
}

class _PagedListPageState extends State<PagedListPage> {
  late final PagedListViewModel _viewModel;

  @override
  void initState() {
    super.initState();
    _viewModel = PagedListViewModel()..loadFirstPage();
    _viewModel.addListener(() {
      if (mounted) setState(() {});
    });
  }

  @override
  void dispose() {
    _viewModel.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('分页列表')),
      body: _viewModel.initialLoading
          ? const Center(child: CircularProgressIndicator())
          : EasyRefresh(
              controller: _viewModel.refreshController,
              onRefresh: _viewModel.onRefresh,
              onLoad: _viewModel.onLoad,
              child: ListView.builder(
                itemCount: _viewModel.items.length,
                itemBuilder: (_, i) => ListTile(title: Text(_viewModel.items[i].name)),
              ),
            ),
    );
  }
}
```

> **关键原则**：EasyRefreshController 的声明 → ViewModel，调用 → ViewModel，dispose → ViewModel。View 层只做 Widget 组装，从 ViewModel 读取 controller 和方法引用。

---

## 目的二：强制使用 EasyRefreshController

### 2.1 核心规则 / Core Rule

> **凡使用 EasyRefresh，必须通过 EasyRefreshController 控制结束时机。Controller 的 `control*` 参数按场景区分：**

#### 场景 A：仅下拉刷新（无分页，无 onLoad）

```dart
// ✅ 正确 — 仅刷新
late final EasyRefreshController _controller = EasyRefreshController(
  controlFinishRefresh: true,  // 必须
  // controlFinishLoad 不设置（默认 false），因为没有 onLoad
);

EasyRefresh(
  controller: _controller,
  onRefresh: () async {
    // ...
    _controller.finishRefresh();
  },
  // 不设置 onLoad
  child: ListView.builder(/* ... */),
);

@override
void dispose() {
  _controller.dispose();
  super.dispose();
}
```

#### 场景 B：下拉刷新 + 上拉分页

```dart
// ✅ 正确 — 刷新 + 分页
late final EasyRefreshController _controller = EasyRefreshController(
  controlFinishRefresh: true,  // 必须
  controlFinishLoad: true,     // 必须（有分页时）
);

EasyRefresh(
  controller: _controller,
  onRefresh: () async {
    // ...
    _controller.finishRefresh();
    _controller.resetFooter();  // 分页场景必须
  },
  onLoad: () async {
    // ...
    _controller.finishLoad(IndicatorResult.noMore);
  },
  child: ListView.builder(/* ... */),
);

@override
void dispose() {
  _controller.dispose();
  super.dispose();
}
```

```dart
// ❌ 禁止：不使用 Controller
EasyRefresh(
  onRefresh: () async { },
  onLoad: () async { },
)
```

### 2.2 Controller 参数对照表

| 参数 | 仅刷新 | 刷新+分页 | 说明 |
|------|:------:|:---------:|------|
| `controlFinishRefresh` | ✅ true | ✅ true | 始终需要 |
| `controlFinishLoad` | ❌ 不设置 | ✅ true | 仅分页时需要 |
| `resetFooter()` | 不需要 | ✅ 必须 | 刷新后重置 |
| `dispose()` | ✅ | ✅ | 始终需要 |

### 2.3 Controller 生命周期

**场景 A：仅刷新**
```
创建 Controller（controlFinishRefresh: true）
    ▼
EasyRefresh(controller: _controller)
    │
    └── 下拉触发 → onRefresh()
          ├── 成功 → _controller.finishRefresh()
          └── 失败 → _controller.finishRefresh(IndicatorResult.fail)
    ▼
dispose() → _controller.dispose()
```

**场景 B：刷新 + 分页**
```
创建 Controller（controlFinishRefresh: true, controlFinishLoad: true）
    ▼
EasyRefresh(controller: _controller)
    │
    ├── 下拉触发 → onRefresh()
    │     ├── 成功 → _controller.finishRefresh()
    │     │         _controller.resetFooter()    ← ⚠️ 必须
    │     └── 失败 → _controller.finishRefresh(IndicatorResult.fail)
    │
    └── 上拉触发 → onLoad()
          ├── 成功有更多 → _controller.finishLoad()
          ├── 成功无更多 → _controller.finishLoad(IndicatorResult.noMore)
          └── 失败 → _page--, _controller.finishLoad(IndicatorResult.fail)
    ▼
dispose() → _controller.dispose()
```

### 2.4 Controller 方法速查

| 方法 | 何时调用 | 说明 |
|------|----------|------|
| `callRefresh()` | 外部按钮触发刷新 | 程序化触发下拉刷新动画 |
| `callLoad()` | 外部按钮触发加载 | 程序化触发上拉加载动画 |
| `finishRefresh([result])` | `onRefresh` 完成后 | 结束刷新动画，可传 `fail`/`success` |
| `finishLoad([result])` | `onLoad` 完成后 | 结束加载动画，可传 `noMore`/`fail` |
| `resetFooter()` | `finishRefresh()` 之后 | 重置 Footer 状态，**每次刷新后必须调用** |

### 2.5 分层架构中的 Controller 放置规则

当项目使用 ViewModel / Presenter / PageController 等业务逻辑层时：

```
┌─────────────────────────────────┐
│          View 层                 │
│  (StatefulWidget / StatelessWidget)│
│  - 读取 viewModel.controller     │
│  - 绑定 viewModel.onRefresh      │
│  - 绑定 viewModel.onLoad         │
│  - 不做 Controller 生命周期管理    │
└────────────┬────────────────────┘
             │ 持有引用
┌────────────▼────────────────────┐
│      ViewModel / Presenter 层    │
│  - 创建 EasyRefreshController   │ ← 创建
│  - 暴露 controller 给 View       │
│  - 实现 onRefresh() / onLoad()  │ ← 调用 finish* / resetFooter
│  - dispose() 释放 Controller    │ ← 回收
│  - 管理分页状态（page/hasMore）  │
└─────────────────────────────────┘
```

| 职责 | View 层 | ViewModel 层 |
|------|:---:|:---:|
| 创建 `EasyRefreshController` | ❌ | ✅ |
| 调用 `finishRefresh()` | ❌ | ✅ |
| 调用 `finishLoad()` | ❌ | ✅ |
| 调用 `resetFooter()` | ❌ | ✅ |
| 调用 `dispose()` 释放 | ❌ | ✅ |
| 管理分页状态 | ❌ | ✅ |
| 传递 `controller` 给 `EasyRefresh` | ✅ | — |
| 绑定 `onRefresh`/`onLoad` 回调 | ✅ | — |
| `setState` 驱动 UI 刷新 | ✅ | — |

> **核心规则**：Controller 的创建、finish* 调用、dispose 全部放在 ViewModel 层。View 层只做 `controller:` 和 `onRefresh:` 的绑定，不直接调用 Controller 方法。

---

## 目的三：自动生成 EasyRefreshConfig 本地化

### 3.1 语种检测规则 / Locale Detection

**核心原则：根据当前用户对话所使用的语言决定配置文本语种。**

按以下优先级检测语种（`zh` 或 `en`）：

| 优先级 | 检测方式 | 示例 |
|--------|----------|------|
| 🔴 **P0** | **用户对话语种** | 用户说中文 → `zh`；用户说英文 → `en` |
| 🟠 P1 | 检查项目中 `.arb` 文件命名 | `app_zh.arb` → `zh`；`app_en.arb` → `en` |
| 🟡 P2 | 检查 `MaterialApp` 的 `supportedLocales` / `locale` | `Locale('zh')` → `zh` |
| 🟢 P3 | 检查已有 `EasyRefresh.defaultHeaderBuilder` 文本语种 | 包含中文字符 → `zh` |
| 🔵 回退 | 默认 `zh` | — |

> **P0 规则详解**：生成 EasyRefreshConfig 时，直接根据用户当前对话的语言选择对应模板：
> - 用户在对话中使用**中文**（含任一中文字符）→ 生成中文版配置
> - 用户在对话中使用**英文**（无中文字符）→ 生成英文版配置

### 3.2 生成 EasyRefreshConfig 文件

**文件路径**: `lib/common/easy_refresh_config.dart`（如项目有特定公共目录则放在对应位置）

> **文件注释、Dartdoc 注释、字段名称全部跟随用户语种。** 文件注释用中文时，Dartdoc 也用中文；文件注释用英文时，Dartdoc 也用英文。

#### 用户使用中文 → 中文版本

```dart
/// EasyRefresh 本地化配置
///
/// 统一管理所有 Header/Footer 的提示文本。
/// 在 main() 中调用 [EasyRefreshConfig.init] 即可全局生效。
library;

import 'package:easy_refresh/easy_refresh.dart';

class EasyRefreshConfig {
  EasyRefreshConfig._();

  /// 初始化 EasyRefresh 全局本地化配置
  ///
  /// 应在 main() 函数中、runApp() 之前调用。
  static void init() {
    EasyRefresh.defaultHeaderBuilder = () => ClassicHeader(
      pulledText: '下拉刷新',
      hitText: '释放刷新',
      processingText: '正在刷新...',
      successText: '刷新成功',
      failedText: '刷新失败',
      safeArea: true,
    );
    EasyRefresh.defaultFooterBuilder = () => ClassicFooter(
      loadingText: '加载中...',
      noMoreText: '— 已经到底了 —',
      failedText: '加载失败，点击重试',
      safeArea: true,
    );
  }
}
```

#### 用户使用英文 → 英文版本

```dart
/// EasyRefresh localization configuration.
///
/// Manages all Header/Footer prompt text.
/// Call [EasyRefreshConfig.init] in main() for global effect.
library;

import 'package:easy_refresh/easy_refresh.dart';

class EasyRefreshConfig {
  EasyRefreshConfig._();

  /// Initialize EasyRefresh global localization.
  ///
  /// Should be called in main() before runApp().
  static void init() {
    EasyRefresh.defaultHeaderBuilder = () => ClassicHeader(
      pulledText: 'Pull to refresh',
      hitText: 'Release to refresh',
      processingText: 'Refreshing...',
      successText: 'Refresh succeeded',
      failedText: 'Refresh failed',
      safeArea: true,
    );
    EasyRefresh.defaultFooterBuilder = () => ClassicFooter(
      loadingText: 'Loading...',
      noMoreText: '— No more data —',
      failedText: 'Load failed, tap to retry',
      safeArea: true,
    );
  }
}
```

### 3.3 在 main() 中初始化

```dart
import 'package:flutter_easy_refresh/easy_refresh_config.dart'; // 调整路径

void main() {
  EasyRefreshConfig.init(); // ⚠️ 必须在 runApp 之前调用
  runApp(const MyApp());
}
```

### 3.4 完整集成示例 / Full Integration Example

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'app.dart';
import 'common/easy_refresh_config.dart';

void main() {
  EasyRefreshConfig.init();
  runApp(const MyApp());
}
```

---

## 完整标准模板 / Complete Standard Template

### 分页场景（刷新 + 上拉加载）

```dart
import 'package:easy_refresh/easy_refresh.dart';
import 'package:flutter_easy_refresh/easy_refresh_config.dart'; // 如已创建

class TemplateListPage extends StatefulWidget {
  const TemplateListPage({super.key});

  @override
  State<TemplateListPage> createState() => _TemplateListPageState();
}

class _TemplateListPageState extends State<TemplateListPage> {
  // === EasyRefresh Controller（强制） ===
  late final EasyRefreshController _controller = EasyRefreshController(
    controlFinishRefresh: true,
    controlFinishLoad: true,
  );

  // === 数据状态 ===
  final List<Item> _items = [];
  int _page = 1;
  static const int _pageSize = 20;
  bool _hasMore = true;
  bool _initialLoading = true;

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  void initState() {
    super.initState();
    _fetchFirstPage();
  }

  // ---- 数据获取 ----

  Future<void> _fetchFirstPage() async {
    try {
      final result = await api.getItems(page: 1, pageSize: _pageSize);
      if (!mounted) return;
      setState(() {
        _items.addAll(result.items);
        _hasMore = result.hasMore;
        _initialLoading = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() => _initialLoading = false);
    }
  }

  Future<void> _onRefresh() async {
    _page = 1;
    try {
      final result = await api.getItems(page: 1, pageSize: _pageSize);
      if (!mounted) return;
      setState(() {
        _items
          ..clear()
          ..addAll(result.items);
        _hasMore = result.hasMore;
      });
      _controller.finishRefresh();
      _controller.resetFooter();
    } catch (e) {
      if (!mounted) return;
      _controller.finishRefresh(IndicatorResult.fail);
    }
  }

  Future<void> _onLoad() async {
    if (!_hasMore) return;
    _page++;
    try {
      final result = await api.getItems(page: _page, pageSize: _pageSize);
      if (!mounted) return;
      setState(() {
        _items.addAll(result.items);
        _hasMore = result.hasMore;
      });
      _hasMore
          ? _controller.finishLoad()
          : _controller.finishLoad(IndicatorResult.noMore);
    } catch (e) {
      if (!mounted) return;
      _page--;
      _controller.finishLoad(IndicatorResult.fail);
    }
  }

  // ---- UI ----

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('列表')),
      body: _initialLoading
          ? const Center(child: CircularProgressIndicator())
          : EasyRefresh(
              controller: _controller,
              onRefresh: _onRefresh,
              onLoad: _onLoad,
              child: ListView.builder(
                itemCount: _items.length,
                itemBuilder: (context, index) {
                  return ListTile(title: Text(_items[index].name));
                },
              ),
            ),
    );
  }
}
```

### 仅刷新场景（无 onLoad，无分页）

```dart
import 'package:easy_refresh/easy_refresh.dart';
import 'package:flutter_easy_refresh/easy_refresh_config.dart'; // 如已创建

class RefreshOnlyPage extends StatefulWidget {
  const RefreshOnlyPage({super.key});

  @override
  State<RefreshOnlyPage> createState() => _RefreshOnlyPageState();
}

class _RefreshOnlyPageState extends State<RefreshOnlyPage> {
  // === EasyRefresh Controller（仅刷新） ===
  late final EasyRefreshController _controller = EasyRefreshController(
    controlFinishRefresh: true,
    // ⚠️ 不设置 controlFinishLoad
  );

  // === 数据状态 ===
  final List<Item> _items = [];
  bool _initialLoading = true;

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  void initState() {
    super.initState();
    _fetchData();
  }

  Future<void> _fetchData() async {
    try {
      final result = await api.getItems();
      if (!mounted) return;
      setState(() {
        _items = result;
        _initialLoading = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() => _initialLoading = false);
    }
  }

  Future<void> _onRefresh() async {
    try {
      final result = await api.getItems();
      if (!mounted) return;
      setState(() => _items = result);
      _controller.finishRefresh();
    } catch (e) {
      if (!mounted) return;
      _controller.finishRefresh(IndicatorResult.fail);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('列表')),
      body: _initialLoading
          ? const Center(child: CircularProgressIndicator())
          : EasyRefresh(
              controller: _controller,
              onRefresh: _onRefresh,
              child: ListView.builder(
                itemCount: _items.length,
                itemBuilder: (context, index) {
                  return ListTile(title: Text(_items[index].name));
                },
              ),
            ),
    );
  }
}
```

### ViewModel 架构 — 仅刷新

```dart
class RefreshViewModel {
  final EasyRefreshController controller = EasyRefreshController(
    controlFinishRefresh: true,
  );
  final List<Item> items = [];
  bool initialLoading = true;

  Future<void> loadData() async {
    initialLoading = true;
    try {
      items.addAll(await api.getItems());
    } finally {
      initialLoading = false;
    }
  }

  Future<void> onRefresh() async {
    try {
      final result = await api.getItems();
      items
        ..clear()
        ..addAll(result);
      controller.finishRefresh();
    } catch (e) {
      controller.finishRefresh(IndicatorResult.fail);
    }
  }

  void dispose() => controller.dispose();
  void addListener(VoidCallback listener) { /* ChangeNotifier 实现 */ }
}

class View extends StatelessWidget {
  // ... 绑定 _viewModel.controller / _viewModel.onRefresh
}
```

### ViewModel 架构 — 分页

```dart
class PagedViewModel {
  final EasyRefreshController controller = EasyRefreshController(
    controlFinishRefresh: true,
    controlFinishLoad: true,
  );
  final List<Item> items = [];
  int page = 1;
  bool hasMore = true;
  bool initialLoading = true;

  Future<void> loadFirstPage() async { /* ... */ }
  Future<void> onRefresh() async {
    page = 1;
    try {
      final result = await api.getItems(page: 1, pageSize: 20);
      items..clear()..addAll(result.items);
      hasMore = result.hasMore;
      controller.finishRefresh();
      controller.resetFooter();
    } catch (e) {
      controller.finishRefresh(IndicatorResult.fail);
    }
  }
  Future<void> onLoad() async {
    if (!hasMore) return;
    page++;
    try {
      final result = await api.getItems(page: page, pageSize: 20);
      items.addAll(result.items);
      hasMore = result.hasMore;
      hasMore
          ? controller.finishLoad()
          : controller.finishLoad(IndicatorResult.noMore);
    } catch (e) {
      page--;
      controller.finishLoad(IndicatorResult.fail);
    }
  }

  void dispose() => controller.dispose();
  void addListener(VoidCallback listener) { /* ChangeNotifier 实现 */ }
}
```

---

## 特殊场景适配 / Special Scenarios

### 嵌套滚动 (NestedScrollView)

```dart
EasyRefresh.builder(
  controller: _controller,
  onRefresh: _onRefresh,
  onLoad: _onLoad,
  childBuilder: (context, physics) {
    return NestedScrollView(
      physics: physics,                     // ⚠️ 必须
      headerSliverBuilder: (context, innerBoxIsScrolled) => [
        SliverAppBar(/* ... */),
      ],
      body: ListView.builder(
        physics: physics,                   // ⚠️ 内部也必须
        itemCount: _items.length,
        itemBuilder: (_, i) => ListTile(title: Text(_items[i].name)),
      ),
    );
  },
)
```

### Locator 定位指示器

```dart
EasyRefresh(
  controller: _controller,
  header: Header(position: IndicatorPosition.locator),
  footer: Footer(position: IndicatorPosition.locator),
  onRefresh: _onRefresh,
  onLoad: _onLoad,
  child: CustomScrollView(
    slivers: [
      SliverAppBar(/* ... */),
      const HeaderLocator.sliver(),
      SliverList(/* ... */),
      const FooterLocator.sliver(),
    ],
  ),
)
```

### cursor 分页（基于游标的分页）

```dart
String? _cursor;

Future<void> _onRefresh() async {
  _cursor = null;
  try {
    final result = await api.getItems(cursor: null, limit: _pageSize);
    if (!mounted) return;
    setState(() {
      _items
        ..clear()
        ..addAll(result.items);
      _cursor = result.nextCursor;
      _hasMore = result.hasMore;
    });
    _controller.finishRefresh();
    _controller.resetFooter();
  } catch (e) {
    if (!mounted) return;
    _controller.finishRefresh(IndicatorResult.fail);
  }
}

Future<void> _onLoad() async {
  if (!_hasMore) return;
  try {
    final result = await api.getItems(cursor: _cursor, limit: _pageSize);
    if (!mounted) return;
    setState(() {
      _items.addAll(result.items);
      _cursor = result.nextCursor;
      _hasMore = result.hasMore;
    });
    _hasMore
        ? _controller.finishLoad()
        : _controller.finishLoad(IndicatorResult.noMore);
  } catch (e) {
    if (!mounted) return;
    _controller.finishLoad(IndicatorResult.fail);
  }
}
```

---

## 最佳实践 / Best Practices

| # | 规则 | 说明 |
|---|------|------|
| 1 | Controller 参数按场景 | 有分页 → `controlFinishRefresh` + `controlFinishLoad` 均为 true；仅刷新 → 仅 `controlFinishRefresh: true` |
| 2 | 分页场景刷新后 resetFooter | `finishRefresh()` 后立即 `resetFooter()`，否则 noMore 残留 |
| 3 | 失败回退页码 | `_onLoad` 失败时 `_page--` |
| 4 | mounted 检查 | 所有异步回调 `setState` 前 `if (!mounted) return;` |
| 5 | 首次加载分离 | 用 `_initialLoading` 标志单独处理首次加载，不与 EasyRefresh 混用 |
| 6 | dispose 释放 | Controller 必须在 `dispose()` 中释放 |
| 7 | 配置文件检查 | 首次改造时检查是否存在 `easy_refresh_config.dart`，不存在则自动创建 |
| 8 | main() 初始化 | `EasyRefreshConfig.init()` 必须在 `runApp()` 之前调用 |
| 9 | 分层架构放置 | 有 ViewModel/Presenter 时，Controller 创建、finish* 调用、dispose 都放在业务逻辑层，View 层只做绑定 |

---

## 改造前置检查 / Pre-refactoring Checklist

在对页面进行 EasyRefresh 改造前，执行以下检查：

```
□ 1. pubspec.yaml 中是否存在 easy_refresh 依赖？
     否 → flutter pub add easy_refresh
□ 2. 页面代码中是否存在分页参数（page/offset/cursor）？
     否 → 仅需下拉刷新场景，按「仅刷新」模板改造
     是 → 按「刷新+分页」模板改造
□ 3. 项目中是否存在 easy_refresh_config.dart？
     否 → 检测语种 → 自动创建配置文件
     是 → 跳过
□ 4. main() 中是否调用了 EasyRefreshConfig.init()？
     否 → 添加调用
     是 → 跳过
□ 5. 页面是否已有 EasyRefresh？
     否 → 按对应场景模板改造
     是 → 检查 Controller 参数是否匹配场景（分页→双 true，仅刷新→仅 controlFinishRefresh），不符合则修正
```

---

## 常见问题 / FAQ

### Q1: 为什么必须使用 Controller？两个 control* 有什么区别？
不使用 Controller 时，EasyRefresh 会在 `onRefresh`/`onLoad` 的 Future 完成后自动结束动画。但这存在问题：
- 无法在异步回调中 `setState` 后再结束动画（状态更新与 UI 不同步）
- 无法精确控制失败/无更多等状态
- 刷新后无法调用 `resetFooter()`

**两个参数的使用规则：**

| 参数 | 仅刷新（无分页） | 刷新+分页 |
|------|:---:|:---:|
| `controlFinishRefresh: true` | ✅ | ✅ |
| `controlFinishLoad: true` | ❌ 不需要 | ✅ 必须 |

- **仅刷新页面**没有 `onLoad` 回调，设置 `controlFinishLoad: true` 无意义，保持默认 `false` 即可
- **分页页面**必须两者都为 `true`

### Q2: 如果页面已有 EasyRefresh 但没用 Controller？
→ 改造为 Controller 模式：添加 Controller 声明、dispose、将回调中的自动完成改为手动 `finish*`。

### Q3: 嵌套滚动/多滚动组件怎么办？
→ 使用 `EasyRefresh.builder` 并**必须**将 `physics` 传递给所有内部滚动组件。

### Q4: 项目同时支持中英文怎么办？/ 如何切换语种？
→ 配置生成时以用户对话语种为准。如项目需同时支持中英双语，EasyRefreshConfig 可接受 `locale` 参数，在 `MaterialApp` 切换语言时同步调用：

```dart
class EasyRefreshConfig {
  static void init({String locale = 'zh'}) {
    if (locale == 'en') {
      EasyRefresh.defaultHeaderBuilder = () => ClassicHeader(
        pulledText: 'Pull to refresh',
        hitText: 'Release to refresh',
        processingText: 'Refreshing...',
        successText: 'Refresh succeeded',
        failedText: 'Refresh failed',
        safeArea: true,
      );
      EasyRefresh.defaultFooterBuilder = () => ClassicFooter(
        loadingText: 'Loading...',
        noMoreText: '— No more data —',
        failedText: 'Load failed, tap to retry',
        safeArea: true,
      );
    } else {
      EasyRefresh.defaultHeaderBuilder = () => ClassicHeader(
        pulledText: '下拉刷新',
        hitText: '释放刷新',
        processingText: '正在刷新...',
        successText: '刷新成功',
        failedText: '刷新失败',
        safeArea: true,
      );
      EasyRefresh.defaultFooterBuilder = () => ClassicFooter(
        loadingText: '加载中...',
        noMoreText: '— 已经到底了 —',
        failedText: '加载失败，点击重试',
        safeArea: true,
      );
    }
  }
}

// 语言切换时重新调用
void onLocaleChange(String newLocale) {
  EasyRefreshConfig.init(locale: newLocale);
}
```

### Q5: 项目使用了 ViewModel / Presenter 架构，EasyRefreshController 放在哪里？
→ Controller 的创建、finish* 调用、dispose 全部放在 **ViewModel / Presenter 层**，View 层只做绑定。

```dart
// ✅ ViewModel 持有 Controller，管理完整生命周期
class MyViewModel {
  final EasyRefreshController controller = EasyRefreshController(
    controlFinishRefresh: true,
    controlFinishLoad: true,
  );

  Future<void> onRefresh() async {
    // ... 数据操作
    controller.finishRefresh();
    controller.resetFooter();
  }

  Future<void> onLoad() async {
    // ... 数据操作
    controller.finishLoad(IndicatorResult.noMore);
  }

  void dispose() => controller.dispose();
}

// ✅ View 层只绑定，不操作 Controller
// EasyRefresh(
//   controller: _viewModel.controller,
//   onRefresh: _viewModel.onRefresh,
//   onLoad: _viewModel.onLoad,
//   ...
// )
```

分层放置的原因：
- **单一职责**：View 负责 UI，ViewModel 负责业务逻辑和状态控制
- **可测试性**：Controller 和 finish* 逻辑在 ViewModel 中可以被单元测试覆盖
- **生命周期一致**：Controller 随 ViewModel 创建/销毁，避免 View 层重建导致的状态丢失

---

## 参考资源 / References

- **EasyRefresh 官方**: https://pub.dev/packages/easy_refresh
- **API 文档**: https://pub.dev/documentation/easy_refresh/latest/
- **GitHub**: https://github.com/xuelongqy/flutter_easy_refresh
- **分页辅助包**: https://pub.dev/packages/easy_paging
- **模式参考**: `references/easy_refresh_patterns.md` — 完整 API 参数速查表
