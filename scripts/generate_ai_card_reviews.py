from __future__ import annotations

import json
import math
import re
import csv
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


RULE_CONCEPT_PATTERNS = {
    "attack_damage_life_loss": {
        "label": "攻击/伤害/生命流失",
        "terms": ["攻击", "伤害", "生命流失", "流失", "失去生命", "受伤", "扣"],
        "note": "规则书需区分攻击、伤害与生命流失；生命流失扣生命但不算攻击或伤害。",
    },
    "kill_death_life": {
        "label": "杀死/死亡/生命",
        "terms": ["杀死", "死亡", "彻底死亡", "灭杀", "生命", "血", "重生", "复活"],
        "note": "杀死可能绕过生命扣减；无生命属性、多生命阶段和重生应独立判断。",
    },
    "leaving_presence": {
        "label": "离场/不在场/找不到/无此人",
        "terms": ["离场", "不在场", "找不到", "无此人", "消失", "破空", "退出"],
        "note": "离场不等于死亡；找不到、无此人、不在场应保留独立状态。",
    },
    "clear_card_object": {
        "label": "清除/卡与人物单元",
        "terms": ["清除", "人物单元", "这张卡", "卡上", "附加人物", "称号", "物品"],
        "note": "清除针对卡而不是单个人物单元，可能牵连卡上的其他对象。",
    },
    "turn_round_timing": {
        "label": "回合/轮/时机",
        "terms": ["回合", "下回合", "每回合", "轮", "下轮", "转轮", "任意时刻", "立即", "同时"],
        "note": "回合与轮不同；任意时刻、立即、同时会提高结算顺序风险。",
    },
    "scene_location": {
        "label": "场景/地点/空间",
        "terms": ["场景", "地点", "位置", "到达", "寻找", "山庄", "空间"],
        "note": "场景是全局环境，地点是位置概念；卡牌可制造多个地点或特殊空间。",
    },
    "deck_discard_zones": {
        "label": "牌堆/弃牌/本局弃卡",
        "terms": ["摸", "抽", "弃", "弃牌", "弃牌堆", "本局弃卡", "洗回", "补抽"],
        "note": "抽牌堆、弃牌堆、本局弃卡堆是不同区域，随机弃和自己弃的去向不同。",
    },
    "ability_learning_copy": {
        "label": "学习/复制/特技所有权",
        "terms": ["学会", "学习", "复制", "模仿", "偷走", "获得特技", "失去特技", "特技失灵"],
        "note": "学习、复制、屏蔽、失去特技需要区分特技名称、特技文本与所属人物。",
    },
    "exclusive_identity": {
        "label": "专属/身份",
        "terms": ["身份", "（身份）"],
        "note": "专属以特技名两侧【】判断；身份描述与身份特技都可能产生身份属性。",
    },
    "faction_alliance_player_side": {
        "label": "玩家/一方/阵营/结盟",
        "terms": ["玩家", "一方", "阵营", "结盟", "盟主", "非己方", "己方"],
        "note": "玩家、一方、阵营、结盟是不同层级，不应混同。",
    },
    "manual_text_ruling": {
        "label": "文本修改/人工裁定",
        "terms": ["删", "字", "文本", "抹去", "重新解释", "只剩", "控制几率"],
        "note": "文本修改类效果短期应进入人工裁定层，不强求程序化。",
    },
    "multi_unit": {
        "label": "多人一卡/共享生命",
        "terms": ["七子", "二老", "四侠", "三人组", "两人", "各自", "共同", "共享", "全体"],
        "note": "多人一卡需要区分物理卡、人物单元、共同特技和共享生命池。",
    },
}


RULE_CONCEPT_WEIGHTS = {
    "attack_damage_life_loss": 0.35,
    "kill_death_life": 0.45,
    "leaving_presence": 0.9,
    "clear_card_object": 0.85,
    "turn_round_timing": 0.55,
    "scene_location": 0.75,
    "deck_discard_zones": 0.65,
    "ability_learning_copy": 0.7,
    "exclusive_identity": 0.25,
    "faction_alliance_player_side": 0.25,
    "manual_text_ruling": 1.15,
    "multi_unit": 1.0,
}


