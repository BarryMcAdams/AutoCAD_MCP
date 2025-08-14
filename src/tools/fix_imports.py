#!/usr/bin/env python3
"""
Fix relative imports to absolute imports in the src directory
"""
import os
import re
import glob

def fix_imports_in_file(filepath):
    """Fix relative imports in a single file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match relative imports like "from ..module import something"
    # Replace with absolute imports
    pattern = r'from \.\.([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)'
    replacement = r'from src.\1'
    
    new_content = re.sub(pattern, replacement, content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed imports in: {filepath}")
        return True
    return False

def main():
    """Fix all relative imports in src directory"""
    src_dir = 'src'
    fixed_count = 0
    
    # Find all Python files in src directory
    python_files = glob.glob(os.path.join(src_dir, '**', '*.py'), recursive=True)
    
    for filepath in python_files:
        if fix_imports_in_file(filepath):
            fixed_count += 1
    
    print(f"Fixed imports in {fixed_count} files")

if __name__ == '__main__':
    main()