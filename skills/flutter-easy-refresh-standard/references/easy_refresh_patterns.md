# EasyRefresh 模式参考速查表 / Pattern Quick Reference

## EasyRefreshController 完整 API

```dart
late final EasyRefreshController _controller = EasyRefreshController(
  controlFinishRefresh: true,  // ⚠️ 标准化要求：必须为 true
  controlFinishLoad: true,     // ⚠️ 标准化要求：必须为 true
);

// 方法
_controller.callRefresh();                             // 触发刷新
_controller.callLoad();                                // 触发加载
_controller.finishRefresh([IndicatorResult? result]);  // 结束刷新
_controller.finishLoad([IndicatorResult? result]);     // 结束加载
_controller.resetFooter();                             // 重置 Footer（刷新后必须调用）
_controller.dispose();                                 // 释放资源
```

## IndicatorResult 枚举

| 值 | 含义 | Controller 用法 |
|---|------|-----------------|
| `IndicatorResult.success` | 成功 | `_controller.finishRefresh()` / `_controller.finishLoad()` |
| `IndicatorResult.fail` | 失败 | `_controller.finishRefresh(IndicatorResult.fail)` / `_controller.finishLoad(IndicatorResult.fail)` |
| `IndicatorResult.noMore` | 无更多数据 | `_controller.finishLoad(IndicatorResult.noMore)` |
| `IndicatorResult.none` | 无结果 | 极少使用 |
| `IndicatorResult.processed` | 已手动处理 | 极少使用 |

## 分页参数检测规则

以下参数名出现时判定为分页接口：

| 页码参数 | 条数参数 | 游标参数 | 偏移参数 |
|----------|----------|----------|----------|
| `page` | `pageSize` | `cursor` | `offset` |
| `pageNum` | `size` | `nextCursor` | `limit` |
| `current` | `limit` | `after` | `count` |
| `pageIndex` | `perPage` | `nextToken` |  |
| `p` | `ps` |  |  |

## ClassicHeader/ClassicFooter 本地化字段

### ClassicHeader

| 字段 | 中文 | English |
|------|------|---------|
| `pulledText` | 下拉刷新 | Pull to refresh |
| `hitText` | 释放刷新 | Release to refresh |
| `processingText` | 正在刷新... | Refreshing... |
| `successText` | 刷新成功 | Refresh succeeded |
| `failedText` | 刷新失败 | Refresh failed |
| `noMoreText` | 没有更多了 | No more |
| `safeArea` | `true` | `true` |

### ClassicFooter

| 字段 | 中文 | English |
|------|------|---------|
| `loadingText` | 加载中... | Loading... |
| `noMoreText` | — 已经到底了 — | — No more data — |
| `failedText` | 加载失败，点击重试 | Load failed, tap to retry |
| `safeArea` | `true` | `true` |

## 外部样式包速查

| 包名 | Header | Footer |
|------|--------|--------|
| `easy_refresh_bubbles` | `BubblesHeader()` | `BubblesFooter()` |
| `easy_refresh_space` | `SpaceHeader()` | `SpaceFooter()` |
| `easy_refresh_squats` | `SquatsHeader()` | `SquatsFooter()` |
| `easy_refresh_skating` | `SkatingHeader()` | `SkatingFooter()` |
| `easy_refresh_bow` | `BowHeader()` | `BowFooter()` |
| `easy_refresh_halloween` | `HalloweenHeader()` | `HalloweenFooter()` |

## 构造方式选择

| 场景 | 构造函数 | 说明 |
|------|----------|------|
| 单个 ListView/GridView | `EasyRefresh(child:)` | 最简单 |
| NestedScrollView / 嵌套滚动 / 多滚动组件 | `EasyRefresh.builder(childBuilder:)` | 必须传 `physics` |
| CustomScrollView 中指定指示器位置 | 任一 + `IndicatorPosition.locator` | 配合 `HeaderLocator.sliver()` |

## 改造对照表 / Before → After

| 原模式 | 改造后 |
|--------|--------|
| `_fetchData(int page)` 手动传 page | `_onRefresh()` + `_onLoad()` + Controller |
| build 中根据滚动位置触发加载 | EasyRefresh `onLoad` 回调 |
| 手动 `isLoading` 标志控制 loading 显示 | Controller `finish*` 自动管理动画 |
| 手动 `hasMore` 控制底部 loading widget | Controller `finishLoad(IndicatorResult.noMore)` |
| 无刷新后重置 Footer | `_controller.resetFooter()` |
