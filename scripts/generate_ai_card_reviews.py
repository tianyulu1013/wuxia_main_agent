from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import median


ROOT = Path(__file__).resolve().parents[1]
CARDS_PATH = ROOT / "data" / "cards_current" / "all_cards.jsonl"
OUT_DIR = ROOT / "data" / "review"
DOCS_DIR = ROOT / "docs"


CATEGORY_LABELS = {
    "combat_characters": "战斗人物",
    "attached_characters": "附加人物",
    "items": "物品",
    "titles": "称号",
    "scenes": "场景",
    "deprecated": "废弃",
}


DIMENSION_KEYWORDS = {
    "offense": {
        "label": "输出",
        "positive": [
            "攻击",
            "伤害",
            "输出",
            "击中",
            "击敌",
            "杀死",
            "彻底死亡",
            "灭杀",
            "流失",
            "失去生命",
            "先-",
        ],
    },
    "defense": {
        "label": "生存",
        "positive": [
            "无敌",
            "不中",
            "免疫",
            "不受",
            "无效",
            "闪避",
            "抵挡",
            "削减",
            "复活",
            "重生",
            "不会死亡",
            "不死",
            "回满",
            "回复",
            "回血",
            "留1血",
        ],
    },
    "control": {
        "label": "控制",
        "positive": [
            "禁",
            "异常",
            "失灵",
            "不响应",
            "无法",
            "不能",
            "控制",
            "改变",
            "指定",
            "随机",
            "动卡",
            "弃",
            "抽",
            "偷",
            "顺序",
            "找不到",
            "不在场",
            "离场",
            "清除",
        ],
    },
    "resource": {
        "label": "资源",
        "positive": [
            "摸",
            "抽",
            "补",
            "弃牌",
            "扩卡",
            "学会",
            "学习",
            "复制",
            "模仿",
            "获得",
            "得到",
            "归还",
            "刷新",
            "累积",
            "支付",
            "拿走",
        ],
    },
    "mobility_social": {
        "label": "位置/阵营",
        "positive": [
            "场景",
            "地点",
            "位置",
            "寻找",
            "到达",
            "结盟",
            "阵营",
            "一方",
            "盟主",
            "避战",
            "袭击",
        ],
    },
    "special_victory": {
        "label": "胜负特判",
        "positive": [
            "胜利",
            "失败",
            "不算输",
            "视为输",
            "视为胜",
            "并列",
            "名次",
            "破空",
            "退出",
        ],
    },
    "rule_disruption": {
        "label": "规则破坏",
        "positive": [
            "删",
            "字",
            "文本",
            "抹去",
            "改为",
            "视为",
            "重新",
            "任意时刻",
            "控制几率",
            "改变顺序",
            "不需",
            "无论",
        ],
    },
}


ROLE_PATTERNS = [
    ("爆发输出", ["彻底死亡", "灭杀", "杀死", "×", "*2", "x2", "输出", "击敌", "先-"]),
    ("持续输出", ["每回合", "/回合", "累积", "下回合", "持续", "毒"]),
    ("肉盾/生存", ["无敌", "不中", "免疫", "闪避", "抵挡", "削减", "复活", "重生", "不会死亡"]),
    ("控制/封锁", ["禁", "异常", "失灵", "无法", "不能", "不响应", "清除", "离场"]),
    ("资源/学习", ["摸", "抽", "扩卡", "学会", "学习", "复制", "模仿", "获得", "偷"]),
    ("位置/场景", ["场景", "地点", "不在场", "找不到", "寻找", "到达", "避战"]),
    ("阵营/结盟", ["结盟", "阵营", "一方", "盟主"]),
    ("胜负特判", ["胜利", "失败", "不算输", "并列", "破空"]),
    ("规则解释高风险", ["删", "字", "文本", "抹去", "控制几率", "改变顺序"]),
]


