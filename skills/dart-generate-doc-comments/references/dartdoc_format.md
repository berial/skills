# Dartdoc 格式参考 / Dartdoc Format Reference

本文件是 `dart-generate-doc-comments` skill 的格式速查与中英写作指南。核心原则：**宁可少写，不要写废话。**

This file is the format quick-reference and EN/ZH writing guide for the `dart-generate-doc-comments` skill. Core principle: **prefer writing nothing over writing noise.**

---

## 第一原则：避免无用注释 / First Principle: Avoid Useless Comments

Dartdoc 的价值在于补充**代码本身看不出来**的信息。下列注释属于噪声，一律删除或改写：

Dartdoc is valuable only when it adds facts **not obvious from the code**. The following are noise — delete or rewrite them:

| 噪声模式 / Noise pattern | 问题 / Problem |
|--------------------------|----------------|
| 复述标识符 / Restates identifier | `/// Is adult.` on `bool get isAdult` —— 名字已说明 |
| 复述参数类型 / Restates param type | `/// [page] The page.` on `int page` —— 签名已写明 |
| 复述返回类型 / Restates return type | `/// Returns the result as String.` —— 签名已有 `String` |
| 凑数假示例 / Fake example | `instance.add(0, 0)` —— 不能编译、无意义 |
| javadoc 标签 / javadoc tags | `@author` / `@created` / `@param` —— 非 Dartdoc 规范 |

**判断口诀**：删掉这条注释，读者会不会漏掉某个"代码本身看不出来"的事实？会→写；不会→删。

---

## 何时跳过 / When to Skip

默认对自明代码不写注释 / By default, do not comment self-explanatory code：

- 方法名/字段名已说明用途（`getDisplayName()`、`isAdult`、`User.name`）
- 参数文档只是重复类型
- 返回值只是复述类型
- 简单 getter / setter / 纯委托
- 构造函数只是赋值字段
- 纯数据类字段（除非有约束）

---

## 何时该写 / When to Write

只有当注释能补充代码没说清楚的信息时才写 / Only when the comment adds facts the code does not make clear：

- **真实用途/意图**：名字不够直观，或方法做了非显然的事
- **前置条件 / 约束**：`page` 必须 ≥ 1；`width` 单位是逻辑像素
- **单位 / 格式**：Unix 毫秒还是秒；金额单位；经纬度还是屏幕像素
- **副作用**：修改外部状态、写文件、发起网络请求、触发通知
- **异常**：何时抛出哪种异常
- **边界 / 空安全**：`null` 代表什么；列表可能为空；越界行为
- **复杂算法 / 协议**：缓存策略、重试逻辑、分页协议、排序稳定性

---

## 基本结构 / Basic Structure

```dart
/// 首行：简短的一句话摘要（不超过一行）。/ One-line summary.
///
/// 可选的详细说明，仅在有内容时才写。/ Optional details, only when there's content.
///
/// * [paramName] 参数用途（仅当非显然时）。/ Param purpose (only when non-obvious).
///
/// 返回值说明（仅当返回值有非显然语义时）。/ Return value (only when non-obvious).
///
/// 示例：（仅对非平凡 API）/ Example: (non-trivial APIs only)
/// ```dart
/// final result = add(2, 3);
/// ```
```

---

## 文档标签 / Documentation Tags

### 基础 / Basic
- `///` — 文档注释（Dart 用 `///`，不用 `/** */`）/ Doc comment (use `///`, not `/** */`)
- `[Name]` — 引用类、方法、参数、库，生成可点击链接 / Reference a class/method/param/library, renders as a link
- `* [paramName] ...` — 参数列表（Markdown 列表）/ Param list (Markdown list)

### 不要使用 / Do NOT use
- ❌ `@author` / `@created` —— javadoc 标签，不属于 Dartdoc
- ❌ `/** */` —— Dart 中较少使用
- ❌ `@param` / `@return` —— 用 `* [param]` 和 `Returns ...` 文本代替

---

## 文件级说明 / File-level Docs

**不使用** `@author` / `@created` 文件头。如确需说明整个库用途，用 Dartdoc 的 `library;` 段（可选）：

Do **not** add `@author` / `@created` headers. If a library's purpose truly needs stating, use the Dartdoc `library;` directive (optional):

```dart
/// 提供用户资料相关的数据模型与服务。
/// Provides data models and services for user profiles.
library user_profile;

import 'package:flutter/material.dart';
```

多数文件不需要文件级注释。只有当用途从文件名/内容看不出时才写。

---

## 模板示例 / Template Examples

### 有信息量的函数文档 / Informative Function Docs

```dart
/// 计算两个数的和。
/// Calculates the sum of two numbers.
///
/// * [a] 第一个加数。 / The first addend.
/// * [b] 第二个加数。 / The second addend.
///
/// 返回 [a] 与 [b] 的和。 / Returns the sum of [a] and [b].
int add(int a, int b) => a + b;
```

> 注：`add` 本身已较自明，这里仅为展示格式。真实场景中，只有当存在溢出、特殊取值等约束时才值得写。

### 有信息量的类文档 / Informative Class Docs

```dart
/// 表示系统中的一个用户。 / Represents a user in the system.
///
/// 不可变；通过 [User.copy] 或工厂方法产生新实例。 / Immutable; produce new instances via [User.copy] or factories.
class User {
  final String id;
  final String name;

  const User({required this.id, required this.name});
}
```

### 有信息量的枚举文档 / Informative Enum Docs

```dart
/// 表示任务的状态。 / Represents the status of a task.
enum TaskStatus {
  /// 任务尚未开始。 / The task has not yet started.
  pending,

  /// 任务进行中。 / The task is currently in progress.
  inProgress,

  /// 任务已成功完成。 / The task completed successfully.
  completed,
}
```

---

## 语言特定规范 / Language-Specific Guidelines

### 英文 / English
1. 首行简短摘要，首字母大写，第三人称单数："Calculates...", "Represents...", "Creates..."
2. 参数说明用 "The" 前缀且必须有信息增量："The 1-based page index (≥1)."
3. 返回值："Returns the..." 或 "A [type] representing..."
4. 示例标签用 ASCII 冒号：`Example:`

### 中文 / Chinese
1. 首行简短摘要，句号结尾，动词短语："计算..."、"表示..."、"创建..."
2. 参数说明用"要..."且必须有信息增量："从 1 开始的页码（≥1）。"
3. 返回值："返回..."开头
4. 示例标签用全角冒号：`示例：`

---

## 最佳实践 / Best Practices

1. **信息增量优先 / Information density first**：注释必须补充代码未表达的事实
2. **首行简短 / Short first line**：一句话摘要，便于 IDE 悬浮预览
3. **第三人称 / Third person**：英文用单数，中文用动词短语
4. **引用代替重复 / Reference, don't restate**：用 `[ClassName]` 而非重新描述
5. **示例仅在非平凡时写 / Examples only when non-trivial**：且必须能编译、参数真实
6. **同一文件语种统一 / Consistent language**：不要中英混用
