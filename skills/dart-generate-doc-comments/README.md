# Dart Doc Comment Generator / Dart 注释生成器

> Generate comprehensive Dartdoc API documentation comments for Dart code.
> 为 Dart 代码自动生成全面的 Dartdoc API 文档注释。

[![Python](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## Features / 特性

- 🌐 **Bilingual support** — English (`--lang en`) and Chinese (`--lang zh`) comment generation
- 📄 **Auto-detect new files** — Adds `@author` / `@created` headers for new Dart files
- 🧩 **Comprehensive coverage** — Classes, enums, functions, methods, constructors
- 📝 **Parameter & return documentation** — Auto-generated from function signatures
- 💡 **Usage examples** — Auto-generated code examples for methods with parameters
- 🔧 **Extensible** — Add new languages by extending the `STRINGS` dictionary

## Quick Start / 快速开始

```bash
# Generate Chinese comments (default)
python scripts/generate_dart_comments.py path/to/file.dart

# Generate English comments
python scripts/generate_dart_comments.py path/to/file.dart --lang en

# Generate and save to different file
python scripts/generate_dart_comments.py path/to/file.dart output.dart --lang en
```

## Example / 示例

### Before / 之前

```dart
class Calculator {
  int add(int a, int b) {
    return a + b;
  }
}
```

### After (English) / 之后（英文）

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
  /// final result = instance.add(0, 0);
  /// ```
  int add(int a, int b) {
    return a + b;
  }
}
```

### After (Chinese) / 之后（中文）

```dart
/// calculator 类。
class Calculator {
  /// add。
  ///
  /// * [a] 要使用的 a。
  /// * [b] 要使用的 b。
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

## Batch Processing / 批量处理

```bash
# Generate English docs for all Dart files
find lib -name "*.dart" -exec python scripts/generate_dart_comments.py {} --lang en \;

# Generate Chinese docs for all Dart files
find lib -name "*.dart" -exec python scripts/generate_dart_comments.py {} --lang zh \;
```

## Adding a New Language / 添加新语言

Extend the `STRINGS` dictionary in `scripts/generate_dart_comments.py`:

```python
STRINGS['ja'] = {
    'file_header_desc': '{name} モジュール。',
    'class_desc': '{words} クラス。',
    'enum_desc': '{words} の列挙型。',
    'function_desc': '{words_cap}。',
    'method_desc': '{words_cap}。',
    'constructor_desc': '新しい {parent} インスタンスを作成します。',
    'param_desc': '使用する {words}。',
    'return_prefix': '戻り値',
    'return_desc': '{rtype} としての結果。',
    'return_default': '結果。',
    'example_label': '例：',
    'new_file_log': '  [新しいファイル] ファイルヘッダーを追加しました（作成者: {author}）',
    'generated_log': '{count} 個の要素のコメントを {path} に生成しました',
    'no_elements': '{path} に文書化可能な要素が見つかりませんでした',
    'usage': '使用法: generate_dart_comments.py <dart_file> [output_file] [--lang en|zh]',
    'file_not_found': 'エラー: ファイル {path} が見つかりません',
}
```

## Documentation Standards / 文档标准

See [references/dartdoc_format.md](references/dartdoc_format.md) for:
- File header metadata format
- Documentation tag reference
- Templates for functions, classes, and enums
- Language-specific writing guidelines (EN/ZH)

详见 [references/dartdoc_format.md](references/dartdoc_format.md)：
- 文件头元数据格式
- 文档标签参考
- 函数、类、枚举模板
- 中英文写作指南

## CI/CD Integration / CI/CD 集成

```yaml
# GitHub Actions example
- name: Generate Docs
  run: |
    find lib -name "*.dart" -exec python scripts/generate_dart_comments.py {} --lang en \;
```

## License

MIT