RISK_PATTERNS = [
    ("文本解释风险", ["删", "字", "文本", "抹去", "重新解释", "视为", "无论"]),
    ("结算顺序风险", ["顺序", "任意时刻", "同时", "立即", "之后", "此前", "此后"]),
    ("循环/累积风险", ["累积", "刷新", "再次", "每回合", "每次", "可重复", "不计次数"]),
    ("目标/来源风险", ["来源", "对象", "目标", "任一", "所有", "波及", "侧面", "非对阵"]),
    ("状态交互风险", ["异常", "禁", "不利", "有利", "失灵", "不中", "无效"]),
    ("空间状态风险", ["不在场", "找不到", "无此人", "离场", "场景", "地点", "消失"]),
    ("胜负裁定风险", ["胜利", "失败", "不算输", "破空", "并列", "退出"]),
    ("随机/人工裁定风险", ["随机", "掷骰", "几率", "控制几率", "暗中"]),
]


ELECTRONICIZATION_PATTERNS = [
    ("人工解释", ["删", "字", "文本", "抹去", "重新"]),
    ("隐藏信息", ["暗中", "不亮", "扣着", "观看", "秘密"]),
    ("随机控制", ["随机", "几率", "掷骰", "控制几率"]),
    ("动态目标/顺序", ["任意时刻", "改变", "顺序", "来源", "对象", "目标"]),
    ("空间系统", ["场景", "地点", "不在场", "找不到", "无此人", "离场", "消失"]),
    ("学习复制", ["学会", "学习", "复制", "模仿", "获得特技"]),
    ("多人一卡", ["七子", "二老", "四侠", "三人组", "共同", "两人", "各自"]),
]


def load_jsonl(path: Path) -> list[dict]:
    records = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def count_hits(text: str, keywords: list[str]) -> int:
    return sum(text.count(keyword) for keyword in keywords)


def number_features(text: str) -> dict:
    nums = [int(x) for x in re.findall(r"(?<!\d)(\d{2,5})(?!\d)", text)]
    damage_like = []
    for match in re.finditer(r"[-+](\d{2,5})|(\d{2,5})\s*(?:伤害|毒|冰|狂|迟|惊愕|攻|全|重生)", text):
        value = match.group(1) or match.group(2)
        if value:
            damage_like.append(int(value))
    return {
        "numbers": nums[:20],
        "max_number": max(nums) if nums else 0,
        "damage_numbers": damage_like[:20],
        "max_damage_number": max(damage_like) if damage_like else 0,
        "number_count": len(nums),
    }


def clamp(value: float, low: float = 1.0, high: float = 5.0) -> float:
    return max(low, min(high, value))


def stars(score: float) -> str:
    rounded = int(round(clamp(score)))
    return "★" * rounded + "☆" * (5 - rounded)


def score_from_hits(hit_count: int, extra: float = 0.0) -> float:
    return clamp(1.0 + min(2.8, hit_count * 0.48) + extra)


def classify_roles(text: str) -> list[str]:
    roles = []
    for role, keywords in ROLE_PATTERNS:
        if count_hits(text, keywords) > 0:
            roles.append(role)
    return roles[:6]


def classify_risks(text: str) -> list[dict]:
    risks = []
    for name, keywords in RISK_PATTERNS:
        hits = count_hits(text, keywords)
        if hits:
            risks.append({"name": name, "level": "高" if hits >= 3 else "中", "hits": hits})
    return sorted(risks, key=lambda item: (-item["hits"], item["name"]))[:8]


def classify_electronicization(text: str, ability_count: int) -> tuple[str, list[str], float]:
    reasons = []
    raw = 0.0
    for name, keywords in ELECTRONICIZATION_PATTERNS:
        hits = count_hits(text, keywords)
        if hits:
            reasons.append(name)
            raw += min(2.0, hits * 0.7)
    raw += min(2.0, max(0, ability_count - 3) * 0.35)
    if len(text) > 260:
        raw += 0.8
    if len(text) > 520:
        raw += 0.8
    if raw >= 5.0:
        level = "极高"
    elif raw >= 3.3:
        level = "高"
    elif raw >= 1.6:
        level = "中"
    else:
        level = "低"
    return level, reasons[:8], raw


def category_baseline(category: str) -> float:
    return {
        "combat_characters": 1.75,
        "attached_characters": 1.45,
        "items": 1.35,
        "titles": 1.3,
        "scenes": 1.35,
        "deprecated": 1.0,
    }.get(category, 1.5)


