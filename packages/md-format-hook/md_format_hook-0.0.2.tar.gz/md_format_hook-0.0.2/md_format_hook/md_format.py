from __future__ import annotations

import re
import pangu
import pandas as pd
import argparse
from typing import Sequence


def get_nouns(csv_file):
    try:
        df = pd.read_csv(csv_file, header=None)
        df[1] = df[1].astype(str)
        return df[1].tolist()
    except Exception as e:
        print(f"Error occurred while reading CSV file: {e}")
        return []


def format_file(filename, nouns):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # Use Pangu to automatically insert whitespace between CJK and half-width characters
        content = pangu.spacing_text(content)

        # Check and convert nouns to proper nouns
        for noun in nouns:
            pattern = r'\b({})\b'.format(noun.lower())
            content = re.sub(pattern, noun, content, flags=re.IGNORECASE)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"Error occurred while formatting file {filename}: {e}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    retv = 0

    nouns = get_nouns('dicts.csv')
    for filename in args.filenames:
        if filename.endswith('.md'):
            format_file(filename, nouns)
            print(f'{filename} is formatted with pangu and dicts.csv')
            retv = 1

    return retv


if __name__ == '__main__':
    main()
