from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median


ROOT = Path(__file__).resolve().parents[1]
CARDS_PATH = ROOT / "data" / "cards_current" / "all_cards.jsonl"
ABILITIES_PATH = ROOT / "data" / "cards_current" / "abilities.jsonl"
OUT_JSON = ROOT / "data" / "review" / "card_database_statistics.json"
OUT_MD = ROOT / "docs" / "card-database-statistics.md"


CATEGORY_LABELS = {
    "combat_characters": "战斗人物",
    "attached_characters": "附加人物",
    "items": "物品",
    "titles": "称号",
    "scenes": "场景",
    "deprecated": "废弃",
}


ABILITY_KIND_LABELS = {
    "说明": "说明/自由文本",
}


KEYWORD_GROUPS = {
    "不占名额/机会成本": ["不占名额", "不占.*名额"],
    "抢先/优先": ["抢先", "优先结算", "先结算", "先发动"],
    "一定造成/不可闪避": ["一定造成", "不可闪避", "无法闪避", "不能闪避"],
    "禁响应/失灵": ["不响应", "无法响应", "失灵", "屏蔽"],
    "清除/离场": ["清除", "离场", "退出", "破空", "消失"],
    "不在场/找不到/无此人": ["不在场", "找不到", "无此人"],
    "生命流失": ["生命流失", "流失", "失去生命"],
    "学习/复制": ["学会", "学习", "复制", "模仿", "获得特技"],
    "随机/掷骰": ["随机", "掷骰", "1/2", "1/6"],
    "胜负特判": ["胜利", "失败", "不算输", "并列", "名次"],
    "文本修改/人工裁定": ["删", "字", "文本", "抹去", "重新解释"],
    "牌堆/弃牌": ["摸", "抽", "弃牌", "弃牌堆", "本局弃卡", "洗回"],
}


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def as_label(category: str) -> str:
    return CATEGORY_LABELS.get(category, category)


def ability_kind_label(kind: str) -> str:
    return ABILITY_KIND_LABELS.get(kind, kind)


def compact_counter(counter: Counter, limit: int | None = None) -> dict:
    items = counter.most_common(limit)
    return {key: value for key, value in items}


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round((len(ordered) - 1) * pct)))
    return ordered[index]


def parse_life(value) -> list[int]:
    if value is None:
        return []
    if isinstance(value, int):
        return [value]
    text = str(value)
    return [int(x) for x in re.findall(r"(?<!\d)(\d{2,5})(?!\d)", text)]


def keyword_hits(text: str) -> dict[str, int]:
    result = {}
    for group, patterns in KEYWORD_GROUPS.items():
        hits = 0
        for pattern in patterns:
            if any(ch in pattern for ch in ".*+?[](){}|\\"):
                hits += len(re.findall(pattern, text))
            else:
                hits += text.count(pattern)
        if hits:
            result[group] = hits
    return result


def weapon_tokens(text: str) -> list[str]:
    return re.findall(r"【[^】]+】", text or "")


