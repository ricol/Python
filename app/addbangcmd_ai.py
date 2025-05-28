#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from typing import List, Tuple

# Constants for shebang and encoding declarations
SHEBANG_STANDARD = '#!/usr/bin/python'
SHEBANG_LOCAL = '#!/usr/local/bin/python'
SHEBANG_ENV = '#!/usr/bin/env python'
CODING_UTF8 = "#-*- coding: utf-8 -*-"
CODING_UTF = "#-*- coding:utf -*-"

class FileProcessor:
    @staticmethod
    def get_files(directory: str, file_extension: str) -> List[str]:
        """Get all files with given extension in directory tree, excluding files with 'addbangcmd' in name."""
        result = []
        for root, _, files in os.walk(directory):
            path = root.split(os.sep)
            dir_path = '/'.join(path)
            for file in files:
                file_path = f"{dir_path}/{file}"
                filename, extension = os.path.splitext(file_path)
                if "addbangcmd" in filename:
                    continue
                if extension == file_extension:
                    result.append(file_path)
        return result

    @staticmethod
    def clean_content(content: str) -> Tuple[str, bool]:
        """
        Remove shebang lines, encoding declarations, and excessive empty lines.
        Returns cleaned content and whether any changes were made.
        """
        lines = content.split('\n')
        processed = False
        
        # Remove header lines
        while lines and FileProcessor._should_remove_line(lines[0]):
            lines.pop(0)
            processed = True
        
        # Clean up empty lines
        cleaned_lines = FileProcessor._remove_excessive_empty_lines(lines)
        
        if processed:
            return '\n'.join(cleaned_lines), True
        return content, False

    @staticmethod
    def _should_remove_line(line: str) -> bool:
        """Determine if a line should be removed from the header."""
        line_stripped = line.strip()
        return (line_stripped in {SHEBANG_STANDARD, SHEBANG_LOCAL, SHEBANG_ENV, CODING_UTF8, CODING_UTF, ""}
                or "coding" in line_stripped and "utf" in line_stripped
                or "usr/bin/" in line_stripped
                or line_stripped.startswith("#!"))

    @staticmethod
    def _remove_excessive_empty_lines(lines: List[str]) -> List[str]:
        """Remove consecutive empty lines, keeping at most one."""
        cleaned_lines = []
        last_line_empty = False
        
        for line in lines:
            is_empty = not line.strip()
            if is_empty:
                if not last_line_empty:
                    cleaned_lines.append("")
                    last_line_empty = True
            else:
                cleaned_lines.append(line)
                last_line_empty = False
                
        return cleaned_lines

    @staticmethod
    def process_file(file_path: str, content: str, add_header: bool) -> bool:
        """Process file content by either adding or removing headers."""
        if add_header:
            lines = content.split('\n')
            if (len(lines) >= 3 
                and lines[0] == SHEBANG_ENV 
                and lines[1] == CODING_UTF8 
                and lines[2] == ''):
                return False
                
            cleaned_content, _ = FileProcessor.clean_content(content)
            lines = cleaned_content.split('\n')
            lines.insert(0, SHEBANG_ENV)
            lines.insert(1, CODING_UTF8)
            lines.insert(2, '')
            return FileProcessor._save_file(file_path, '\n'.join(lines))
        else:
            cleaned_content, was_processed = FileProcessor.clean_content(content)
            if was_processed:
                return FileProcessor._save_file(file_path, cleaned_content)
            return False

    @staticmethod
    def _save_file(file_path: str, content: str) -> bool:
        """Save content to file, handling potential errors."""
        try:
            with open(file_path, 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error[{file_path}]: {e}", file=sys.stderr)
            return False


def main():
    if len(sys.argv) <= 2:
        print("Usage: addbangcmd.py --add|--remove <directory>")
        sys.exit(1)
        
    option = sys.argv[1]
    if option not in ["--add", "--remove"]:
        print("Invalid operation!")
        sys.exit(1)
        
    directory = sys.argv[2]
    file_extension = ".py"
    
    print(f"Searching for {file_extension} files in {directory}")
    files = FileProcessor.get_files(directory, file_extension)
    total_files = len(files)
    ignored = 0
    updated = 0
    
    for file_path in files:
        try:
            with open(file_path, "r") as f:
                content = f.read()
                print(f"Processing...{file_path}")
                if FileProcessor.process_file(file_path, content, add_header=(option == "--add")):
                    updated += 1
                else:
                    ignored += 1
        except Exception as e:
            print(f"Error reading {file_path}: {e}", file=sys.stderr)
            ignored += 1
    
    print("\nResult:")
    print(f"Total[{file_extension}]: {total_files}")
    print(f"Updated: {updated}")
    print(f"Ignored: {ignored}")


if __name__ == "__main__":
    main()