def first_pass(card: dict) -> dict:
    title = card.get("title", "")
    category = card.get("category", "")
    fields = card.get("fields") or {}
    abilities = card.get("abilities") or []
    text = card.get("all_text") or "\n".join(str(v) for v in fields.values() if v is not None)
    num = number_features(text)

    dimension_scores = {}
    hit_breakdown = {}
    for key, cfg in DIMENSION_KEYWORDS.items():
        hits = count_hits(text, cfg["positive"])
        hit_breakdown[key] = hits
        extra = 0.0
        if key == "offense":
            if num["max_damage_number"] >= 1000:
                extra += 0.8
            elif num["max_damage_number"] >= 500:
                extra += 0.45
            if "杀死" in text or "彻底死亡" in text or "灭杀" in text:
                extra += 0.8
        if key == "defense" and ("无敌" in text or "重生" in text or "复活" in text):
            extra += 0.7
        if key == "special_victory" and category in {"items", "titles", "scenes"}:
            extra -= 0.4
        dimension_scores[key] = round(score_from_hits(hits, extra), 2)

    ability_count = len(abilities)
    text_len = len(text)
    punctuation_load = text.count("；") + text.count("，") + text.count("：") + text.count("（")
    complexity_raw = (
        min(2.2, text_len / 240)
        + min(1.4, ability_count * 0.28)
        + min(1.0, punctuation_load / 30)
        + min(0.8, len(classify_risks(text)) * 0.11)
    )
    complexity = round(clamp(1.0 + complexity_raw), 2)

    electronicization_level, electronicization_reasons, electronicization_raw = classify_electronicization(text, ability_count)
    risks = classify_risks(text)
    roles = classify_roles(text)
    if not roles:
        roles = ["功能牌" if category in {"items", "titles", "scenes"} else "待观察"]

    offense = dimension_scores["offense"]
    defense = dimension_scores["defense"]
    control = dimension_scores["control"]
    resource = dimension_scores["resource"]
    special = dimension_scores["special_victory"]
    strength_raw = (
        category_baseline(category)
        + (offense - 1) * 0.34
        + (defense - 1) * 0.26
        + (control - 1) * 0.22
        + (resource - 1) * 0.14
        + (special - 1) * 0.28
    )
    if category == "deprecated":
        strength_raw = min(strength_raw, 2.0)
    strength = round(clamp(strength_raw), 2)

    confidence = "中"
    if text_len < 40:
        confidence = "低"
    elif text_len > 520 or len(risks) >= 5 or complexity >= 4.6:
        confidence = "中低"
    if category == "deprecated":
        confidence = "低"

    evidence = []
    if num["max_damage_number"]:
        evidence.append(f"最大显式数值约 {num['max_damage_number']}")
    if ability_count:
        evidence.append(f"解析特技 {ability_count} 条")
    top_dims = sorted(dimension_scores.items(), key=lambda kv: kv[1], reverse=True)[:3]
    evidence.extend(f"{DIMENSION_KEYWORDS[k]['label']} {v}" for k, v in top_dims if v > 1.2)

    return {
        "card_id": card.get("id"),
        "title": title,
        "category": category,
        "category_label": CATEGORY_LABELS.get(category, category),
        "source_work": fields.get("source_work"),
        "author_group": fields.get("author_group"),
        "life": fields.get("life"),
        "ability_count": ability_count,
        "text_length": text_len,
        "roles": roles,
        "tags": roles,
        "scores": {
            "strength_raw": strength,
            "strength_stars": stars(strength),
            "complexity": complexity,
            "complexity_stars": stars(complexity),
            "offense": dimension_scores["offense"],
            "defense": dimension_scores["defense"],
            "control": dimension_scores["control"],
            "resource": dimension_scores["resource"],
            "mobility_social": dimension_scores["mobility_social"],
            "special_victory": dimension_scores["special_victory"],
            "rule_disruption": dimension_scores["rule_disruption"],
        },
        "feature_hits": hit_breakdown,
        "number_features": num,
        "risks": risks,
        "electronicization": {
            "level": electronicization_level,
            "score_raw": round(electronicization_raw, 2),
            "reasons": electronicization_reasons,
        },
        "confidence": confidence,
        "evidence": evidence[:8],
        "ai_review": {
            "round": 1,
            "summary": build_summary_sentence(title, roles, strength, complexity, risks, electronicization_level),
            "limitations": "自动批量初评，只根据牌面文本和全库分布推断；不代表作者裁定，也不修改源数据库。",
        },
    }


