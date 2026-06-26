#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Dartdoc comments for Dart code.

This script analyzes Dart files and generates comprehensive API documentation
comments for functions, methods, classes, enums, and other documentable elements.

Supports both English (--lang en) and Chinese (--lang zh) comment generation.
"""

import re
import sys
import os
import argparse
import subprocess
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
from pathlib import Path


# ---------------------------------------------------------------------------
# Localized string templates – add new languages by extending this dict
# ---------------------------------------------------------------------------

STRINGS = {
    'en': {
        'file_header_desc': '{name} module.',
        'class_desc': 'The {words} class.',
        'enum_desc': 'Enumeration of {words}.',
        'function_desc': '{words_cap}.',
        'method_desc': '{words_cap}.',
        'constructor_desc': 'Creates a new {parent}.',
        'param_desc': 'The {words} to use.',
        'return_prefix': 'Returns',
        'return_desc': 'the result as {rtype}.',
        'return_default': 'the result.',
        'example_label': 'Example:',
        'new_file_log': '  [New file] Added file header (author: {author})',
        'generated_log': 'Generated comments for {count} elements in {path}',
        'no_elements': 'No documentable elements found in {path}',
        'usage': 'Usage: generate_dart_comments.py <dart_file> [output_file] [--lang en|zh]',
        'file_not_found': 'Error: File {path} does not exist',
    },
    'zh': {
        'file_header_desc': '{name} 模块。',
        'class_desc': '{words} 类。',
        'enum_desc': '{words} 的枚举。',
        'function_desc': '{words_cap}。',
        'method_desc': '{words_cap}。',
        'constructor_desc': '创建新的{parent}实例。',
        'param_desc': '要使用的{words}。',
        'return_prefix': '返回',
        'return_desc': '{rtype} 类型的结果。',
        'return_default': '计算结果。',
        'example_label': '示例：',
        'new_file_log': '  [新文件] 已添加文件头（作者: {author}）',
        'generated_log': '已为 {count} 个元素在 {path} 中生成注释',
        'no_elements': '在 {path} 中未找到可文档化的元素',
        'usage': '用法: generate_dart_comments.py <dart_file> [output_file] [--lang en|zh]',
        'file_not_found': '错误: 文件 {path} 不存在',
    },
}


@dataclass
class DartElement:
    """Represents a documentable Dart element."""
    name: str
    type: str  # 'function', 'method', 'class', 'enum', 'constructor', etc.
    line_number: int
    code: str
    parameters: List[str] = None
    return_type: Optional[str] = None
    is_static: bool = False
    is_abstract: bool = False
    parent_class: Optional[str] = None


class DartCommentGenerator:
    """Generates Dartdoc comments for Dart code elements.

    Supports multiple languages for generated comments via the ``language``
    parameter (``'en'`` for English, ``'zh'`` for Chinese).
    """

    def __init__(self, language: str = 'zh'):
        """Initialize the generator.

        Args:
            language: Language code for generated comments (``'en'`` or ``'zh'``).
        """
        if language not in STRINGS:
            print(f"Warning: Unsupported language '{language}', falling back to 'zh'.")
            language = 'zh'
        self.language = language
        self.s = STRINGS[language]  # shortcut for string lookups
        self._author = self._get_author()

    def _get_author(self) -> str:
        """Get author name from git config or environment variables."""
        try:
            result = subprocess.run(
                ['git', 'config', 'user.name'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            pass

        for var in ['USER', 'USERNAME', 'LOGNAME']:
            username = os.environ.get(var)
            if username:
                return username

        return 'Unknown'

    def _is_new_file(self, lines: List[str]) -> bool:
        """Check if a file is 'new' (has no existing dartdoc comments)."""
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('///'):
                return False
        return True

    def _generate_file_header(self, file_path: str) -> str:
        """Generate file-level header with author and creation time.

        Args:
            file_path: Path to the Dart file, used to infer file description.

        Returns:
            A multi-line string with the file header dartdoc comment.
        """
        filename = os.path.basename(file_path)
        module_name = os.path.splitext(filename)[0]

        # Convert snake_case or camelCase module name to readable words
        readable_name = re.sub(r'[_]', ' ', module_name)
        readable_name = re.sub(r'([A-Z])', r' \1', readable_name).strip()

        creation_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        header_lines = [
            '/// ',
            f'/// @author {self._author}',
            f'/// @created {creation_time}',
            '/// ',
            f'/// {self.s["file_header_desc"].format(name=readable_name)}',
            '/// ',
        ]
        return '\n'.join(header_lines)

    def parse_dart_file(self, file_path: str) -> List[DartElement]:
        """Parse a Dart file and extract documentable elements."""
        elements = []

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        current_class = None
        i = 0

        while i < len(lines):
            line = lines[i].strip()
            original_line = lines[i]

            # Skip empty lines and comments
            if not line or line.startswith('//') or line.startswith('/*') or line.startswith('///'):
                i += 1
                continue

            # Check for class declaration
            class_match = re.match(r'^class\s+(\w+)', line)
            if class_match:
                current_class = class_class_name = class_match.group(1)
                elements.append(DartElement(
                    name=class_class_name,
                    type='class',
                    line_number=i + 1,
                    code=line
                ))
                i += 1
                continue

            # Check for enum declaration
            enum_match = re.match(r'^enum\s+(\w+)', line)
            if enum_match:
                elements.append(DartElement(
                    name=enum_match.group(1),
                    type='enum',
                    line_number=i + 1,
                    code=line
                ))
                i += 1
                continue

            # Check for constructor (must be inside class and match ClassName pattern)
            if current_class:
                constructor_match = re.match(rf'^{re.escape(current_class)}\s*\(([^)]*)\)\s*(?::\s*[^{{]*)?\s*(?:\{{|;)', line)
                if constructor_match:
                    params = constructor_match.group(1).strip()
                    elements.append(DartElement(
                        name=current_class,
                        type='constructor',
                        line_number=i + 1,
                        code=line,
                        parameters=[p.strip() for p in params.split(',') if p.strip()],
                        parent_class=current_class
                    ))
                    i += 1
                    continue

            # Check for function/method declaration with generic type support (handles nested generics)
            func_match = re.match(r'^(?:static\s+)?(?:\w+(?:<[^()]+>)?)\s+(\w+)\s*\(([^)]*)\)\s*(?:async\s*)?(?:\{|;)', line)
            if func_match:
                name = func_match.group(1)
                # Skip keywords and non-declarations
                if name in ('if', 'else', 'for', 'while', 'switch', 'case', 'return', 'throw', 'try', 'catch', 'finally', 'class', 'enum', 'extends', 'implements', 'with', 'import', 'export', 'library', 'part'):
                    func_match = None

            if func_match:
                name = func_match.group(1)
                params = func_match.group(2).strip()

                # Determine if it's a method or function
                elem_type = 'method' if current_class else 'function'

                # Check for return type (handle generics like Future<Map<String, dynamic>>)
                return_type = None
                if '(' in line:
                    before_paren = line[:line.index('(')].strip()
                    # Remove static keyword if present
                    before_paren = re.sub(r'^static\s+', '', before_paren)
                    # Extract the return type (everything before the function name)
                    # Match pattern: ReturnType FunctionName
                    rt_match = re.match(r'(.+?)\s+' + re.escape(name) + r'\s*$', before_paren)
                    if rt_match:
                        return_type = rt_match.group(1).strip()

                elements.append(DartElement(
                    name=name,
                    type=elem_type,
                    line_number=i + 1,
                    code=line,
                    parameters=[p.strip() for p in params.split(',') if p.strip()],
                    return_type=return_type,
                    parent_class=current_class
                ))

            i += 1

        return elements

    def generate_comment(self, element: DartElement) -> str:
        """Generate a Dartdoc comment for a Dart element."""
        lines_list = []

        # Generate description based on element type and name
        description = self._generate_description(element)
        lines_list.append(f'/// {description}')

        # Add parameters documentation
        if element.parameters and element.type in ['function', 'method', 'constructor']:
            for param in element.parameters:
                if param:
                    # Extract parameter name, handling named params with {} and this. prefix
                    param_name = param.split()[-1] if ' ' in param else param
                    # Remove this. prefix, braces, and optional/default values
                    param_name = re.sub(r'^this\.', '', param_name)
                    param_name = re.sub(r'[{}]', '', param_name)
                    param_name = re.sub(r'=.*$', '', param_name)
                    if param_name:
                        param_desc = self._generate_parameter_description(param_name, element)
                        lines_list.append(f'/// * [{param_name}] {param_desc}')

        # Add return type documentation
        if element.return_type and element.return_type != 'void':
            return_desc = self._generate_return_description(element)
            lines_list.append('/// ')
            lines_list.append(f'/// {self.s["return_prefix"]} {return_desc}')

        # Add example if appropriate
        if element.type in ['function', 'method'] and element.name:
            example = self._generate_example(element)
            if example:
                lines_list.append('/// ')
                lines_list.append(f'/// {self.s["example_label"]}')
                lines_list.append('/// ```dart')
                for ex_line in example.split('\n'):
                    lines_list.append(f'/// {ex_line}')
                lines_list.append('/// ```')

        return '\n'.join(lines_list)

    def _generate_description(self, element: DartElement) -> str:
        """Generate a description for the element."""
        name = element.name

        # Convert camelCase to space-separated words
        words = re.sub(r'([A-Z])', r' \1', name).strip().lower()

        if element.type == 'class':
            return self.s['class_desc'].format(words=words)
        elif element.type == 'enum':
            return self.s['enum_desc'].format(words=words)
        elif element.type == 'function':
            return self.s['function_desc'].format(words_cap=words.capitalize())
        elif element.type == 'method':
            return self.s['method_desc'].format(words_cap=words.capitalize())
        elif element.type == 'constructor':
            parent = element.parent_class or 'instance'
            return self.s['constructor_desc'].format(parent=parent)

        return f'Documentation for {name}.'

    def _generate_parameter_description(self, param_name: str, element: DartElement) -> str:
        """Generate description for a parameter."""
        words = re.sub(r'([A-Z])', r' \1', param_name).strip().lower()
        return self.s['param_desc'].format(words=words)

    def _generate_return_description(self, element: DartElement) -> str:
        """Generate description for return value."""
        if element.return_type:
            return self.s['return_desc'].format(rtype=element.return_type)
        return self.s['return_default']

    def _generate_example(self, element: DartElement) -> Optional[str]:
        """Generate an example usage if appropriate."""
        if not element.parameters:
            return None

        args = []
        for param in element.parameters:
            if param:
                param_name = param.split()[-1] if ' ' in param else param
                if 'String' in param:
                    args.append(f"'{param_name}'")
                elif 'int' in param or 'double' in param:
                    args.append('0')
                elif 'bool' in param:
                    args.append('true')
                elif 'List' in param:
                    args.append('[]')
                elif 'Map' in param:
                    args.append('{}')
                else:
                    args.append('null')

        args_str = ', '.join(args)

        if element.type == 'function':
            return f'final result = {element.name}({args_str});'
        elif element.type == 'method':
            return f'final result = instance.{element.name}({args_str});'

        return None

    def insert_comments(self, file_path: str, output_path: Optional[str] = None):
        """Insert generated comments into a Dart file."""
        elements = self.parse_dart_file(file_path)

        if not elements:
            print(self.s['no_elements'].format(path=file_path))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Check if this is a new file (no existing dartdoc comments)
        is_new = self._is_new_file(lines)

        # For new files, insert file header at the very beginning (before imports)
        header_offset = 0
        if is_new:
            file_header = self._generate_file_header(file_path)
            header_lines = file_header.split('\n')
            # Insert at position 0 (before everything)
            for i, hline in enumerate(header_lines):
                lines.insert(i, hline + '\n')
            header_offset = len(header_lines)
            print(self.s['new_file_log'].format(author=self._author))

        # Adjust line numbers by header offset and process elements
        insertions = []
        for element in elements:
            adjusted_line = element.line_number - 1 + header_offset
            comment = self.generate_comment(element)
            insertions.append((adjusted_line, comment))

        # Sort by line number descending to insert from bottom to top
        insertions.sort(key=lambda x: x[0], reverse=True)

        # Insert comments
        for line_index, comment in insertions:
            # Check if there's already a comment above this line
            if line_index > 0 and lines[line_index - 1].strip().startswith('///'):
                continue

            comment_lines = comment.split('\n')
            for i, comment_line in enumerate(comment_lines):
                lines.insert(line_index + i, comment_line + '\n')

        # Write to output file
        output_file = output_path or file_path
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        print(self.s['generated_log'].format(count=len(elements), path=output_file))


def main():
    parser = argparse.ArgumentParser(
        description='Generate Dartdoc comments for Dart files.',
        add_help=False,
    )
    parser.add_argument('input_file', nargs='?', help='Path to the Dart file to process')
    parser.add_argument('output_file', nargs='?', default=None,
                        help='Optional output file path (defaults to overwriting input)')
    parser.add_argument('--lang', choices=['en', 'zh'], default='zh',
                        help='Language for generated comments (default: zh)')
    parser.add_argument('-h', '--help', action='store_true',
                        help='Show this help message and exit')

    args = parser.parse_args()

    if args.help or not args.input_file:
        lang_s = STRINGS.get(args.lang, STRINGS['zh'])
        print(lang_s['usage'])
        print()
        print("Options:")
        print("  dart_file     Path to the Dart file to process")
        print("  output_file   Optional output file path")
        print("  --lang en|zh  Language for comments (default: zh)")
        sys.exit(0 if args.help else 1)

    input_file = args.input_file

    if not os.path.exists(input_file):
        lang_s = STRINGS.get(args.lang, STRINGS['zh'])
        print(lang_s['file_not_found'].format(path=input_file))
        sys.exit(1)

    generator = DartCommentGenerator(language=args.lang)
    generator.insert_comments(input_file, args.output_file)


if __name__ == '__main__':
    main()