CONCEPT_TO_ROLES = {
    "attack_damage_life_loss": None,
    "kill_death_life": None,
    "leaving_presence": "空间/离场裁定",
    "clear_card_object": "对象清除裁定",
    "turn_round_timing": None,
    "scene_location": "位置/场景",
    "deck_discard_zones": "资源/牌堆",
    "ability_learning_copy": "资源/学习",
    "exclusive_identity": None,
    "faction_alliance_player_side": None,
    "manual_text_ruling": "人工裁定",
    "multi_unit": "多人一卡",
}


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


def detect_rule_concepts(text: str, card: dict | None = None) -> list[dict]:
    concepts = []
    for key, cfg in RULE_CONCEPT_PATTERNS.items():
        hits = {term: text.count(term) for term in cfg["terms"] if text.count(term)}
        if key == "attack_damage_life_loss":
            has_life_loss = any(term in text for term in ["生命流失", "流失", "失去生命"])
            has_attack_damage_pair = "攻击" in text and "伤害" in text
            if not (has_life_loss or has_attack_damage_pair):
                hits = {}
        elif key == "turn_round_timing":
            timing_terms = ["轮", "任意时刻", "同时", "立即", "下轮", "转轮"]
            has_specific_timing = any(term in text for term in timing_terms)
            has_dense_turn_text = text.count("回合") >= 3
            if not (has_specific_timing or has_dense_turn_text):
                hits = {}
        elif key == "exclusive_identity" and card is not None:
            fields = card.get("fields") or {}
            abilities = card.get("abilities") or []
            hits = {}
            identity_text = str(fields.get("identity") or fields.get("description_identity") or "")
            if identity_text:
                hits["身份字段"] = 1
            identity_ability_count = sum(1 for ability in abilities if ability.get("is_identity"))
            exclusive_ability_count = sum(1 for ability in abilities if ability.get("is_exclusive"))
            if identity_ability_count:
                hits["身份特技"] = identity_ability_count
            if exclusive_ability_count:
                hits["专属特技"] = exclusive_ability_count
        if not hits:
            continue
        score = sum(hits.values())
        concepts.append(
            {
                "key": key,
                "label": cfg["label"],
                "hits": hits,
                "score": score,
                "note": cfg["note"],
            }
        )
    return sorted(concepts, key=lambda item: (-item["score"], item["label"]))


def concept_keys(concepts: list[dict]) -> set[str]:
    return {concept["key"] for concept in concepts}


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
    rule_concepts = detect_rule_concepts(text, card)

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
    if rule_concepts:
        evidence.append("规则概念：" + "、".join(concept["label"] for concept in rule_concepts[:3]))
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
        "rule_concepts": rule_concepts,
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