def build_summary_sentence(title: str, roles: list[str], strength: float, complexity: float, risks: list[dict], electronicization: str) -> str:
    role_text = "、".join(roles[:3])
    risk_text = "，主要风险在" + "、".join(r["name"] for r in risks[:2]) if risks else ""
    return (
        f"{title} 的初步定位偏向 {role_text}；强度估计 {stars(strength)}，"
        f"复杂度 {stars(complexity)}，电子化难度 {electronicization}{risk_text}。"
    )


def percentile_rank(values: list[float], value: float) -> float:
    if not values:
        return 0.5
    below = sum(1 for item in values if item < value)
    equal = sum(1 for item in values if item == value)
    return (below + equal * 0.5) / len(values)


def second_pass(reviews: list[dict]) -> list[dict]:
    by_category = defaultdict(list)
    for review in reviews:
        by_category[review["category"]].append(review)

    all_strength = [r["scores"]["strength_raw"] for r in reviews]
    all_complexity = [r["scores"]["complexity"] for r in reviews]

    for review in reviews:
        category_reviews = by_category[review["category"]]
        category_strength = [r["scores"]["strength_raw"] for r in category_reviews]
        category_complexity = [r["scores"]["complexity"] for r in category_reviews]
        strength = review["scores"]["strength_raw"]
        complexity = review["scores"]["complexity"]
        global_strength_pct = percentile_rank(all_strength, strength)
        category_strength_pct = percentile_rank(category_strength, strength)
        global_complexity_pct = percentile_rank(all_complexity, complexity)
        category_complexity_pct = percentile_rank(category_complexity, complexity)

        adjusted_strength = strength
        if category_strength_pct >= 0.9 and strength < 4.4:
            adjusted_strength += 0.25
        if category_strength_pct <= 0.15 and strength > 1.5:
            adjusted_strength -= 0.2
        if review["electronicization"]["level"] in {"高", "极高"} and review["scores"]["rule_disruption"] >= 3.5:
            adjusted_strength += 0.1
        adjusted_strength = round(clamp(adjusted_strength), 2)

        needs_author_review = []
        if review["confidence"] in {"低", "中低"}:
            needs_author_review.append("自动理解置信度不高")
        if review["electronicization"]["level"] in {"高", "极高"}:
            needs_author_review.append("电子化/结算风险较高")
        if review["scores"]["rule_disruption"] >= 3.5:
            needs_author_review.append("规则解释或人工裁定成分较重")
        if category_complexity_pct >= 0.9:
            needs_author_review.append("同类复杂度前 10%")
        if category_strength_pct >= 0.95:
            needs_author_review.append("同类强度前 5%")

        review["scores"]["strength_adjusted"] = adjusted_strength
        review["scores"]["strength_adjusted_stars"] = stars(adjusted_strength)
        review["relative_position"] = {
            "global_strength_percentile": round(global_strength_pct, 3),
            "category_strength_percentile": round(category_strength_pct, 3),
            "global_complexity_percentile": round(global_complexity_pct, 3),
            "category_complexity_percentile": round(category_complexity_pct, 3),
        }
        review["ai_review_round2"] = {
            "round": 2,
            "summary": (
                f"第二轮按同类分布校正后，强度为 {stars(adjusted_strength)}；"
                f"同类强度分位 {category_strength_pct:.0%}，同类复杂度分位 {category_complexity_pct:.0%}。"
            ),
            "needs_author_review": needs_author_review,
        }
    return reviews


