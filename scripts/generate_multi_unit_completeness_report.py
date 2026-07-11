from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "cards.sqlite"
UNIT_OVERRIDES_PATH = ROOT / "data" / "card_unit_overrides.json"
REPORT_PATH = ROOT / "docs" / "multi-unit-completeness-report.md"

KNOWN_MULTI_UNIT_TITLES = {
    "全真七子",
    "阿三阿四",
    "欢乐英雄",
    "渡厄 渡劫 渡难",
    "玄冥二老",
    "龙木二岛主",
    "江南七怪",
    "太岳四侠",
    "金坷垃三人组",
    "三才剑客",
    "袁冠南 萧中慧",
    "五个人头",
    "血变",
    "千手书生",
    "凌退思",
    "胡青牛王难姑",
    "四大恶人",
    "石中玉",
    "十大恶人",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def compact(value: object, limit: int = 160) -> str:
    text = " ".join(str(value or "").split())
    return text if len(text) <= limit else text[:limit] + "..."


def owner_key(owner_units: object, explicit_unit_names: list[str]) -> str | None:
    if not isinstance(owner_units, list) or not owner_units:
        return None
    owner_names = [str(item) for item in owner_units]
    if len(explicit_unit_names) > 1 and set(owner_names) == set(explicit_unit_names):
        return "共同特技"
    return "、".join(owner_names)


def main() -> None:
    unit_overrides = load_json(UNIT_OVERRIDES_PATH)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        owner_titles = {
            row["title"]
            for row in conn.execute(
                """
                SELECT DISTINCT c.title
                FROM card_abilities a
                JOIN cards c ON c.id = a.card_id
                WHERE a.owner_units_json IS NOT NULL
                  AND a.owner_units_json <> ''
                """
            )
        }
        titles = sorted(set(unit_overrides) | KNOWN_MULTI_UNIT_TITLES | owner_titles)
        cards = {}
        ability_rows = []
        for title in titles:
            card = conn.execute("SELECT * FROM cards WHERE title = ?", (title,)).fetchone()
            if card is None:
                continue
            cards[title] = dict(card)
            ability_rows.extend(
                conn.execute(
                    """
                    SELECT ? AS lookup_title, c.title, a.ordinal, a.kind, a.name, a.text, a.owner_units_json
                    FROM card_abilities a
                    JOIN cards c ON c.id = a.card_id
                    WHERE c.id = ?
                    ORDER BY a.ordinal
                    """,
                    (title, card["id"]),
                ).fetchall()
            )
    finally:
        conn.close()

    abilities_by_title: dict[str, list[dict[str, Any]]] = {}
    for row in ability_rows:
        item = dict(row)
        item["owner_units"] = json.loads(item["owner_units_json"]) if item["owner_units_json"] else None
        abilities_by_title.setdefault(item["lookup_title"], []).append(item)

    lines = [
        "# 多人一卡完整性清单",
        "",
        "这份报告列出查询网页背后的多人一卡事实层配置。`共同特技` 不是人物 unit，只是多名人物共享的特技归属组。",
        "",
        f"- 当前配置多人一卡：{len(titles)} 张",
        "",
    ]

    for title in titles:
        config = unit_overrides.get(title, {})
        card = cards.get(title)
        if card is None:
            lines.extend([f"## {title}", "", "- 数据库未找到这张卡。", ""])
            continue
        explicit_units = config.get("units", []) if isinstance(config, dict) else []
        unit_names = [unit.get("name") for unit in explicit_units if isinstance(unit, dict) and unit.get("name")]
        abilities = abilities_by_title.get(title, [])
        grouped: dict[str, list[dict[str, Any]]] = {}
        for ability in abilities:
            key = owner_key(ability.get("owner_units"), unit_names) or "未分配"
            grouped.setdefault(key, []).append(ability)

        shared = config.get("shared", {}) if isinstance(config, dict) else {}
        suppress_card_life = bool(config.get("suppress_card_life")) if isinstance(config, dict) else False
        card_life = card.get("life") if card else None
        shown_life = "不显示为整卡生命" if suppress_card_life else (card_life or "空")
        source_life = card_life or "空"
        shared_life = shared.get("life_pool") or "无"
        configured = bool(explicit_units)

        missing_fields: list[str] = []
        if not configured:
            missing_fields.append("尚未配置 unit 列表")
        for unit in explicit_units:
            if not isinstance(unit, dict):
                continue
            name = unit.get("name") or "未命名"
            if not unit.get("life") and shared_life == "无" and not card_life:
                missing_fields.append(f"{name}: 缺生命")
            if not unit.get("identity"):
                missing_fields.append(f"{name}: 身份空")
            if not unit.get("weapons"):
                missing_fields.append(f"{name}: 兵器空")

        lines.extend(
            [
                f"## {title}",
                "",
                f"- 位置：{card.get('source_sheet')}!{card.get('source_row')}" if card else "- 位置：数据库未找到",
                f"- 牌面/数据库生命：{source_life}",
                f"- 网页整卡生命：{shown_life}",
                f"- 共享生命池：{shared_life}",
                f"- 是否已有 unit 配置：{'是' if configured else '否'}",
                f"- 单元数：{len(unit_names)}",
                "",
                "### 单元",
                "",
            ]
        )

        for unit in explicit_units:
            if not isinstance(unit, dict):
                continue
            meta = []
            if unit.get("life"):
                meta.append(f"生命 {unit['life']}")
            if unit.get("entity_kind"):
                meta.append(f"属性 {unit['entity_kind']}")
            if unit.get("identity"):
                meta.append(f"身份 {unit['identity']}")
            if unit.get("weapons"):
                meta.append(f"兵器 {'、'.join(unit['weapons'])}")
            if unit.get("relationships"):
                meta.append(f"关系 {unit['relationships']}")
            lines.append(f"- {unit.get('name')}: {'；'.join(meta) if meta else '无单元元信息'}")

        lines.extend(["", "### 特技分组", ""])
        for group_name in sorted(grouped, key=lambda name: (name != "共同特技", name)):
            items = grouped[group_name]
            ability_names = "、".join(f"#{item['ordinal']} {item['name'] or '未命名'}" for item in items)
            lines.append(f"- {group_name}: {ability_names}")
        if not grouped:
            lines.append("- 无特技记录")

        lines.extend(["", "### 可能缺字段", ""])
        if missing_fields:
            for item in missing_fields:
                lines.append(f"- {item}")
        else:
            lines.append("- 未发现明显缺字段")
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(REPORT_PATH)


if __name__ == "__main__":
    main()