def third_pass_rule_aware(reviews: list[dict]) -> list[dict]:
    for review in reviews:
        concepts = review.get("rule_concepts") or []
        keys = concept_keys(concepts)
        roles = list(review["roles"])
        risks = list(review["risks"])
        electronic_reasons = list(review["electronicization"]["reasons"])

        for key in keys:
            role = CONCEPT_TO_ROLES.get(key)
            if role and role not in roles:
                roles.append(role)

        concept_text = json.dumps(concepts, ensure_ascii=False)
        if "attack_damage_life_loss" in keys and any(term in concept_text for term in ["生命流失", "流失", "失去生命"]):
            risks.append({"name": "攻击/伤害/生命流失概念边界", "level": "中", "hits": 1})
        if "clear_card_object" in keys:
            risks.append({"name": "卡对象与人物单元边界", "level": "中", "hits": 1})
        if "turn_round_timing" in keys and any(term in concept_text for term in ["轮", "任意时刻", "同时"]):
            risks.append({"name": "回合/轮/时机边界", "level": "中", "hits": 1})
        if "leaving_presence" in keys:
            risks.append({"name": "存在状态边界", "level": "中", "hits": 1})
        if "manual_text_ruling" in keys:
            risks.append({"name": "人工裁定边界", "level": "高", "hits": 1})
        if "multi_unit" in keys:
            risks.append({"name": "多人一卡结构边界", "level": "中", "hits": 1})

        if "manual_text_ruling" in keys and "人工解释" not in electronic_reasons:
            electronic_reasons.append("人工解释")
        if {"leaving_presence", "scene_location"} & keys and "空间系统" not in electronic_reasons:
            electronic_reasons.append("空间系统")
        if "turn_round_timing" in keys and "动态目标/顺序" not in electronic_reasons:
            electronic_reasons.append("动态目标/顺序")
        if "multi_unit" in keys and "多人一卡" not in electronic_reasons:
            electronic_reasons.append("多人一卡")
        if "deck_discard_zones" in keys and "牌堆区域" not in electronic_reasons:
            electronic_reasons.append("牌堆区域")

        concept_load = sum(min(4, concept["score"]) for concept in concepts)
        rule_boundary_score = 1.0 + sum(RULE_CONCEPT_WEIGHTS.get(concept["key"], 0.4) for concept in concepts)
        rule_boundary_score += min(0.8, concept_load * 0.03)
        if {"manual_text_ruling", "multi_unit", "leaving_presence"} & keys:
            rule_boundary_score += 0.35
        if {"turn_round_timing", "clear_card_object", "attack_damage_life_loss"} & keys:
            rule_boundary_score += 0.18
        rule_boundary_score = min(5.0, rule_boundary_score)

        complexity_rule_adjusted = review["scores"]["complexity"]
        if rule_boundary_score >= 4.2:
            complexity_rule_adjusted = min(5.0, complexity_rule_adjusted + 0.25)
        if "manual_text_ruling" in keys:
            complexity_rule_adjusted = min(5.0, complexity_rule_adjusted + 0.25)

        strength_rule_adjusted = review["scores"]["strength_adjusted"]
        # 规则复杂不自动等于强。只有胜负、杀死、清除、稳定无敌类概念才轻微提高影响力估计。
        if {"kill_death_life", "clear_card_object"} & keys:
            strength_rule_adjusted = min(5.0, strength_rule_adjusted + 0.08)
        if "special_victory" in review["feature_hits"] and review["feature_hits"]["special_victory"] >= 2:
            strength_rule_adjusted = min(5.0, strength_rule_adjusted + 0.08)

        deduped_risks = {}
        for risk in risks:
            existing = deduped_risks.get(risk["name"])
            if existing is None or risk["hits"] > existing["hits"] or risk["level"] == "高":
                deduped_risks[risk["name"]] = risk

        review["roles"] = roles[:10]
        review["tags"] = review["roles"]
        review["risks"] = sorted(deduped_risks.values(), key=lambda item: (-item["hits"], item["name"]))[:12]
        review["electronicization"]["reasons"] = electronic_reasons[:10]
        review["scores"]["rule_boundary"] = round(rule_boundary_score, 2)
        review["scores"]["complexity_rule_adjusted"] = round(complexity_rule_adjusted, 2)
        review["scores"]["complexity_rule_adjusted_stars"] = stars(complexity_rule_adjusted)
        review["scores"]["strength_rule_adjusted"] = round(strength_rule_adjusted, 2)
        review["scores"]["strength_rule_adjusted_stars"] = stars(strength_rule_adjusted)
        review["ai_review_round3"] = {
            "round": 3,
            "basis": "结合规则书审计和已确认规则素材，对规则概念边界进行标注；仍为评语层。",
            "rule_concepts": [concept["label"] for concept in concepts],
            "summary": build_round3_summary(review),
        }
    return reviews


def build_round3_summary(review: dict) -> str:
    concepts = [concept["label"] for concept in review.get("rule_concepts", [])[:4]]
    if not concepts:
        return "第三轮未发现需要特别规则概念校正的文本，沿用第二轮评价。"
    return (
        "第三轮识别到规则概念："
        + "、".join(concepts)
        + f"；规则边界复杂度 {review['scores']['rule_boundary']}。"
    )


