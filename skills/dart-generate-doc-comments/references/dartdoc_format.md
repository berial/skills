# Dartdoc 格式参考 / Dartdoc Format Reference

## 文件头元数据（仅新文件）/ File Header Metadata (New Files Only)

当 Dart 文件中不存在任何 `///` 文档注释时（即新文件），应在文件顶部添加文件头。

When no `///` doc comments exist in a Dart file (i.e., a new file), a file header should be added at the top.

```dart
///
/// @author {authorName}
/// @created {YYYY-MM-DD HH:mm:ss}
///
/// {file_description}
///
```

- `@author`：创建人姓名，优先从 `git config user.name` 获取，否则使用当前用户名
  - Author name, obtained from `git config user.name` first, then falls back to current username
- `@created`：文件创建时间，格式为 `YYYY-MM-DD HH:mm:ss`
  - File creation time in `YYYY-MM-DD HH:mm:ss` format
- `{file_description}`：文件/库的简要用途描述
  - Brief description of the file/library purpose

**注意**：此文件头仅对新文件生效。如果文件已存在 `///` 注释，则跳过文件头生成。

**Note**: This header is only added for new files. If existing `///` comments are found, header generation is skipped.

---

## 基本结构 / Basic Structure

```dart
/// Brief description of the element. / 元素的简要描述。
///
/// Longer description if needed, can span multiple lines. / 如需更长描述，可跨多行。
///
/// * [paramName] Description of the parameter. / 参数的描述。
///
/// Returns description of the return value. / 返回返回值的描述。
///
/// Example: / 示例：
/// ```dart
/// // example code / 示例代码
/// ```
```

---

## 文档标签 / Documentation Tags

### 基本标签 / Basic Tags
- `///` - 单行文档注释 / Single-line doc comment
- `/** */` - 多行文档注释（在Dart中较少使用）/ Multi-line doc comment (less common in Dart)

### 参数文档 / Parameter Documentation
- `* [paramName]` - 参数引用 / Parameter reference
- `@param paramName Description` - 替代格式 / Alternative format

### 返回值 / Return Value
- `Returns description` - 记录返回值 / Documents the return value
- `@return description` - 替代格式 / Alternative format

### 异常 / Exceptions
- `Throws [ExceptionType] if condition` - 记录异常 / Documents exceptions
- `@throws ExceptionType description` - 替代格式 / Alternative format

### 引用 / References
- `[ClassName]` - 类引用 / Class reference
- `[methodName]` - 方法引用 / Method reference
- `[libraryName]` - 库引用 / Library reference

---

## 示例模板 / Example Templates

### 函数文档 / Function Documentation

**English:**
```dart
/// Calculates the sum of two numbers.
///
/// * [a] The first number to add.
/// * [b] The second number to add.
///
/// Returns the sum of [a] and [b].
///
/// Example:
/// ```dart
/// final result = add(2, 3);
/// print(result); // 5
/// ```
int add(int a, int b) {
  return a + b;
}
```

**中文 / Chinese:**
```dart
/// 计算两个数字的和。
///
/// * [a] 要相加的第一个数字。
/// * [b] 要相加的第二个数字。
///
/// 返回 [a] 和 [b] 的和。
///
/// 示例：
/// ```dart
/// final result = add(2, 3);
/// print(result); // 5
/// ```
int add(int a, int b) {
  return a + b;
}
```

### 类文档 / Class Documentation

**English:**
```dart
/// Represents a user in the system.
///
/// This class provides methods for managing user data and authentication.
class User {
  /// The user's unique identifier.
  final String id;

  /// The user's display name.
  final String name;

  /// Creates a new User instance.
  ///
  /// [id] The user's unique identifier.
  /// [name] The user's display name.
  User({required this.id, required this.name});

  /// Authenticates the user with the given credentials.
  ///
  /// [username] The username for authentication.
  /// [password] The password for authentication.
  ///
  /// Returns `true` if authentication succeeds, `false` otherwise.
  ///
  /// Throws [AuthenticationException] if credentials are invalid.
  bool authenticate(String username, String password) {
    return true;
  }
}
```

**中文 / Chinese:**
```dart
/// 表示系统中的用户。
///
/// 此类提供管理用户数据和身份验证的方法。
class User {
  /// 用户的唯一标识符。
  final String id;

  /// 用户的显示名称。
  final String name;

  /// 创建新的User实例。
  ///
  /// [id] 用户的唯一标识符。
  /// [name] 用户的显示名称。
  User({required this.id, required this.name});

  /// 使用给定凭据验证用户身份。
  ///
  /// [username] 用于身份验证的用户名。
  /// [password] 用于身份验证的密码。
  ///
  /// 如果身份验证成功返回 `true`，否则返回 `false`。
  ///
  /// 如果凭据无效，抛出 [AuthenticationException]。
  bool authenticate(String username, String password) {
    return true;
  }
}
```

### 枚举文档 / Enum Documentation

**English:**
```dart
/// Represents the status of a task.
enum TaskStatus {
  /// The task has not yet started.
  pending,

  /// The task is currently in progress.
  inProgress,

  /// The task has been completed successfully.
  completed,

  /// The task failed to complete.
  failed,
}
```

**中文 / Chinese:**
```dart
/// 表示任务的状态。
enum TaskStatus {
  /// 任务尚未开始。
  pending,

  /// 任务当前正在进行中。
  inProgress,

  /// 任务已成功完成。
  completed,

  /// 任务未能完成。
  failed,
}
```

---

## 语言特定规范 / Language-Specific Guidelines

### 英文规范 / English Guidelines
1. **Be concise**: Start descriptions with a capital letter, use complete sentences
2. **Use third-person singular**: "Calculates...", "Represents...", "Creates..."
3. **Parameter descriptions**: Use "The" prefix — "The first number to add."
4. **Return value**: Use "Returns the..." or "A [type] representing..."
5. **Examples**: Label with "Example:" not "Example：" (use ASCII colon)

### 中文规范 / Chinese Guidelines
1. **简洁明了**：描述以句号结尾，使用完整句子
2. **动词开头**：使用"计算..."、"表示..."、"创建..."等动词短语
3. **参数描述**：使用"要..."的形式 — "要相加的第一个数字。"
4. **返回值**：使用"返回..."开头
5. **示例标签**：使用全角标点"示例："

---

## 最佳实践 / Best Practices

1. **简洁 / Be concise**：保持描述简短但信息丰富 / Keep descriptions short but informative
2. **使用完整句子 / Use complete sentences**：以大写字母开头 / Start with a capital letter
3. **记录非显而易见的行为 / Document non-obvious behavior**：关注代码中不明确的内容 / Focus on what's not obvious from the code
4. **包含示例 / Include examples**：展示如何使用复杂API / Show how to use complex APIs
5. **记录参数 / Document parameters**：解释每个参数的作用 / Explain what each parameter does
6. **记录返回值 / Document return values**：解释返回的内容 / Explain what is returned
7. **记录异常 / Document exceptions**：解释何时抛出异常 / Explain when exceptions are thrown
8. **使用引用 / Use references**：链接到相关类和方法 / Link to related classes and methods