def write_jsonl(path: Path, records: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def top_cards(reviews: list[dict], key_path: tuple[str, ...], limit: int = 20) -> list[dict]:
    def get_value(record: dict) -> float:
        cur = record
        for key in key_path:
            cur = cur[key]
        return float(cur)

    return [
        {
            "title": r["title"],
            "category": r["category_label"],
            "value": get_value(r),
            "roles": r["roles"][:3],
            "risks": [risk["name"] for risk in r["risks"][:2]],
        }
        for r in sorted(reviews, key=get_value, reverse=True)[:limit]
    ]


def build_summary(reviews: list[dict]) -> dict:
    category_counts = Counter(r["category_label"] for r in reviews)
    role_counts = Counter(role for r in reviews for role in r["roles"])
    risk_counts = Counter(risk["name"] for r in reviews for risk in r["risks"])
    electronicization_counts = Counter(r["electronicization"]["level"] for r in reviews)
    needs_review = [r for r in reviews if r["ai_review_round2"]["needs_author_review"]]

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": "data/cards_current/all_cards.jsonl",
        "review_count": len(reviews),
        "category_counts": dict(category_counts),
        "role_counts": dict(role_counts.most_common()),
        "risk_counts": dict(risk_counts.most_common()),
        "electronicization_counts": dict(electronicization_counts),
        "median_strength_adjusted": median(r["scores"]["strength_adjusted"] for r in reviews),
        "median_complexity": median(r["scores"]["complexity"] for r in reviews),
        "needs_author_review_count": len(needs_review),
        "top_strength": top_cards(reviews, ("scores", "strength_adjusted")),
        "top_complexity": top_cards(reviews, ("scores", "complexity")),
        "top_rule_disruption": top_cards(reviews, ("scores", "rule_disruption")),
        "highest_electronicization_risk": [
            {
                "title": r["title"],
                "category": r["category_label"],
                "level": r["electronicization"]["level"],
                "score_raw": r["electronicization"]["score_raw"],
                "reasons": r["electronicization"]["reasons"],
            }
            for r in sorted(reviews, key=lambda x: x["electronicization"]["score_raw"], reverse=True)[:30]
        ],
    }


