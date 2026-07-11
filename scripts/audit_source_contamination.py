from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
UNIT_OVERRIDES = ROOT / "data" / "card_unit_overrides.json"
ABILITY_OVERRIDES = ROOT / "data" / "author_ability_overrides.json"
ABILITIES_JSONL = ROOT / "data" / "cards_current" / "abilities.jsonl"
REPORT = ROOT / "docs" / "source-contamination-audit.md"

SUSPICIOUS_PATTERNS = [
    "脑补",
    "推测",
    "猜测",
    "可能",
    "大概",
    "应该",
    "理解为",
    "看起来",
    "相关剧情牵连",
    "牵连",
    "待作者裁定",
    "临时人物单元名",
    "待确认",
]


def load_json(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def load_abilities() -> list[dict[str, Any]]:
    if not ABILITIES_JSONL.exists():
        return []
    return [
        json.loads(line)
        for line in ABILITIES_JSONL.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def compact(value: object, limit: int = 180) -> str:
    text = " ".join(str(value or "").split())
    return text if len(text) <= limit else text[:limit] + "..."


def suspicious_text(value: object) -> list[str]:
    text = str(value or "")
    return [pattern for pattern in SUSPICIOUS_PATTERNS if pattern in text]


def owner_key(owner_units: object) -> str | None:
    if not isinstance(owner_units, list) or not owner_units:
        return None
    if "全体" in owner_units:
        return "全体"
    return "、".join(str(owner) for owner in owner_units)


def audit_unit_overrides(data: dict[str, Any], abilities: list[dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    by_card: dict[str, list[dict[str, Any]]] = {}
    for ability in abilities:
        by_card.setdefault(str(ability.get("card_title") or ""), []).append(ability)

    for card_title, config in sorted(data.items()):
        if not isinstance(config, dict):
            continue

        shared = config.get("shared")
        if isinstance(shared, dict):
            for field, value in sorted(shared.items()):
                hits = suspicious_text(value)
                if hits:
                    lines.append(
                        f"- `{card_title}` shared.`{field}` 命中 {', '.join(hits)}：{compact(value)}"
                    )

        unit_names = []
        for unit in config.get("units", []) or []:
            if not isinstance(unit, dict):
                continue
            name = str(unit.get("name") or "")
            unit_names.append(name)

            if re.search(r"\d+$", name) and unit.get("name_status") != "作者确认可用":
                lines.append(f"- `{card_title}` 人物单元 `{name}` 使用数字占位名，需作者命名或确认。")

            for field, value in sorted(unit.items()):
                if field == "name":
                    continue
                hits = suspicious_text(value)
                if hits:
                    lines.append(
                        f"- `{card_title}` / `{name}` 的 `{field}` 命中 {', '.join(hits)}：{compact(value)}"
                    )

        ability_owners = set()
        for ability in by_card.get(card_title, []):
            key = owner_key(ability.get("owner_units"))
            if key:
                ability_owners.add(key)
                if key != "全体":
                    ability_owners.update(str(owner) for owner in ability.get("owner_units", []))

        for name in unit_names:
            if "全体" in ability_owners:
                continue
            unit_config = next(
                (
                    unit
                    for unit in config.get("units", []) or []
                    if isinstance(unit, dict) and unit.get("name") == name
                ),
                {},
            )
            if unit_config.get("no_abilities_confirmed"):
                continue
            if name and name not in ability_owners and name != "全体":
                lines.append(
                    f"- `{card_title}` / `{name}` 当前没有直接归属的特技。若这是无特技人物则正常，否则需补所属。"
                )

    return lines


def audit_ability_overrides(data: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for section in ("ability_updates", "ability_splits", "ability_deletes", "structure_confirmed"):
        for index, item in enumerate(data.get(section, []) or [], start=1):
            text = json.dumps(item, ensure_ascii=False)
            hits = suspicious_text(text)
            if hits:
                match = item.get("match", item)
                lines.append(
                    f"- `{section}` #{index} {compact(match)} 命中 {', '.join(sorted(set(hits)))}。"
                )
    return lines


def main() -> None:
    unit_data = load_json(UNIT_OVERRIDES) or {}
    ability_data = load_json(ABILITY_OVERRIDES) or {}
    abilities = load_abilities()

    unit_findings = audit_unit_overrides(unit_data, abilities)
    ability_findings = audit_ability_overrides(ability_data)

    lines = [
        "# 源数据库防污染审计",
        "",
        "本报告只提示疑点，不自动修改事实层数据。",
        "",
        "## 审计原则",
        "",
        "- 事实层只允许牌面、Excel、日志、规则文档、作者裁定。",
        "- AI 推测、解释、强度评价、电子化建议必须进入解释层或评审层。",
        "- 宁可字段为空，也不能补写没有来源的概括。",
        "",
        "## 人物单元覆盖疑点",
        "",
    ]
    if unit_findings:
        lines.extend(unit_findings)
    else:
        lines.append("- 未发现明显疑点。")

    lines.extend(["", "## 特技覆盖疑点", ""])
    if ability_findings:
        lines.extend(ability_findings)
    else:
        lines.append("- 未发现明显疑点。")

    lines.extend(
        [
            "",
            "## 下一步",
            "",
            "- 数字占位名需要作者命名或确认。",
            "- 无特技人物如果是事实，应保留；如果只是漏归属，应补作者裁定。",
            "- 命中可疑词的内容应移入解释层，或由作者明确裁定后保留。",
        ]
    )

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(REPORT)


if __name__ == "__main__":
    main()
