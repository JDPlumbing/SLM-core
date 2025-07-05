"""
utils_text.py — Reusable text and file manipulation tools
Usage: import utils_text or call as CLI script
"""

import os
import re
from collections import Counter

# -----------------------------
# Core Utility Functions
# -----------------------------

def delete_lines_starting_with(path, prefix):
    """Delete lines in a file that start with a given prefix"""
    with open(path, "r") as f:
        lines = f.readlines()
    with open(path, "w") as f:
        f.writelines(line for line in lines if not line.lstrip().startswith(prefix))

def dedupe_list(seq):
    """Remove duplicates from list, preserving order"""
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]

def find_replace_file(path, find_str, replace_str):
    """Replace all occurrences of find_str with replace_str in a file"""
    with open(path, "r") as f:
        content = f.read()
    with open(path, "w") as f:
        f.write(content.replace(find_str, replace_str))

def prepend_to_lines(lines, prefix):
    """Prepend a prefix to each line"""
    return [prefix + line for line in lines]

def append_to_lines(lines, suffix):
    """Append a suffix to each line"""
    return [line + suffix for line in lines]

def list_files_by_ext(root_dir, ext=".txt"):
    """Recursively list files by extension"""
    return [
        os.path.join(dp, f)
        for dp, _, filenames in os.walk(root_dir)
        for f in filenames if f.endswith(ext)
    ]

def clean_file(path):
    """Trim whitespace and remove blank lines in a file"""
    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")

def frozen(seq):
    """Return a frozen, hashable version of a list"""
    return tuple(sorted(set(seq)))

def count_items(seq):
    """Count occurrences of items in a list"""
    return dict(Counter(seq))

def flatten(nested):
    """Flatten a nested list one level"""
    return [item for sublist in nested for item in sublist]

def regex_replace_file(path, pattern, repl):
    """Regex find/replace on a file"""
    with open(path, "r") as f:
        content = f.read()
    new_content = re.sub(pattern, repl, content)
    with open(path, "w") as f:
        f.write(new_content)


# -----------------------------
# CLI Interface
# -----------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Text/file utilities")
    sub = parser.add_subparsers(dest="command", required=True)

    # Delete lines
    d = sub.add_parser("delete-lines")
    d.add_argument("path")
    d.add_argument("prefix")

    # Replace string
    r = sub.add_parser("replace")
    r.add_argument("path")
    r.add_argument("find")
    r.add_argument("replace")

    # Clean file
    c = sub.add_parser("clean")
    c.add_argument("path")

    # Regex replace
    x = sub.add_parser("regex")
    x.add_argument("path")
    x.add_argument("pattern")
    x.add_argument("replacement")

    args = parser.parse_args()

    if args.command == "delete-lines":
        delete_lines_starting_with(args.path, args.prefix)
    elif args.command == "replace":
        find_replace_file(args.path, args.find, args.replace)
    elif args.command == "clean":
        clean_file(args.path)
    elif args.command == "regex":
        regex_replace_file(args.path, args.pattern, args.replacement)