def build_statistics(cards: list[dict], abilities: list[dict]) -> dict:
    cards_by_id = {card["id"]: card for card in cards}
    abilities_by_card = defaultdict(list)
    for ability in abilities:
        abilities_by_card[ability["card_id"]].append(ability)

    category_counts = Counter(as_label(card["category"]) for card in cards)
    author_counts = Counter((card.get("fields") or {}).get("author_group") or "未标作者" for card in cards)
    source_work_counts = Counter((card.get("fields") or {}).get("source_work") or "未标出处" for card in cards)
    ability_kind_counts = Counter(ability_kind_label(ability.get("kind") or "未分类") for ability in abilities)
    ability_kind_by_category = defaultdict(Counter)
    exclusive_count = 0
    identity_ability_count = 0
    owner_unit_ability_count = 0
    review_flag_counts = Counter()
    source_field_counts = Counter()

    for ability in abilities:
        category = as_label(ability.get("card_category") or cards_by_id.get(ability["card_id"], {}).get("category", ""))
        ability_kind_by_category[category][ability_kind_label(ability.get("kind") or "未分类")] += 1
        if ability.get("is_exclusive"):
            exclusive_count += 1
        if ability.get("is_identity"):
            identity_ability_count += 1
        if ability.get("owner_units"):
            owner_unit_ability_count += 1
        for flag in ability.get("review_flags") or []:
            review_flag_counts[flag] += 1
        source_field_counts[ability.get("source_field") or "未标字段"] += 1

    ability_counts_per_card = [len(abilities_by_card[card["id"]]) for card in cards]
    ability_count_hist = Counter(ability_counts_per_card)
    high_ability_cards = sorted(
        (
            {
                "title": card["title"],
                "category": as_label(card["category"]),
                "ability_count": len(abilities_by_card[card["id"]]),
                "author_group": (card.get("fields") or {}).get("author_group"),
                "source_work": (card.get("fields") or {}).get("source_work"),
            }
            for card in cards
        ),
        key=lambda item: item["ability_count"],
        reverse=True,
    )[:30]

    text_lengths = [len(card.get("all_text") or "") for card in cards]
    high_text_cards = sorted(
        (
            {
                "title": card["title"],
                "category": as_label(card["category"]),
                "text_length": len(card.get("all_text") or ""),
                "ability_count": len(abilities_by_card[card["id"]]),
            }
            for card in cards
        ),
        key=lambda item: item["text_length"],
        reverse=True,
    )[:30]

    keyword_group_counts = Counter()
    keyword_group_cards = defaultdict(list)
    for card in cards:
        hits = keyword_hits(card.get("all_text") or "")
        for group, count in hits.items():
            keyword_group_counts[group] += 1
            keyword_group_cards[group].append(
                {
                    "title": card["title"],
                    "category": as_label(card["category"]),
                    "hits": count,
                }
            )

    for group in list(keyword_group_cards):
        keyword_group_cards[group] = sorted(keyword_group_cards[group], key=lambda item: item["hits"], reverse=True)[:25]

    weapon_counts = Counter()
    for card in cards:
        fields = card.get("fields") or {}
        weapon_text = "\n".join(str(fields.get(key) or "") for key in ["weapons", "traits", "item_category"])
        for token in weapon_tokens(weapon_text):
            weapon_counts[token] += 1

    life_values = []
    no_life_cards = []
    multi_life_cards = []
    for card in cards:
        if card["category"] not in {"combat_characters", "attached_characters", "deprecated"}:
            continue
        values = parse_life((card.get("fields") or {}).get("life"))
        if not values:
            no_life_cards.append({"title": card["title"], "category": as_label(card["category"])})
        elif len(values) > 1:
            multi_life_cards.append({"title": card["title"], "category": as_label(card["category"]), "life_values": values})
        life_values.extend(values)

    unit_cards = []
    for card in cards:
        card_abilities = abilities_by_card[card["id"]]
        owners = sorted({owner for ability in card_abilities for owner in (ability.get("owner_units") or [])})
        if owners:
            unit_cards.append(
                {
                    "title": card["title"],
                    "category": as_label(card["category"]),
                    "owner_units": owners,
                    "owner_unit_count": len(owners),
                    "unit_specific_ability_count": sum(1 for ability in card_abilities if ability.get("owner_units")),
                }
            )

    stats = {
        "card_count": len(cards),
        "ability_count": len(abilities),
        "notes": {
            "说明/自由文本": "不是正式特技类型，而是解析器兜底分类：牌面中没有可识别特技前缀，但仍是有效规则文字的段落。"
        },
        "category_counts": compact_counter(category_counts),
        "author_counts": compact_counter(author_counts),
        "source_work_top30": compact_counter(source_work_counts, 30),
        "ability_kind_counts": compact_counter(ability_kind_counts),
        "ability_kind_by_category": {category: compact_counter(counter) for category, counter in sorted(ability_kind_by_category.items())},
        "exclusive_ability_count": exclusive_count,
        "identity_ability_count": identity_ability_count,
        "owner_unit_ability_count": owner_unit_ability_count,
        "review_flag_counts": compact_counter(review_flag_counts),
        "source_field_counts": compact_counter(source_field_counts),
        "ability_count_per_card": {
            "min": min(ability_counts_per_card) if ability_counts_per_card else 0,
            "max": max(ability_counts_per_card) if ability_counts_per_card else 0,
            "mean": round(mean(ability_counts_per_card), 2) if ability_counts_per_card else 0,
            "median": median(ability_counts_per_card) if ability_counts_per_card else 0,
            "histogram": dict(sorted(ability_count_hist.items())),
        },
        "high_ability_cards": high_ability_cards,
        "text_length": {
            "min": min(text_lengths) if text_lengths else 0,
            "max": max(text_lengths) if text_lengths else 0,
            "mean": round(mean(text_lengths), 2) if text_lengths else 0,
            "median": median(text_lengths) if text_lengths else 0,
            "p90": percentile(text_lengths, 0.9),
        },
        "high_text_cards": high_text_cards,
        "keyword_group_card_counts": compact_counter(keyword_group_counts),
        "keyword_group_top_cards": dict(keyword_group_cards),
        "weapon_counts": compact_counter(weapon_counts),
        "life_stats": {
            "life_value_count": len(life_values),
            "min": min(life_values) if life_values else 0,
            "max": max(life_values) if life_values else 0,
            "mean": round(mean(life_values), 2) if life_values else 0,
            "median": median(life_values) if life_values else 0,
            "no_life_cards": no_life_cards[:80],
            "no_life_count": len(no_life_cards),
            "multi_life_cards": multi_life_cards,
            "multi_life_count": len(multi_life_cards),
        },
        "multi_unit_or_owner_unit_cards": unit_cards,
        "multi_unit_or_owner_unit_count": len(unit_cards),
    }
    return stats