def fourth_pass_converge(reviews: list[dict]) -> list[dict]:
    by_category = defaultdict(list)
    for review in reviews:
        by_category[review["category"]].append(review)

    for review in reviews:
        category_reviews = by_category[review["category"]]
        rule_values = [r["scores"].get("rule_boundary", 1.0) for r in category_reviews]
        final_strength = review["scores"].get("strength_rule_adjusted", review["scores"]["strength_adjusted"])
        final_complexity = review["scores"].get("complexity_rule_adjusted", review["scores"]["complexity"])
        rule_pct = percentile_rank(rule_values, review["scores"].get("rule_boundary", 1.0))

        final_watch_reasons = []
        if review["electronicization"]["level"] in {"高", "极高"}:
            final_watch_reasons.append("电子化/结算风险较高")
        if review["scores"].get("rule_boundary", 1.0) >= 4.0:
            final_watch_reasons.append("规则概念边界复杂")
        if rule_pct >= 0.9:
            final_watch_reasons.append("同类规则边界复杂度前 10%")
        if review["relative_position"]["category_complexity_percentile"] >= 0.92:
            final_watch_reasons.append("同类文本复杂度靠前")
        if review["relative_position"]["category_strength_percentile"] >= 0.96:
            final_watch_reasons.append("同类影响力靠前")
        if "人工裁定边界" in [risk["name"] for risk in review["risks"]]:
            final_watch_reasons.append("人工裁定边界")
        if review["confidence"] == "低":
            final_watch_reasons.append("自动理解置信度低")

        review["scores"]["final_strength"] = round(final_strength, 2)
        review["scores"]["final_strength_stars"] = stars(final_strength)
        review["scores"]["final_complexity"] = round(final_complexity, 2)
        review["scores"]["final_complexity_stars"] = stars(final_complexity)
        review["relative_position"]["category_rule_boundary_percentile"] = round(rule_pct, 3)
        review["ai_review_round4"] = {
            "round": 4,
            "summary": (
                f"第四轮收敛：最终影响力 {stars(final_strength)}，最终复杂度 {stars(final_complexity)}；"
                f"规则边界分位 {rule_pct:.0%}。"
            ),
            "watch_reasons": final_watch_reasons,
        }
    return reviews


