---
name: dart-generate-doc-comments
description: >
  为Dart代码生成全面的Dartdoc API文档注释。支持中英文（`--lang zh` / `--lang en`）。当用户创建/修改Dart文件、编写Dart代码、新增Dart类/函数/方法/枚举时自动调用。
  Generate comprehensive Dartdoc API documentation comments for Dart code. Supports both Chinese (--lang zh) and English (--lang en). Trigger on Dart file creation, modification, class/function/method/enum addition, etc.
---

# Dart 注释生成器 / Dart Doc Comment Generator

## 概述 / Overview

此skill为Dart代码自动生成Dartdoc API文档注释，**应在任何Dart开发活动中被调用**。支持**中文**和**英文**两种注释语言，通过 `--lang` 参数切换。

This skill automatically generates Dartdoc API documentation comments for Dart code and **should be invoked during any Dart development activity**. Supports both **Chinese** and **English** comment languages, switchable via the `--lang` parameter.

## 语言选择 / Language Selection

| 参数 | 语言 | 示例 |
|------|------|------|
| `--lang zh` | 中文（默认） | `python scripts/generate_dart_comments.py file.dart --lang zh` |
| `--lang en` | English (default when user prefers English) | `python scripts/generate_dart_comments.py file.dart --lang en` |

**AI 自动判断规则：** 根据用户使用的语言自动选择 `--lang` 参数。用户使用中文则生成中文注释，使用英文则生成英文注释。

**AI auto-detection:** Automatically select `--lang` based on the user's language. Use `--lang zh` when the user writes in Chinese, `--lang en` when the user writes in English.

## 快速开始 / Quick Start

### 基本用法 / Basic Usage

```bash
# 为单个文件生成注释（中文默认）/ Generate comments for a single file (Chinese by default)
python scripts/generate_dart_comments.py path/to/file.dart

# 生成英文注释 / Generate English comments
python scripts/generate_dart_comments.py path/to/file.dart --lang en

# 生成中文注释（显式指定）/ Generate Chinese comments (explicit)
python scripts/generate_dart_comments.py path/to/file.dart --lang zh

# 生成注释并保存到不同文件 / Generate and save to different file
python scripts/generate_dart_comments.py path/to/file.dart output.dart --lang en
```

### 手动生成文档 / Manual Documentation Generation

当自动生成不适用时，使用以下指南 / When automatic generation is not applicable, use these guidelines:

1. **阅读Dartdoc格式参考 / Read the Dartdoc format reference**：参见 `references/dartdoc_format.md`
2. **识别可文档化元素 / Identify documentable elements**：函数、方法、类、枚举 / functions, methods, classes, enums
3. **生成文档 / Generate documentation**：遵循模板和最佳实践 / Follow templates and best practices
4. **插入注释 / Insert comments**：将文档放置在每个元素上方 / Place documentation above each element

## 工作流程 / Workflow

### 步骤1：分析Dart文件 / Step 1: Analyze Dart File

```bash
python scripts/generate_dart_comments.py path/to/file.dart
```

脚本将 / The script will:
1. 解析Dart文件 / Parse the Dart file
2. 识别所有可文档化元素 / Identify all documentable elements
3. 根据 `--lang` 参数生成相应语言的Dartdoc注释 / Generate Dartdoc comments in the selected language
4. 在每个元素上方插入注释 / Insert comments above each element

### 步骤2：审查和完善 / Step 2: Review and Refine

生成后 / After generation：
1. 审查生成的注释以确保准确性 / Review generated comments for accuracy
2. 在需要时增强描述 / Enhance descriptions where needed
3. 为复杂API添加具体示例 / Add concrete examples for complex APIs
4. 确保参数文档清晰 / Ensure parameter documentation is clear

## 基于任务的操作 / Task-Based Operations

### 为单个文件生成 / Generate for Single File

```bash
# 中文 / Chinese
python scripts/generate_dart_comments.py lib/models/user.dart

# 英文 / English
python scripts/generate_dart_comments.py lib/models/user.dart --lang en
```

### 为多个文件生成 / Generate for Multiple Files

```bash
# 中文 / Chinese
find lib -name "*.dart" -exec python scripts/generate_dart_comments.py {} --lang zh \;

# 英文 / English
find lib -name "*.dart" -exec python scripts/generate_dart_comments.py {} --lang en \;
```

### 生成到单独目录 / Generate to Separate Directory

```bash
python scripts/generate_dart_comments.py lib/ lib_documented/ --lang en
```

## 文档标准 / Documentation Standards

### 文件头元数据（仅新文件）/ File Header Metadata (New Files Only)

当处理一个**新创建的 Dart 文件**（即文件中没有任何 `///` 文档注释）时，必须在文件顶部添加文件头。

For **newly created Dart files** (no existing `///` doc comments), a file header must be added at the top.

格式 / Format：

```dart
///
/// @author {authorName}
/// @created {YYYY-MM-DD HH:mm:ss}
///
/// {file_description}
///
```

- **@author**：创建人（从 `git config user.name` 自动获取）/ Author (auto-detected from `git config user.name`)
- **@created**：创建时间（格式 `YYYY-MM-DD HH:mm:ss`）/ Creation time (format `YYYY-MM-DD HH:mm:ss`)
- **@description**：文件用途简述 / Brief description of the file's purpose

判断"新文件"的标志：文件中不存在任何 `///` 开头的注释行。对于已有文档注释的旧文件，不添加此文件头。

Indicator of a "new file": no lines starting with `///` exist. For existing files with doc comments, this header is skipped.

