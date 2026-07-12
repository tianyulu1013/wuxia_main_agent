from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CARDS_PATH = ROOT / "data" / "cards_current" / "all_cards.jsonl"
NOTES_PATH = ROOT / "data" / "review" / "card_understanding_notes.json"


CATEGORY_LABELS = {
    "combat_characters": "战斗人物",
    "attached_characters": "附加人物",
    "items": "物品",
    "scenes": "场景",
    "titles": "称号",
    "deprecated": "废弃记录",
}


KEYWORD_RULES = [
    ("抢先结算", "涉及抢先结算，必须和抢先攻击区分；它会影响对方响应、复活和整轮内容是否能结算。"),
    ("抢先攻击", "涉及抢先攻击，注意它通常仍会计算对方防御、不中、响应等内容。"),
    ("一定造成", "涉及一定造成，常用于穿透常规防御，需检查与转移、替伤、破、不中的关系。"),
    ("破", "涉及破，可能穿透或破坏部分防御结构，实战效果可能高于数字。"),
    ("杀死", "涉及杀死，需区分扣血、伤害、死亡、离场、清除。"),
    ("死亡", "涉及死亡或死后效果，需确认是否触发复活、离场、遗留效果。"),
    ("重生", "涉及重生/复活，需确认次数、生命状态、是否会被抢先结算压制。"),
    ("复活", "涉及重生/复活，需确认次数、生命状态、是否会被抢先结算压制。"),
    ("禁制", "涉及禁制，通常能处理奇怪能力，但需要确认禁制对象和持续时间。"),
    ("无效", "涉及无效/失灵，需确认作用范围是特技、攻击、物品、身份还是特定类型。"),
    ("失灵", "涉及无效/失灵，需确认作用范围是特技、攻击、物品、身份还是特定类型。"),
    ("不响应", "涉及不响应，需确认不能响应的是攻击、特技、物品还是整段结算。"),
    ("结盟", "涉及结盟或阵营关系，实战价值会受到多人桌面政治影响。"),
    ("离场", "涉及离场，必须和死亡、不在场、破空、清除区分。"),
    ("清除", "涉及清除，通常针对卡或对象本身，不能自动等同于死亡。"),
    ("流失", "涉及生命流失；生命流失不是攻击或伤害。"),
    ("毒", "涉及毒类状态，需确认是否累叠、是否可解除、是否属于异常。"),
    ("冰", "涉及冰/异常状态，需确认持续时间和解除方式。"),
    ("狂", "涉及狂/异常状态，需确认持续时间和行动影响。"),
    ("迟", "涉及迟/异常状态，需确认持续时间和行动影响。"),
    ("全", "涉及全体或波及类效果，需确认是否能指定人物单元以及对多人一卡的命中方式。"),
    ("波及", "涉及波及，需确认来源、目标、是否能被不中/削减/转移。"),
    ("偷", "涉及偷取/拿走，需确认目标物是否实际存在、是否可被转移。"),
    ("拿走", "涉及偷取/拿走，需确认目标物是否实际存在、是否可被转移。"),
    ("学会", "涉及学会/复制，需区分普通学会与完美学会。"),
    ("复制", "涉及学会/复制，需区分普通复制与完美复制。"),
    ("累积", "涉及累积，需确认是单局累积还是跨局长期记录。"),
]


def load_cards() -> list[dict[str, object]]:
    cards: list[dict[str, object]] = []
    for line in CARDS_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            cards.append(json.loads(line))
    return cards


def load_notes() -> dict[str, object]:
    if NOTES_PATH.exists():
        return json.loads(NOTES_PATH.read_text(encoding="utf-8"))
    return {
        "_schema": {
            "version": 1,
            "purpose": "卡牌理解笔记层：记录经作者校准或待作者校准的卡牌理解，用于评卡和改卡参考。不得反向污染源数据库、Excel 或牌面事实。",
        },
        "notes": {},
    }


