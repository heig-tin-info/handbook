#!/usr/bin/env python3
"""Escape the pipes that live inside code spans of a Markdown table row.

GFM splits a table row on every ``|`` that is not escaped as ``\\|``, code
spans included; Python-Markdown's ``tables`` extension is lenient and ignores
a ``|`` it finds between two backticks. The handbook was written against the
lenient reading, so a row such as::

    | `|`  | Disjonction | `(0b1101 | 0b1010) == 0b1111` |

looks right on the site and gives TMark four cells for a three-column table,
which LaTeX rejects with ``Extra alignment tab has been changed to \\cr``.

This script rewrites those rows to the GFM spelling, escaping a ``|`` only
when it sits inside a backtick code span of a line that belongs to a table.
It is idempotent: a pipe already written ``\\|`` is left alone.

Usage::

    python utils/escape_table_pipes.py            # rewrite docs/**/*.md
    python utils/escape_table_pipes.py --check    # report, change nothing
    python utils/escape_table_pipes.py path.md …  # restrict to some files
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
DELIMITER_CHARS = set("|:- \t")


def is_delimiter_row(line: str) -> bool:
    """Whether *line* is the ``| --- | --- |`` row that declares a table."""
    stripped = line.strip()
    if not stripped or "|" not in stripped or "-" not in stripped:
        return False
    return set(stripped) <= DELIMITER_CHARS


def code_span_ranges(line: str) -> list[tuple[int, int]]:
    """The ``(start, end)`` offsets of the code-span *contents* of *line*.

    Backtick runs are paired the way CommonMark pairs them: a run of *n*
    backticks opens a span that the next run of exactly *n* backticks closes.
    A backtick escaped with a backslash neither opens nor closes.
    """
    runs: list[tuple[int, int]] = []  # (start, length)
    i = 0
    while i < len(line):
        if line[i] != "`":
            i += 1
            continue
        backslashes = 0
        j = i - 1
        while j >= 0 and line[j] == "\\":
            backslashes += 1
            j -= 1
        start = i
        while i < len(line) and line[i] == "`":
            i += 1
        if backslashes % 2:  # the first backtick of the run is escaped
            start += 1
        if i > start:
            runs.append((start, i - start))
    ranges: list[tuple[int, int]] = []
    pos = 0
    while pos < len(runs):
        start, length = runs[pos]
        for other in range(pos + 1, len(runs)):
            if runs[other][1] == length:
                ranges.append((start + length, runs[other][0]))
                pos = other + 1
                break
        else:
            pos += 1
    return ranges


def escape_row(line: str) -> str:
    """Escape every unescaped ``|`` inside a code span of *line*."""
    out = list(line)
    for start, end in reversed(code_span_ranges(line)):
        for i in range(end - 1, start - 1, -1):
            if out[i] != "|":
                continue
            backslashes = 0
            j = i - 1
            while j >= start and out[j] == "\\":
                backslashes += 1
                j -= 1
            if backslashes % 2 == 0:
                out[i] = "\\|"
    return "".join(out)


def convert(text: str) -> tuple[str, int]:
    """Return *text* with its table rows escaped, and how many rows changed."""
    lines = text.split("\n")
    fence: str | None = None
    in_table = False
    changed = 0
    for index, line in enumerate(lines):
        match = FENCE.match(line)
        if match:
            if fence is None:
                fence = match.group(1)[0] * 3
            elif line.strip().startswith(fence):
                fence = None
            in_table = False
            continue
        if fence is not None:
            continue
        if not line.strip():
            in_table = False
            continue
        if is_delimiter_row(line):
            header = index - 1
            if header >= 0 and lines[header].strip() and "|" in lines[header]:
                in_table = True
                rewritten = escape_row(lines[header])
                if rewritten != lines[header]:
                    lines[header] = rewritten
                    changed += 1
            continue
        if not in_table:
            continue
        rewritten = escape_row(line)
        if rewritten != line:
            lines[index] = rewritten
            changed += 1
    return "\n".join(lines), changed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="files to rewrite")
    parser.add_argument("--check", action="store_true", help="report only")
    parser.add_argument(
        "--docs", type=Path, default=Path("docs"), help="tree to walk by default"
    )
    args = parser.parse_args(argv)

    paths = args.paths or sorted(args.docs.rglob("*.md"))
    total_rows = 0
    total_files = 0
    for path in paths:
        text = path.read_text(encoding="utf-8")
        converted, changed = convert(text)
        if not changed:
            continue
        total_rows += changed
        total_files += 1
        print(f"{path}: {changed} row{'s' if changed > 1 else ''}")
        if not args.check:
            path.write_text(converted, encoding="utf-8")
    verb = "would change" if args.check else "changed"
    print(f"{verb} {total_rows} rows in {total_files} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