### 特定元素的文档 / Element-Specific Documentation

#### 函数和方法 / Functions & Methods
- **描述 / Description**：功能 / What it does
- **参数 / Parameters**：每个参数的用途 / Purpose of each parameter
- **返回值 / Return**：返回的内容 / What it returns
- **异常 / Exceptions**：何时抛出异常 / When exceptions are thrown
- **示例 / Example**：复杂函数的使用示例 / Usage examples for complex functions

#### 类 / Classes
- **描述 / Description**：目的和职责 / Purpose and responsibilities
- **属性 / Properties**：关键属性及其含义 / Key properties and their meaning
- **方法 / Methods**：公共方法概述 / Overview of public methods
- **用法 / Usage**：如何使用该类 / How to use the class

#### 枚举 / Enums
- **描述 / Description**：枚举代表什么 / What the enum represents
- **值 / Values**：每个枚举值的含义 / Meaning of each enum value

### 质量指南 / Quality Guidelines

1. **简洁 / Be concise**：保持描述简短但信息丰富 / Keep descriptions short but informative
2. **使用完整句子 / Use complete sentences**：以大写字母开头 / Start with a capital letter
3. **记录非显而易见的行为 / Document non-obvious behavior**：关注代码中不明确的内容 / Focus on what's not obvious from the code
4. **包含示例 / Include examples**：展示如何使用复杂API / Show how to use complex APIs
5. **使用引用 / Use references**：链接到相关类和方法 / Link to related classes and methods
6. **新文件添加文件头 / Add file header for new files**：自动添加 `@author` 和 `@created` / Auto-add `@author` and `@created`

## 资源 / Resources

### scripts/
- `generate_dart_comments.py` - 生成Dartdoc注释的主脚本 / Main script for generating Dartdoc comments

### references/
- `dartdoc_format.md` - 完整的Dartdoc格式参考和模板（中英双语）/ Complete Dartdoc format reference and templates (bilingual)

## 高级用法 / Advanced Usage

### 自定义模板 / Custom Templates

自定义文档生成 / Customize documentation generation：
1. 编辑 `scripts/generate_dart_comments.py` / Edit `scripts/generate_dart_comments.py`
2. 修改 `STRINGS` 字典中的模板或添加新语言 / Modify templates in the `STRINGS` dict or add new languages
3. 调整 `_generate_*` 方法中的生成逻辑 / Adjust generation logic in `_generate_*` methods

### 添加新语言 / Adding a New Language

在 `STRINGS` 字典中添加新语言的键，包含所有必需的字符串模板：

Add a new language key to the `STRINGS` dict with all required string templates:

```python
STRINGS['ja'] = {
    'file_header_desc': '{name} モジュール。',
    'class_desc': '{words} クラス。',
    # ... 所有必需的键 / all required keys
}
```

### 与CI/CD集成 / CI/CD Integration

```yaml
# GitHub Actions步骤示例 / Example GitHub Actions step
- name: 生成文档 / Generate Docs
  run: |
    find lib -name "*.dart" -exec python scripts/generate_dart_comments.py {} --lang en \;
```

### 批量处理 / Batch Processing

```bash
# 为所有Dart文件生成英文文档 / Generate English docs for all Dart files
find . -name "*.dart" -type f -exec python scripts/generate_dart_comments.py {} --lang en \;

# 为所有Dart文件生成中文文档 / Generate Chinese docs for all Dart files
find . -name "*.dart" -type f -exec python scripts/generate_dart_comments.py {} --lang zh \;
```

## 故障排除 / Troubleshooting

### 常见问题 / Common Issues

1. **脚本未找到 / Script not found**：确保在skill目录中或使用完整路径 / Ensure you're in the skill directory or using the full path
2. **权限错误 / Permission error**：使用 `chmod +x` 使脚本可执行 / Use `chmod +x` to make the script executable
3. **解析错误 / Parse error**：生成前检查Dart文件语法 / Check Dart file syntax before generation
4. **UnicodeDecodeError（GBK编码错误）**：脚本已使用 `encoding='utf-8'` 打开文件，AI内联处理时也需使用 `encoding='utf-8'`
5. **语言不支持 / Unsupported language**：使用 `--lang en` 或 `--lang zh`，不支持的代码将回退到中文

## 示例 / Examples

### 英文生成示例 / English Generation Example

**之前 / Before:**
```dart
class Calculator {
  int add(int a, int b) {
    return a + b;
  }
}
```

**之后 (`--lang en`) / After:**
```dart
/// Represents a calculator for performing arithmetic operations.
class Calculator {
  /// Adds two numbers together.
  ///
  /// * [a] The first number to add.
  /// * [b] The second number to add.
  ///
  /// Returns the sum of [a] and [b].
  ///
  /// Example:
  /// ```dart
  /// final calculator = Calculator();
  /// final result = calculator.add(2, 3);
  /// print(result); // 5
  /// ```
  int add(int a, int b) {
    return a + b;
  }
}
```

### 中文生成示例 / Chinese Generation Example

**之后 (`--lang zh`) / After:**
```dart
///
/// @author San Zhang
/// @created 2026-06-25 17:03:00
///
/// calculator 模块。
///

/// calculator 类。
class Calculator {
  /// add。
  ///
  /// * [a] 要使用的a。
  /// * [b] 要使用的b。
  ///
  /// 返回 int 类型的结果。
  ///
  /// 示例：
  /// ```dart
  /// final result = instance.add(0, 0);
  /// ```
  int add(int a, int b) {
    return a + b;
  }
}
```