def card_snapshot(card: dict[str, object]) -> dict[str, object]:
    fields = card.get("fields") if isinstance(card.get("fields"), dict) else {}
    source = card.get("source") if isinstance(card.get("source"), dict) else {}
    return {
        "category": card.get("category"),
        "life": str(fields.get("life")) if fields.get("life") is not None else None,
        "identity": fields.get("identity") or fields.get("traits"),
        "traits": fields.get("traits"),
        "item_category": fields.get("item_category"),
        "source_work": fields.get("source_work"),
        "author_group": fields.get("author_group"),
        "weapons": fields.get("weapons"),
        "relationships": fields.get("relationships"),
        "description": fields.get("description"),
        "source_sheet": source.get("sheet"),
        "source_row": source.get("row"),
    }


def ability_summary(card: dict[str, object]) -> tuple[list[str], list[str]]:
    abilities = card.get("abilities") if isinstance(card.get("abilities"), list) else []
    kinds: dict[str, int] = {}
    exclusive = 0
    identity = 0
    for ability in abilities:
        if not isinstance(ability, dict):
            continue
        kind = str(ability.get("kind") or "未标")
        kinds[kind] = kinds.get(kind, 0) + 1
        if ability.get("is_exclusive"):
            exclusive += 1
        if ability.get("is_identity"):
            identity += 1
    lines = []
    if kinds:
        lines.append("特技结构：" + "，".join(f"{k}×{v}" for k, v in sorted(kinds.items())))
    if exclusive:
        lines.append(f"检测到专属特技 {exclusive} 条。")
    if identity:
        lines.append(f"检测到身份特技 {identity} 条。")
    names = [str(a.get("name") or "") for a in abilities if isinstance(a, dict) and a.get("name")]
    return lines, names[:8]


def keyword_notes(text: str) -> list[str]:
    notes = []
    seen = set()
    for keyword, note in KEYWORD_RULES:
        if keyword in text and note not in seen:
            notes.append(note)
            seen.add(note)
        if len(notes) >= 8:
            break
    return notes


def category_position(category: str, title: str) -> list[str]:
    label = CATEGORY_LABELS.get(category, category or "未知类别")
    if category == "combat_characters":
        return [f"{title} 是战斗人物；低置信初评只按牌面机制摘要，不代表作者强度结论。"]
    if category == "attached_characters":
        return [f"{title} 是附加人物；需要区分“经常产生影响”和“稳定好用”。"]
    if category == "items":
        return [f"{title} 是物品；价值通常取决于开局/使用窗口、持有关系、是否可转移或被清除。"]
    if category == "scenes":
        return [f"{title} 是场景；影响往往是全局规则、身份信息或地点结构。"]
    if category == "titles":
        return [f"{title} 是称号；需关注附加对象、失去条件、最终名次或身份变化。"]
    if category == "deprecated":
        return [f"{title} 是废弃记录；默认不作为当前游玩评价对象，只用于历史参考。"]
    return [f"{title} 属于{label}；当前仅有低置信自动摘要。"]


def generic_value(category: str, text_notes: list[str]) -> list[str]:
    if category == "deprecated":
        return ["废弃记录不参与当前常规强度评价，除非作者特别要求回看旧版设计。"]
    if category == "scenes":
        return ["场景的实际价值取决于本局是否进入该场景，以及场上哪些人物能利用或规避场景规则。"]
    if category == "items":
        return ["物品强度取决于使用时机、目标限制、是否会被抢走/清除，以及是否与特定人物联动。"]
    if category == "titles":
        return ["称号强度取决于附加对象、是否可失去、是否改变身份/名次/阵营，以及是否被针对。"]
    if category == "attached_characters":
        return ["附加人物要同时看收益和负担；弃不掉、强制出战、改变阵营或干扰队友时，可能是搅局卡而非纯增益。"]
    if text_notes:
        return ["实战价值需要围绕上述关键词裁定展开；当前只是基于牌面关键词的低置信提醒。"]
    return ["牌面没有被自动规则捕捉到特别高风险关键词；仍需作者或玩家根据实际对局补充强度和用法。"]