def write_markdown(stats: dict) -> None:
    lines = [
        "# 卡牌数据库统计报告 v0.1",
        "",
        "- 来源：`data/cards_current/all_cards.jsonl` 与 `data/cards_current/abilities.jsonl`",
        "- 性质：统计报告，不修改源数据库。",
        "",
        "## 总览",
        "",
        f"- 卡牌总数：{stats['card_count']}",
        f"- 特技/说明条目总数：{stats['ability_count']}",
        f"- 专属特技数：{stats['exclusive_ability_count']}",
        f"- 身份特技数：{stats['identity_ability_count']}",
        f"- 带所属人物单元的特技数：{stats['owner_unit_ability_count']}",
        "",
        "## 卡牌类型",
        "",
    ]
    for key, value in stats["category_counts"].items():
        lines.append(f"- {key}: {value}")

    lines.extend(["", "## 特技类型", ""])
    for key, value in stats["ability_kind_counts"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(
        [
            "",
            "`说明/自由文本` 不是正式特技类型，而是解析器兜底分类：牌面中没有 `内功/招式/武功/技能/*/字` 等可识别前缀，",
            "但仍然是有效规则文字的段落。它主要来自物品、场景、称号、附加人物，以及少量战斗人物的开场说明或多人一卡总规则。",
        ]
    )

    lines.extend(["", "## 各卡牌类型下的特技类型", ""])
    for category, counter in stats["ability_kind_by_category"].items():
        parts = "，".join(f"{key}: {value}" for key, value in counter.items())
        lines.append(f"- {category}: {parts}")

    lines.extend(["", "## 每张卡特技数", ""])
    ac = stats["ability_count_per_card"]
    lines.extend(
        [
            f"- 最少：{ac['min']}",
            f"- 最多：{ac['max']}",
            f"- 平均：{ac['mean']}",
            f"- 中位数：{ac['median']}",
            "- 分布：" + "，".join(f"{key}条: {value}张" for key, value in ac["histogram"].items()),
            "",
            "### 特技数最多的卡",
            "",
        ]
    )
    for item in stats["high_ability_cards"][:20]:
        lines.append(f"- {item['title']}（{item['category']}）: {item['ability_count']} 条")

    lines.extend(["", "## 文本长度", ""])
    tl = stats["text_length"]
    lines.extend(
        [
            f"- 最短：{tl['min']}",
            f"- 最长：{tl['max']}",
            f"- 平均：{tl['mean']}",
            f"- 中位数：{tl['median']}",
            f"- P90：{tl['p90']}",
            "",
            "### 文本最长的卡",
            "",
        ]
    )
    for item in stats["high_text_cards"][:20]:
        lines.append(f"- {item['title']}（{item['category']}）: {item['text_length']} 字，{item['ability_count']} 条")

    lines.extend(["", "## 关键词机制统计", ""])
    for key, value in stats["keyword_group_card_counts"].items():
        lines.append(f"- {key}: {value} 张")

    lines.extend(["", "### 不占名额/机会成本相关卡", ""])
    for item in stats["keyword_group_top_cards"].get("不占名额/机会成本", [])[:30]:
        lines.append(f"- {item['title']}（{item['category']}）: 命中 {item['hits']}")

    lines.extend(["", "## 作者分布", ""])
    for key, value in stats["author_counts"].items():
        lines.append(f"- {key}: {value}")

    lines.extend(["", "## 出处 Top 30", ""])
    for key, value in stats["source_work_top30"].items():
        lines.append(f"- {key}: {value}")

    lines.extend(["", "## 兵器/特性标记", ""])
    for key, value in stats["weapon_counts"].items():
        lines.append(f"- {key}: {value}")

    lines.extend(["", "## 生命统计", ""])
    life = stats["life_stats"]
    lines.extend(
        [
            f"- 生命数值样本数：{life['life_value_count']}",
            f"- 最小生命：{life['min']}",
            f"- 最大生命：{life['max']}",
            f"- 平均生命：{life['mean']}",
            f"- 中位生命：{life['median']}",
            f"- 无生命字段人物/旧卡：{life['no_life_count']}",
            f"- 多生命数值卡：{life['multi_life_count']}",
        ]
    )
    if life["multi_life_cards"]:
        lines.extend(["", "### 多生命数值卡", ""])
        for item in life["multi_life_cards"]:
            lines.append(f"- {item['title']}（{item['category']}）: {item['life_values']}")

    lines.extend(["", "## 多人一卡/特技所属人物单元", ""])
    lines.append(f"- 带人物单元所属信息的卡：{stats['multi_unit_or_owner_unit_count']}")
    for item in stats["multi_unit_or_owner_unit_cards"][:60]:
        lines.append(
            f"- {item['title']}（{item['category']}）: {item['owner_unit_count']} 个所属单元，"
            f"{item['unit_specific_ability_count']} 条特技带所属"
        )

    lines.extend(
        [
            "",
            "## 评价模型提醒",
            "",
            "- 卡面强度和游玩强度应分开统计；`不占名额`、强制出战、额外出战等会显著降低机会成本。",
            "- `方恨少` 这类本体很弱但不占名额的卡，不应只按卡面强度评价。",
            "- 后续强度解释层应增加 `机会成本/出战名额价值` 维度。",
        ]
    )

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    cards = load_jsonl(CARDS_PATH)
    abilities = load_jsonl(ABILITIES_PATH)
    stats = build_statistics(cards, abilities)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(stats, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(stats)
    print(f"cards={stats['card_count']}")
    print(f"abilities={stats['ability_count']}")
    print(f"out={OUT_MD}")


if __name__ == "__main__":
    main()
