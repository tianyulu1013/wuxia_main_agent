#!/usr/bin/env python3
"""按卡名和维度读取已精评人物，避免批量加载全部评审。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "data" / "review" / "cards" / "index.json"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def load_index() -> dict:
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))


def resolve_project_path(relative_path: str) -> Path:
    path = (ROOT / relative_path).resolve()
    if ROOT not in path.parents and path != ROOT:
        raise ValueError(f"索引路径越出项目目录：{relative_path}")
    return path


def print_file(relative_path: str) -> None:
    path = resolve_project_path(relative_path)
    print(f"# 文件：{relative_path}\n")
    print(path.read_text(encoding="utf-8"))


def command_title(entries: dict, title: str) -> None:
    entry = entries.get(title)
    if entry is None:
        raise SystemExit(f"未找到已精评人物：{title}")
    print_file(entry["summary"])
    print("\n# 可选维度")
    for key, value in entry["dimensions"].items():
        print(f"- {key}: {value}")


def command_dimension(entries: dict, title: str, dimension: str) -> None:
    entry = entries.get(title)
    if entry is None:
        raise SystemExit(f"未找到已精评人物：{title}")
    relative_path = entry["dimensions"].get(dimension)
    if relative_path is None:
        choices = "、".join(entry["dimensions"])
        raise SystemExit(f"人物“{title}”没有维度“{dimension}”；可用：{choices}")
    print_file(relative_path)


def command_list(entries: dict) -> None:
    for title, entry in entries.items():
        print(f"{title}\t{entry['status']}\t{entry['summary']}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="列出已建立评价目录的人物")

    title_parser = subparsers.add_parser("title", help="读取人物总分析和维度路由")
    title_parser.add_argument("title")

    dimension_parser = subparsers.add_parser("dimension", help="只读取人物的一个评价维度")
    dimension_parser.add_argument("title")
    dimension_parser.add_argument("dimension")

    args = parser.parse_args()
    entries = load_index()["entries"]

    if args.command == "list":
        command_list(entries)
    elif args.command == "title":
        command_title(entries, args.title)
    else:
        command_dimension(entries, args.title, args.dimension)


if __name__ == "__main__":
    main()