def write_jsonl(path: Path, records: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, reviews: list[dict]) -> None:
    columns = [
        "title",
        "category_label",
        "author_group",
        "source_work",
        "life",
        "final_strength",
        "strength_stars",
        "final_complexity",
        "complexity_stars",
        "rule_boundary",
        "electronicization_level",
        "roles",
        "rule_concepts",
        "risks",
        "needs_author_review",
        "summary",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for review in reviews:
            writer.writerow(
                {
                    "title": review["title"],
                    "category_label": review["category_label"],
                    "author_group": review.get("author_group") or "",
                    "source_work": review.get("source_work") or "",
                    "life": review.get("life") if review.get("life") is not None else "",
                    "final_strength": review["scores"].get("final_strength", review["scores"]["strength_adjusted"]),
                    "strength_stars": review["scores"].get("final_strength_stars", review["scores"]["strength_adjusted_stars"]),
                    "final_complexity": review["scores"].get("final_complexity", review["scores"]["complexity"]),
                    "complexity_stars": review["scores"].get("final_complexity_stars", review["scores"]["complexity_stars"]),
                    "rule_boundary": review["scores"].get("rule_boundary", ""),
                    "electronicization_level": review["electronicization"]["level"],
                    "roles": "、".join(review["roles"]),
                    "rule_concepts": "、".join(concept["label"] for concept in review.get("rule_concepts", [])),
                    "risks": "、".join(risk["name"] for risk in review["risks"]),
                    "needs_author_review": "、".join(review.get("ai_review_round4", {}).get("watch_reasons", review["ai_review_round2"]["needs_author_review"])),
                    "summary": review.get("ai_review_round4", review["ai_review_round2"])["summary"],
                }
            )


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
    needs_review = [r for r in reviews if r.get("ai_review_round4", {}).get("watch_reasons", r["ai_review_round2"]["needs_author_review"])]
    rule_concept_counts = Counter(concept["label"] for r in reviews for concept in r.get("rule_concepts", []))

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": "data/cards_current/all_cards.jsonl",
        "review_count": len(reviews),
        "category_counts": dict(category_counts),
        "role_counts": dict(role_counts.most_common()),
        "risk_counts": dict(risk_counts.most_common()),
        "rule_concept_counts": dict(rule_concept_counts.most_common()),
        "electronicization_counts": dict(electronicization_counts),
        "median_strength_adjusted": median(r["scores"].get("final_strength", r["scores"]["strength_adjusted"]) for r in reviews),
        "median_complexity": median(r["scores"].get("final_complexity", r["scores"]["complexity"]) for r in reviews),
        "needs_author_review_count": len(needs_review),
        "top_strength": top_cards(reviews, ("scores", "final_strength")),
        "top_complexity": top_cards(reviews, ("scores", "final_complexity")),
        "top_rule_boundary": top_cards(reviews, ("scores", "rule_boundary")),
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

    lines.extend(["", "## 规则概念分布", ""])
    for name, count in list(summary["rule_concept_counts"].items())[:20]:
        lines.append(f"- {name}: {count}")

    lines.extend(["", "## 最终影响力前 20", ""])
    for item in summary["top_strength"]:
        lines.append(f"- {item['title']}（{item['category']}）: {item['value']}，{', '.join(item['roles'])}")

    lines.extend(["", "## 最终复杂度前 20", ""])
    for item in summary["top_complexity"]:
        lines.append(f"- {item['title']}（{item['category']}）: {item['value']}，{', '.join(item['roles'])}")

    lines.extend(["", "## 规则边界复杂度前 20", ""])
    for item in summary["top_rule_boundary"]:
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
            "1. 先看 `data/review/ai_card_reviews_summary.json` 的 `top_strength`、`top_complexity`、`top_rule_boundary`、`highest_electronicization_risk`。",
            "2. 再抽查 `data/review/ai_card_reviews_round4.jsonl` 中 `ai_review_round4.watch_reasons` 非空的卡。",
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
                f"- 平均最终影响力：{average([r['scores'].get('final_strength', r['scores']['strength_adjusted']) for r in items]):.2f}",
                f"- 平均最终复杂度：{average([r['scores'].get('final_complexity', r['scores']['complexity']) for r in items]):.2f}",
                f"- 平均规则边界：{average([r['scores'].get('rule_boundary', 1.0) for r in items]):.2f}",
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
                f"- 平均最终影响力：{average([r['scores'].get('final_strength', r['scores']['strength_adjusted']) for r in items]):.2f}",
                f"- 平均最终复杂度：{average([r['scores'].get('final_complexity', r['scores']['complexity']) for r in items]):.2f}",
                f"- 平均规则边界：{average([r['scores'].get('rule_boundary', 1.0) for r in items]):.2f}",
                f"- 复杂度前五：{', '.join(r['title'] for r in sorted(items, key=lambda r: r['scores'].get('final_complexity', r['scores']['complexity']), reverse=True)[:5])}",
                f"- 影响力前五：{', '.join(r['title'] for r in sorted(items, key=lambda r: r['scores'].get('final_strength', r['scores']['strength_adjusted']), reverse=True)[:5])}",
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
                f"- 平均最终影响力：{average([r['scores'].get('final_strength', r['scores']['strength_adjusted']) for r in items]):.2f}",
                f"- 平均最终复杂度：{average([r['scores'].get('final_complexity', r['scores']['complexity']) for r in items]):.2f}",
                f"- 代表性高影响力卡：{', '.join(r['title'] for r in sorted(items, key=lambda r: r['scores'].get('final_strength', r['scores']['strength_adjusted']), reverse=True)[:8])}",
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
            "- 第三轮开始引入规则书和已确认规则素材，重点修正攻击/伤害/生命流失、回合/轮、离场/清除、人物单元、场景/地点等概念边界。",
            "- 后续如果你纠正某张卡的定位，应该写入评语层，作为下一轮评价的人工样本。",
        ]
    )

    (DOCS_DIR / "ai-card-review-understanding-map.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_author_watchlist(reviews: list[dict]) -> None:
    watchlist = [r for r in reviews if r.get("ai_review_round4", {}).get("watch_reasons")]
    watchlist.sort(
        key=lambda r: (
            r["electronicization"]["score_raw"],
            r["scores"].get("rule_boundary", 1.0),
            r["scores"].get("final_complexity", r["scores"]["complexity"]),
            r["scores"].get("final_strength", r["scores"]["strength_adjusted"]),
        ),
        reverse=True,
    )

    lines = [
        "# AI 卡牌评价作者复核清单 v0.1",
        "",
        f"- 复核卡牌数：{len(watchlist)}",
        "- 目的：列出 AI 第四轮后仍认为需要作者纠偏、确认或重点看的卡。",
        "- 注意：这是评语层清单，不是改卡建议，也不改源数据库。",
        "",
    ]

    by_reason = Counter(reason for r in watchlist for reason in r["ai_review_round4"]["watch_reasons"])
    lines.extend(["## 复核原因统计", ""])
    for reason, count in by_reason.most_common():
        lines.append(f"- {reason}: {count}")

    lines.extend(["", "## 复核列表", ""])
    for index, review in enumerate(watchlist, start=1):
        reasons = "、".join(review["ai_review_round4"]["watch_reasons"])
        risks = "、".join(risk["name"] for risk in review["risks"][:4]) or "无显式风险标签"
        roles = "、".join(review["roles"][:5])
        concepts = "、".join(concept["label"] for concept in review.get("rule_concepts", [])[:6]) or "无显式规则概念"
        lines.extend(
            [
                f"### {index}. {review['title']}（{review['category_label']}）",
                "",
                f"- 作者/出处：{review.get('author_group') or '未标'} / {review.get('source_work') or '未标'}",
                f"- 定位：{roles}",
                f"- 最终影响力：{review['scores']['final_strength']} {review['scores']['final_strength_stars']}；最终复杂度：{review['scores']['final_complexity']} {review['scores']['final_complexity_stars']}；规则边界：{review['scores']['rule_boundary']}",
                f"- 电子化风险：{review['electronicization']['level']}（{', '.join(review['electronicization']['reasons']) or '无'}）",
                f"- 规则概念：{concepts}",
                f"- 复核原因：{reasons}",
                f"- 风险标签：{risks}",
                f"- AI 摘要：{review['ai_review_round4']['summary']}",
                "",
            ]
        )

    (DOCS_DIR / "ai-card-review-author-watchlist.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cards = load_jsonl(CARDS_PATH)
    round1 = [first_pass(card) for card in cards]
    round2 = second_pass(json.loads(json.dumps(round1, ensure_ascii=False)))
    round3 = third_pass_rule_aware(json.loads(json.dumps(round2, ensure_ascii=False)))
    round4 = fourth_pass_converge(json.loads(json.dumps(round3, ensure_ascii=False)))
    summary = build_summary(round4)

    write_jsonl(OUT_DIR / "ai_card_reviews_round1.jsonl", round1)
    write_jsonl(OUT_DIR / "ai_card_reviews_round2.jsonl", round2)
    write_csv(OUT_DIR / "ai_card_reviews_round2.csv", round2)
    write_jsonl(OUT_DIR / "ai_card_reviews_round3.jsonl", round3)
    write_jsonl(OUT_DIR / "ai_card_reviews_round4.jsonl", round4)
    write_csv(OUT_DIR / "ai_card_reviews_round4.csv", round4)
    write_json(OUT_DIR / "ai_card_reviews_summary.json", summary)
    write_markdown(summary, round4)
    write_understanding_map(round4)
    write_author_watchlist(round4)

    print(f"reviewed={len(round4)}")
    print(f"needs_author_review={summary['needs_author_review_count']}")
    print(f"outputs={OUT_DIR}")


if __name__ == "__main__":
    main()
