# Dart Doc Comments / Dart 文档注释

> Auto-generate **informative** Dartdoc (`///`) comments inline for Dart/Flutter code — only where they add value, skipping self-explanatory code.
> 为 Dart/Flutter 代码内联生成**有信息量**的 Dartdoc（`///`）注释——只在有价值时写，自动跳过自明代码。

[![Skill](https://img.shields.io/badge/skill-dart--generate--doc--comments-blue)](SKILL.md)

---

## 核心理念 / Core Idea

此 skill 不是机械套模板的代码生成器——它指导 AI 在**写/改完 Dart 代码后**，**内联**补充有意义的文档注释。关键在于：**宁可少写，不要写废话。**

This is not a mechanical template generator — it guides the AI to add **meaningful** doc comments **inline after writing/editing Dart code**. The key: **prefer writing nothing over writing noise.**

---

## 何时自动触发 / When It Auto-activates

AI 创建、编写、编辑、脚手架生成任何 Dart 文件后自动生效，即使用户没提到"注释/文档"。语言跟随用户对话语种（中文→`zh`，英文→`en`）。

Activates automatically after the AI creates, writes, edits, or scaffolds any Dart file — even if the user never mentions "docs" or "comments". Language follows the conversation (Chinese→`zh`, English→`en`).

---

## 何时跳过 / When to Skip

默认对自明代码不写注释：

- 方法名/字段名已说明用途（`getDisplayName()`、`isAdult`、`User.name`）
- 参数文档只是重复类型（`/// [page] The page.`）
- 返回值只是复述类型（`/// Returns the result as String.`）
- 简单 getter / setter / 纯委托
- 构造函数只是赋值字段
- 纯数据类字段

## 何时该写 / When to Write

只有当注释能补充代码没说清楚的信息时才写：

- 真实用途/意图、前置条件/约束
- 单位/格式（Unix 毫秒 vs 秒、逻辑像素、经纬度）
- 副作用、异常、边界/空安全行为
- 复杂算法/协议（缓存、重试、分页、排序稳定性）

---

## 示例对比 / Example

### 自明方法 → 不写 / Self-explanatory → Skip

```dart
class User {
  final String name;
  final int age;

  // ❌ 不要写这种复述式注释 / No restating comments
  String getDisplayName() => name;

  // ✅ 自明，保持干净 / Self-explanatory, keep clean
  bool get isAdult => age >= 18;
}
```

### 分页 API → 写（有真实约束）/ Paginated API → Write (real constraints)

```dart
// 中文对话 / Chinese conversation
class ItemRepository {
  /// 拉取一页数据。
  ///
  /// [page] 从 1 开始计数，传 0 或负数会抛出 [ArgumentError]。
  /// [pageSize] 每页条数，上限 100。
  ///
  /// 超出最后一页时返回**空列表**而非抛异常——
  /// 调用方应据此判断是否已到底部。
  Future<List<Item>> fetchItems({required int page, int pageSize = 20}) async {
    // ...
  }
}
```

```dart
// English conversation
class ItemRepository {
  /// Fetches a single page of items.
  ///
  /// [page] is 1-based; passing 0 or a negative value throws [ArgumentError].
  /// [pageSize] caps at 100.
  ///
  /// Returns an **empty list** (never throws) when [page] is past the last
  /// page — callers should treat that as "no more data".
  Future<List<Item>> fetchItems({required int page, int pageSize = 20}) async {
    // ...
  }
}
```

---

## 文件结构 / Structure

| 文件 / File | 说明 / Purpose |
|-------------|----------------|
| [SKILL.md](SKILL.md) | 主指令：触发条件、跳过/写规则、工作流 / Main directives |
| [references/dartdoc_format.md](references/dartdoc_format.md) | 格式速查、噪声清单、中英写作指南 / Format reference |
| [agents/openai.yaml](agents/openai.yaml) | 触发接口配置 / Interface config |

---

## License

MIT
