from __future__ import annotations

import difflib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ORDER_DOC = ROOT / "docs" / "tts-slot-orders-v0.1.md"
REPORT = ROOT / "docs" / "tts-slot-order-check.md"
ASSET_ROOT = ROOT / "actual_psd"
if not ASSET_ROOT.exists():
    ASSET_ROOT = ROOT / "psd卡牌"


DECK_DIRS = {
    "场景": ASSET_ROOT / "场景",
    "金庸1": ASSET_ROOT / "人物" / "金庸" / "1",
    "金庸2": ASSET_ROOT / "人物" / "金庸" / "2",
    "金庸3": ASSET_ROOT / "人物" / "金庸" / "3",
    "古龙1": ASSET_ROOT / "人物" / "古龙" / "1",
    "古龙2": ASSET_ROOT / "人物" / "古龙" / "2",
    "黄易1": ASSET_ROOT / "人物" / "黄易" / "1",
    "温瑞安1": ASSET_ROOT / "人物" / "温瑞安" / "1",
    "黄易温瑞安": ASSET_ROOT / "人物" / "温瑞安" / "2",
    "其他": ASSET_ROOT / "人物" / "其他武侠玄幻",
    "现代": ASSET_ROOT / "人物" / "现代鬼畜",
}


KNOWN_ALIASES = {
    "郭襄（峨眉祖师）": "郭襄",
    "杨过（小）": "杨过（少年）",
    "杨过（大侠）": "杨过",
    "玄铁重剑": "玄铁剑",
    "辟邪剑法": "辟邪剑谱",
    "嬴政": "秦始皇",
    "雾雨魔理沙": "魔理沙",
    "萧秋水（少年）": "萧秋水(少年)",
}


def parse_orders(text: str) -> dict[str, list[str]]:
    orders: dict[str, list[str]] = {}
    current: str | None = None
    in_fence = False

    for line in text.splitlines():
        header = re.match(r"^##\s+\d+\.\s+(.+?)\s*$", line)
        if header:
            current = header.group(1)
            orders.setdefault(current, [])
            in_fence = False
            continue

        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue

        if current and in_fence:
            name = line.strip()
            if name:
                orders[current].append(name)

    return orders


def psd_names(path: Path) -> list[str]:
    if not path.exists():
        return []
    return sorted(p.stem for p in path.glob("*.psd"))


def normalized(name: str) -> str:
    return (
        name.replace("（", "(")
        .replace("）", ")")
        .replace("_", "")
        .replace(" ", "")
        .strip()
    )


def suggestions(name: str, candidates: list[str]) -> list[str]:
    if name in KNOWN_ALIASES and KNOWN_ALIASES[name] in candidates:
        return [KNOWN_ALIASES[name]]

    norm = normalized(name)
    by_norm = [candidate for candidate in candidates if normalized(candidate) == norm]
    if by_norm:
        return by_norm

    return difflib.get_close_matches(name, candidates, n=3, cutoff=0.5)


def bullet_list(items: list[str]) -> list[str]:
    if not items:
        return ["- 无"]
    return [f"- {item}" for item in items]


def main() -> None:
    text = ORDER_DOC.read_text(encoding="utf-8")
    orders = parse_orders(text)

    lines: list[str] = [
        "# TTS 顺序与 PSD 对照报告",
        "",
        "本报告由 `scripts/check_tts_slot_orders.py` 生成，只检查卡名与 PSD 文件名是否能对应，不判断规则文本。",
        f"",
        f"- 本次资产根目录：`{ASSET_ROOT.relative_to(ROOT)}`",
        "",
        "## 总览",
        "",
        "| 牌堆 | 顺序表数量 | PSD 数量 | 精确匹配 | 待裁定 | PSD 多出 |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]

    details: list[str] = []

    for deck, path in DECK_DIRS.items():
        ordered = orders.get(deck, [])
        files = psd_names(path)
        ordered_set = set(ordered)
        file_set = set(files)
        matched = sorted(ordered_set & file_set)
        missing = [name for name in ordered if name not in file_set]
        extra = [name for name in files if name not in ordered_set]

        alias_hits: list[tuple[str, list[str]]] = []
        unresolved: list[str] = []
        for name in missing:
            hit = suggestions(name, extra)
            if hit:
                alias_hits.append((name, hit))
            else:
                unresolved.append(name)

        lines.append(
            f"| {deck} | {len(ordered)} | {len(files)} | {len(matched)} | "
            f"{len(missing)} | {len(extra)} |"
        )

        details.extend(
            [
                "",
                f"## {deck}",
                "",
                f"- 顺序表数量：{len(ordered)}",
                f"- PSD 数量：{len(files)}",
                f"- 精确匹配：{len(matched)}",
                "",
                "### 顺序表中有，但 PSD 未精确匹配",
                "",
            ]
        )
        details.extend(bullet_list(missing))

        details.extend(["", "### 可能是别名或标点差异", ""])
        if alias_hits:
            for name, hit in alias_hits:
                details.append(f"- {name} -> {', '.join(hit)}")
        else:
            details.append("- 无")

        details.extend(["", "### PSD 中有，但顺序表未精确匹配", ""])
        details.extend(bullet_list(extra))

        if unresolved:
            details.extend(["", "### 需要作者确认", ""])
            details.extend(bullet_list(unresolved))

    lines.extend(details)

    lines.extend(
        [
            "",
            "## 非当前 release 牌堆提示",
            "",
            f"- `{ASSET_ROOT.relative_to(ROOT)}/人物/黄易/2` 当前不作为独立牌堆发布；`尤鸟倦`、`左游仙` 当前按 `黄易温瑞安` 合并牌堆处理。",
            f"- `{ASSET_ROOT.relative_to(ROOT)}/废弃` 不是 TTS release 牌堆，只作为废弃/历史素材保留。",
            f"- `{ASSET_ROOT.relative_to(ROOT)}/基础卡` 未纳入本次人物/场景 release 顺序检查。",
            "",
        ]
    )

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(str(REPORT))


if __name__ == "__main__":
    main()