def needs_review(category: str, text_notes: list[str]) -> list[str]:
    questions = ["这张卡尚未作者单卡校准；强度、泛用性、常见用法和艺术形象贴合度都需要人工确认。"]
    if category in {"combat_characters", "attached_characters"}:
        questions.append("需要确认这张卡是主战、辅助、搅局、肉盾、爆发、控制、保护、资源或特殊胜负类中的哪几类。")
    if category in {"items", "titles", "scenes"}:
        questions.append("需要确认它在多数局面中是稳定收益、条件收益、搅局风险，还是主要为了特殊剧情/机制存在。")
    if text_notes:
        questions.append("自动检测到的关键词只提示风险方向；具体结算边界仍以作者裁定为准。")
    return questions


def build_note(card: dict[str, object]) -> dict[str, object]:
    title = str(card.get("title") or "")
    category = str(card.get("category") or "")
    fields = card.get("fields") if isinstance(card.get("fields"), dict) else {}
    all_text = str(card.get("all_text") or "")
    ability_lines, ability_names = ability_summary(card)
    kw_notes = keyword_notes(all_text)
    source_work = fields.get("source_work") or "未标出处"
    author_group = fields.get("author_group") or "未标作者"
    core = category_position(category, title)
    if ability_lines:
        core.extend(ability_lines)
    if ability_names:
        core.append("主要特技名示例：" + "、".join(ability_names))
    return {
        "status": "ai_draft",
        "sample_set": "full_library_light_ai_draft_2026_07_12",
        "current_snapshot": card_snapshot(card),
        "source_research": [
            f"未做外部资料核验；只记录数据库牌面、出处《{source_work}》和作者组“{author_group}”带来的低置信初步理解。",
            "艺术形象符合度需要作者或熟悉原作的玩家校准。",
        ],
        "author_rulings": [],
        "core_positioning": core,
        "key_mechanics": kw_notes or ["当前仅有自动薄摘要；尚未提炼出稳定的关键机制结论。"],
        "practical_value": generic_value(category, kw_notes),
        "strategy_notes": [
            "低置信建议：先按牌面关键词找它解决的问题，再看它是否依赖特定队友、敌人、场景或开局信息。",
            "若玩家有实际对局体感，应优先补充常见用法、弱点、克星和容易误用之处。",
        ],
        "face_value_vs_play_value": {
            "face_value": "这是自动生成的牌面层初读，只反映文本表面信号。",
            "play_value": "真实游玩价值需要结合随机抓牌、阵容、多人谈判、隐藏信息和作者裁定。",
            "calibration_lesson": "未校准卡不能作为高权重强度样本，只能作为讨论入口。",
        },
        "flavor_alignment": [
            "未联网核验人物/物品/场景来源形象。",
            "如果这张卡来自小说、游戏或内部朋友形象，需要补充其核心艺术特征后再评价贴合度。",
        ],
        "rules_risks": kw_notes or ["暂无自动识别出的高风险术语；不代表规则完全清晰。"],
        "ai_misread_risks": [
            "AI 草稿可能过度依赖关键词，不理解真实结算结构。",
            "不要把本条低置信内容写回源数据库，也不要当作作者强度定论。",
        ],
        "reference_lessons": [
            "这是一条全库覆盖用的低置信草稿；作者或玩家校准后才能升级为 author_reviewed。",
        ],
        "needs_author_review": needs_review(category, kw_notes),
        "generality": {
            "level": "待校准",
            "notes": [
                "当前没有作者单卡校准，不能给出稳定泛用性判断。",
                "可由玩家补充：多数局面是否好用、依赖哪些队友/敌人、是否容易被克制。",
            ],
        },
    }


def main() -> None:
    root = load_notes()
    notes = root.setdefault("notes", {})
    cards = load_cards()
    created = 0
    preserved = 0
    for card in cards:
        title = str(card.get("title") or "")
        if not title:
            continue
        if title in notes and isinstance(notes[title], dict):
            preserved += 1
            continue
        notes[title] = build_note(card)
        created += 1
    root["_schema"]["generated_light_drafts"] = {
        "batch": "full_library_light_ai_draft_2026_07_12",
        "created": created,
        "preserved_existing": preserved,
        "warning": "These notes are low-confidence AI discussion starters and must not be treated as source card facts.",
    }
    NOTES_PATH.write_text(json.dumps(root, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"created={created}")
    print(f"preserved={preserved}")
    print(f"total_notes={len(notes)}")


if __name__ == "__main__":
    main()
