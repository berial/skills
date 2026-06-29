---
name: dart-generate-doc-comments
description: >
  Generate comprehensive Dartdoc API documentation comments (/// ...) for Dart and Flutter code. Use this skill AFTER you create, write, edit, or scaffold any Dart (.dart) source file — including when writing new classes, functions, methods, constructors, enums, mixins, extensions, typedefs, or top-level declarations. Trigger automatically whenever you finish producing or modifying Dart/Flutter code for the user: building a feature, adding a widget/model/service, implementing a method, refactoring, or converting design to code — even if the user never mentions "docs" or "comments". Pick `--lang zh` when the user writes Chinese, `--lang en` when they write English.
  为 Dart / Flutter 代码生成完整的 Dartdoc API 文档注释（///）。当你为用户**创建、编写、编辑、脚手架生成任何 Dart (.dart) 文件后必须调用**——新增类、函数、方法、构造函数、枚举、mixin、extension、typedef、顶层声明时同样适用。只要你在为用户产出或修改 Dart/Flutter 代码（实现功能、加 widget/model/service、实现方法、重构、把设计转成代码）就应自动触发，即使用户完全没提到"文档""注释"。用户用中文则 `--lang zh`，用英文则 `--lang en`。
---

# Dart 注释生成 / Dart Doc Comments

## 概述 / Overview

此 skill 在 AI **写完或改完 Dart 代码后自动生效**：为代码内联补充**有信息量**的 Dartdoc 文档注释。它**不是**机械套模板——AI 必须读懂代码意图后再决定写什么、**以及要不要写**。

This skill activates automatically **after the AI writes or edits Dart code**: it adds **informative** Dartdoc comments inline. It is **not** mechanical templating — the AI must understand the code's intent before deciding what to write and **whether to write at all**.

核心原则 / Core principle：

> **宁可少写，不要写废话。** 一条注释若只是复述了名字、参数类型或返回类型，就是噪声，必须删掉或改成有信息量的说明。

> **Prefer writing nothing over writing noise.** A comment that merely restates an identifier, a parameter type, or a return type is noise — delete it or rewrite it to add real information.

---

## 第一原则：什么时候【不要】写注释 / When NOT to Write

**默认对"自明"的代码不写注释。** 只有当注释能补充代码本身无法表达的信息时才写。遇到以下情况一律跳过：

- **方法名/字段名已说明用途**：`getDisplayName()`、`isAdult()`、`User.name` —— 不写。
- **参数文档只是重复类型**：`/// [page] The page.`（`int page` 已经写明是 int）—— 不写。
- **返回值只是复述类型**：`/// Returns the result as String.` —— 不写；签名里已有 `String`。
- **简单 getter / setter / 纯委托**：直接转发到字段或单次调用 —— 不写。
- **构造函数只是赋值字段**：`User({required this.id, required this.name});` —— 不写。
- **纯数据类字段**（除非有约束，见下）。

---

## 什么时候【应该】写 / When to Write

只有当注释能补充**代码没说清楚**的信息时才写。常见值得写的情况：

| 信息类型 | 举例 |
|----------|------|
| **真实用途/意图** | 名字不够直观，或方法做了非显然的事（如 `fetchItems` 其实是"分页拉取，page 从 1 开始"） |
| **前置条件 / 约束** | `[page]` 必须 ≥ 1；`width` 单位是逻辑像素；`id` 不可为空字符串 |
| **单位 / 格式** | 时间戳是 Unix 毫秒还是秒；金额单位；坐标是经纬度还是屏幕像素 |
| **副作用** | 方法会修改外部状态、写文件、发起网络请求、触发通知 |
| **异常** | 何时抛出哪种异常、抛出的条件 |
| **边界 / 空安全** | `null` 返回值代表什么；列表可能为空；越界行为 |
| **复杂算法 / 协议** | 缓存策略、重试逻辑、分页协议、排序稳定性 |

**判断口诀**：如果删掉这条注释，读者会不会漏掉某个"代码本身看不出来"的事实？会 → 写；不会 → 删。

---

## 语言选择 / Language

按**用户对话所用语言**自动决定注释语言，无需用户指定：

| 用户对话语言 | 注释语言 | 文档标签 |
|--------------|----------|----------|
| 中文 | 中文 | `示例：`（全角冒号）|
| 英文 | 英文 | `Example:`（ASCII 冒号）|

- 用户用中文 → 全部注释用中文，第三人称动词短语，如"拉取分页数据。"
- 用户用英文 → 全部注释用英文，第三人称单数，如"Fetches a page of items."
- **同一文件内不要中英混用。**

---

## 工作流程 / Workflow

每次写/改完 Dart 代码后，按以下步骤自检：

```
1. 通读刚写/改的每个公开声明（类、函数、方法、枚举、顶层声明）
2. 对每个声明问："删掉注释，读者会漏掉非显然的事实吗？"
   → 否 → 不写注释（保持代码干净）
   → 是 → 写一条【有信息量】的注释（见"什么时候应该写"）
3. 已有的复述式注释 → 删除或改写为有信息量版本
4. 语言跟随用户对话语种（zh / en）
5. 跑 dart analyze 确认注释没有引入警告
```

**关键：不要为了"覆盖每个元素"而批量堆砌注释。** 公开 API 通常更需要文档，私有实现细节通常不需要。

---

## Dartdoc 格式规范 / Format

### 基本结构

```dart
/// 首行：简短的一句话摘要（不超过一行）。
///
/// 可选的详细说明：补充上下文、约束、行为。仅在有内容时才写。
///
/// * [paramName] 参数用途（仅当用途非显然时）。
///
/// 返回值说明（仅当返回值有非显然语义时）。
///
/// 示例：（仅对非平凡 API）
/// ```dart
/// final r = add(2, 3);
/// ```
```

### 标签速查

- `///` — 文档注释（Dart 用 `///`，不用 `/** */`）。
- `[Name]` — 引用类、方法、参数、库（生成可点击链接）。
- `* [paramName] ...` — 列出参数（Markdown 列表）。
- 不要用 javadoc 的 `@author` / `@created` / `@param` —— 它们不属于 Dartdoc 规范。

### 示例：仅对非平凡 API 才加

只在 API 用法不直观时才写示例，且示例**必须能编译、有意义**（用真实变量名，凑数参数如 `0, 0` 不算）。简单方法不写示例。

---

## 文件级说明 / File-level docs

**不使用** javadoc 风格的 `@author` / `@created` 文件头。如确需说明整个库的用途，用 Dartdoc 规范的 `library;` 段（可选，非强制）：

```dart
/// 提供用户资料相关的数据模型与服务。
library user_profile;

import 'package:flutter/material.dart';
// ...
```

只有当库的用途从文件名/内容看不出、或需要说明模块边界时才写。多数文件不需要文件级注释。

---

## 示例对比 / Examples

### 例 1：自明方法 → 不写

```dart
class User {
  final String name;
  final int age;

  // ❌ 不要写这种复述式注释：
  // /// Get display name.
  // /// 返回 String 类型的结果。
  // String getDisplayName() => name;

  // ✅ 自明，保持干净
  String getDisplayName() => name;

  // ✅ 自明，保持干净
  bool get isAdult => age >= 18;
}
```

### 例 2：构造函数只赋值字段 → 不写

```dart
// ✅ 无需注释，签名已说明一切
class User {
  const User({required this.id, required this.name});
  final String id;
  final String name;
}
```

### 例 3：分页 API → 写（有真实约束）

```dart
// 中文对话输出
class ItemRepository {
  /// 拉取一页数据。
  ///
  /// [page] 从 1 开始计数，传 0 或负数会抛出 [ArgumentError]。
  /// [pageSize] 每页条数，上限 100。
  ///
  /// 当 [page] 超出最后一页时返回**空列表**而非抛异常——
  /// 调用方应据此判断是否已到底部。
  ///
  /// 示例：
  /// ```dart
  /// final first = await repo.fetchItems(page: 1, pageSize: 20);
  /// ```
  Future<List<Item>> fetchItems({required int page, int pageSize = 20}) async {
    // ...
  }
}
```

```dart
// English conversation output
class ItemRepository {
  /// Fetches a single page of items.
  ///
  /// [page] is 1-based; passing 0 or a negative value throws [ArgumentError].
  /// [pageSize] caps at 100.
  ///
  /// Returns an **empty list** (never throws) when [page] is past the last
  /// page — callers should treat that as "no more data".
  ///
  /// Example:
  /// ```dart
  /// final first = await repo.fetchItems(page: 1, pageSize: 20);
  /// ```
  Future<List<Item>> fetchItems({required int page, int pageSize = 20}) async {
    // ...
  }
}
```

> 对比：例 3 的注释补充了**代码本身看不出来**的事实（1-based、上限 100、超页返回空而非抛异常），所以有价值。如果方法只是 `add(a, b)`，就什么都不写。

### 例 4：枚举值需要含义时 → 写

```dart
// ❌ 自明，不写
enum SortOrder { ascending, descending }

// ✅ 值含义不直观，写
enum HttpStatusCode {
  /// 请求成功。
  ok200,

  /// 资源不存在。
  notFound404,

  /// 服务器内部错误。
  internalError500,
}
```

---

## 自检清单 / Self-check

写完注释后逐条确认：

- [ ] 每条注释都补充了"代码本身看不出来"的信息？（没有复述名字/类型）
- [ ] 自明的方法/getter/setter/构造函数**没有**注释？
- [ ] 语言与用户对话语种一致，无中英混用？
- [ ] 示例（若有）能编译、用了真实参数？
- [ ] 没有用 `@author` / `@created` 等 javadoc 标签？
- [ ] `dart analyze` 无新增警告？

---

## 参考 / Reference

完整格式规范与中英写作指南见 [references/dartdoc_format.md](references/dartdoc_format.md)。