def write_markdown(summary: dict, reviews: list[dict]) -> None:
    lines = [
        "# AI 卡牌评价批量报告 v0.1",
        "",
        f"- 生成时间：{summary['generated_at_utc']}",
        f"- 来源：`{summary['source']}`",
        f"- 评价数量：{summary['review_count']}",
        "- 性质：独立评语层，不修改源数据库、Excel、SQLite 或牌面事实。",
        "",
        "## 分类数量",
        "",
    ]
    for name, count in summary["category_counts"].items():
        lines.append(f"- {name}: {count}")

    lines.extend(["", "## 角色标签分布", ""])
    for name, count in list(summary["role_counts"].items())[:20]:
        lines.append(f"- {name}: {count}")

    lines.extend(["", "## 风险标签分布", ""])
    for name, count in list(summary["risk_counts"].items())[:20]:
        lines.append(f"- {name}: {count}")

    lines.extend(["", "## 强度初评前 20", ""])
    for item in summary["top_strength"]:
        lines.append(f"- {item['title']}（{item['category']}）: {item['value']}，{', '.join(item['roles'])}")

    lines.extend(["", "## 复杂度前 20", ""])
    for item in summary["top_complexity"]:
        lines.append(f"- {item['title']}（{item['category']}）: {item['value']}，{', '.join(item['roles'])}")

    lines.extend(["", "## 规则破坏/解释风险前 20", ""])
    for item in summary["top_rule_disruption"]:
        risk_text = "、".join(item["risks"]) if item["risks"] else "无显式风险标签"
        lines.append(f"- {item['title']}（{item['category']}）: {item['value']}，{risk_text}")

    lines.extend(["", "## 电子化风险最高 30", ""])
    for item in summary["highest_electronicization_risk"]:
        lines.append(f"- {item['title']}（{item['category']}）: {item['level']} / {item['score_raw']}，{', '.join(item['reasons'])}")

    lines.extend(
        [
            "",
            "## 明天建议先看的内容",
            "",
            "1. 先看 `data/review/ai_card_reviews_summary.json` 的 `top_strength`、`top_complexity`、`highest_electronicization_risk`。",
            "2. 再抽查 `data/review/ai_card_reviews_round2.jsonl` 中 `ai_review_round2.needs_author_review` 非空的卡。",
            "3. 如果某类判断偏差明显，直接修改评价脚本的关键词/权重后重跑；不要改源数据库。",
        ]
    )

    (DOCS_DIR / "ai-card-review-batch-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def average(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def write_understanding_map(reviews: list[dict]) -> None:
    by_author = defaultdict(list)
    by_category = defaultdict(list)
    by_role = defaultdict(list)
    for review in reviews:
        by_author[review.get("author_group") or "未标作者"].append(review)
        by_category[review["category_label"]].append(review)
        for role in review["roles"]:
            by_role[role].append(review)

    lines = [
        "# AI 卡牌理解地图 v0.1",
        "",
        "这份文件是第二轮评价后的聚合理解，用来帮助后续继续修正 AI 对卡牌体系的认识。",
        "",
        "注意：这不是规则事实层，不得反向改写数据库、Excel 或牌面。",
        "",
        "## 作者组画像",
        "",
    ]

    for author, items in sorted(by_author.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        role_counts = Counter(role for r in items for role in r["roles"])
        risk_counts = Counter(risk["name"] for r in items for risk in r["risks"])
        electronic_high = sum(1 for r in items if r["electronicization"]["level"] in {"高", "极高"})
        lines.extend(
            [
                f"### {author}",
                "",
                f"- 卡牌数：{len(items)}",
                f"- 平均强度：{average([r['scores']['strength_adjusted'] for r in items]):.2f}",
                f"- 平均复杂度：{average([r['scores']['complexity'] for r in items]):.2f}",
                f"- 高/极高电子化风险：{electronic_high}",
                f"- 主要定位：{', '.join(name for name, _ in role_counts.most_common(5)) or '无'}",
                f"- 主要风险：{', '.join(name for name, _ in risk_counts.most_common(5)) or '无'}",
                "",
            ]
        )

    lines.extend(["## 类别画像", ""])
    for category, items in sorted(by_category.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        lines.extend(
            [
                f"### {category}",
                "",
                f"- 数量：{len(items)}",
                f"- 平均强度：{average([r['scores']['strength_adjusted'] for r in items]):.2f}",
                f"- 平均复杂度：{average([r['scores']['complexity'] for r in items]):.2f}",
                f"- 复杂度前五：{', '.join(r['title'] for r in sorted(items, key=lambda r: r['scores']['complexity'], reverse=True)[:5])}",
                f"- 强度前五：{', '.join(r['title'] for r in sorted(items, key=lambda r: r['scores']['strength_adjusted'], reverse=True)[:5])}",
                "",
            ]
        )

    lines.extend(["## 角色群画像", ""])
    for role, items in sorted(by_role.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        if len(items) < 8:
            continue
        lines.extend(
            [
                f"### {role}",
                "",
                f"- 数量：{len(items)}",
                f"- 平均强度：{average([r['scores']['strength_adjusted'] for r in items]):.2f}",
                f"- 平均复杂度：{average([r['scores']['complexity'] for r in items]):.2f}",
                f"- 代表性高强卡：{', '.join(r['title'] for r in sorted(items, key=lambda r: r['scores']['strength_adjusted'], reverse=True)[:8])}",
                "",
            ]
        )

    lines.extend(
        [
            "## 第二轮后的自我修正",
            "",
            "- 强度不是平衡判断，只是从文本中估计“对局影响力”；你的游戏本身不追求单局平衡。",
            "- 复杂度和电子化风险比强度更值得优先看，因为它们更接近规则稳定性问题。",
            "- 规则解释高风险卡不等于坏卡，很多是这个游戏最有味道的卡；只是需要人工裁定边界。",
            "- 后续如果你纠正某张卡的定位，应该写入评语层，作为下一轮评价的人工样本。",
        ]
    )

    (DOCS_DIR / "ai-card-review-understanding-map.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cards = load_jsonl(CARDS_PATH)
    round1 = [first_pass(card) for card in cards]
    round2 = second_pass(json.loads(json.dumps(round1, ensure_ascii=False)))
    summary = build_summary(round2)

    write_jsonl(OUT_DIR / "ai_card_reviews_round1.jsonl", round1)
    write_jsonl(OUT_DIR / "ai_card_reviews_round2.jsonl", round2)
    write_json(OUT_DIR / "ai_card_reviews_summary.json", summary)
    write_markdown(summary, round2)
    write_understanding_map(round2)

    print(f"reviewed={len(round2)}")
    print(f"needs_author_review={summary['needs_author_review_count']}")
    print(f"outputs={OUT_DIR}")


if __name__ == "__main__":
    main()
