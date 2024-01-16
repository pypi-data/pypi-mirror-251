from __future__ import annotations

import re
import pangu
import argparse
from typing import Sequence
from pangu import ANY_CJK

def format_file(filename, patterns):
    try:
        retv = 0
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        for pattern in patterns:
            # 搜索正则匹配到的所有字符串，如果这些字符串有一个满足 ANY_CJK.search(text) 的话，retv = 1
            groups = re.findall(pattern, content)
            for group in groups:
                if ANY_CJK.search(group):
                    retv = 1
                    break
            content = re.sub(
                pattern, lambda m: pangu.spacing_text(m.group(0)), content)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

        return retv

    except Exception as e:
        print(f"Error occurred while formatting file {filename}: {e}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    retv = 0

    patterns = []
    patterns.append(
        r'[\u4e00-\u9fa5\u3000-\u303F]([\'"]?[a-zA-Z0-9]+[\'"]?)[\u4e00-\u9fa5\u3000-\u303F]')
    patterns.append(
        r'([\'"]?[a-zA-Z0-9]+[\'"\`]?)[\u4e00-\u9fa5\u3000-\u303F]')
    patterns.append(r'[\u4e00-\u9fa5\u3000-\u303F]([\'"]?[a-zA-Z0-9]+[\'"]?)')

    for filename in args.filenames:
        if filename.endswith('.md'):
            retv = format_file(filename, patterns)
            if retv:
                print(f'{filename} is formatted with pangu')

    return retv


if __name__ == '__main__':
    main()
