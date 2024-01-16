from __future__ import annotations

import re
import pangu
import argparse
from typing import Sequence


def format_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # Use Pangu to automatically insert whitespace between CJK and half-width characters
        pattern = pattern = r'[\u4e00-\u9fa5\u3000-\u303F]([\'"]?[a-zA-Z0-9]+[\'"]?)[\u4e00-\u9fa5\u3000-\u303F]'
        content = re.sub(
            pattern, lambda m: pangu.spacing_text(m.group(0)), content)
        
        pattern = r'([\'"]?[a-zA-Z0-9]+[\'"\`]?)[\u4e00-\u9fa5\u3000-\u303F]'
        content = re.sub(
            pattern, lambda m: pangu.spacing_text(m.group(0)), content)
        
        pattern = r'[\u4e00-\u9fa5\u3000-\u303F]([\'"]?[a-zA-Z0-9]+[\'"]?)'
        content = re.sub(
            pattern, lambda m: pangu.spacing_text(m.group(0)), content)
    
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

    except Exception as e:
        print(f"Error occurred while formatting file {filename}: {e}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        if filename.endswith('.md'):
            format_file(filename)
            print(f'{filename} is formatted with pangu and dicts.csv')
            retv = 1

    return retv


if __name__ == '__main__':
    main()
