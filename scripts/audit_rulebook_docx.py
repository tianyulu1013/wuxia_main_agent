from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from docx import Document


ROOT = Path(__file__).resolve().parents[1]
DOCX_PATH = ROOT / "五行卡牌规则.docx"
DATA_OUT = ROOT / "data" / "rulebook_docx_extract.json"
TEXT_OUT = ROOT / "docs" / "rulebook-docx-extract.md"
AUDIT_OUT = ROOT / "docs" / "rulebook-structure-audit.md"


CORE_TERMS = [
    "本局",
    "回合",
    "轮",
    "战斗",
    "作战",
    "攻击",
    "伤害",
    "生命流失",
    "流失",
    "杀死",
    "死亡",
    "离场",
    "退出",
    "清除",
    "在场",
    "不在场",
    "找不到",
    "无此人",
    "响应",
    "不响应",
    "不利",
    "有利",
    "效果",
    "特技",
    "对阵",
    "非对阵",
    "正面",
    "侧面",
    "波及",
    "场景",
    "地点",
    "玩家",
    "一方",
    "阵营",
    "结盟",
    "弃牌堆",
    "本局弃卡",
    "人物单元",
    "多人一卡",
    "共享生命",
    "无生命",
    "称号",
    "场景卡",
]


def paragraph_level(style_name: str) -> int | None:
    if style_name == "Title":
        return 0
    if style_name.startswith("Heading "):
        try:
            return int(style_name.removeprefix("Heading "))
        except ValueError:
            return None
    return None


def extract_docx() -> dict[str, object]:
    doc = Document(DOCX_PATH)
    paragraphs: list[dict[str, object]] = []
    body_started = False
    for index, paragraph in enumerate(doc.paragraphs, 1):
        text = paragraph.text.strip()
        if not text:
            continue
        style = paragraph.style.name
        if style.startswith("toc"):
            continue
        if text == "游戏流程" and style == "Heading 1":
            body_started = True
        if not body_started and style not in {"Title", "Subtitle"}:
            continue
        paragraphs.append(
            {
                "paragraph": index,
                "style": style,
                "level": paragraph_level(style),
                "text": text,
            }
        )
    return {"source": str(DOCX_PATH.name), "paragraphs": paragraphs}


def heading_lines(paragraphs: list[dict[str, object]]) -> list[str]:
    lines = []
    for item in paragraphs:
        level = item.get("level")
        if isinstance(level, int) and level >= 1:
            indent = "  " * (level - 1)
            lines.append(f"{indent}- P{item['paragraph']}: {item['text']}")
    return lines


def write_extract(data: dict[str, object]) -> None:
    paragraphs = data["paragraphs"]
    lines = [
        "# 规则书 DOCX 正文抽取",
        "",
        f"- 来源：`{data['source']}`",
        "- 说明：跳过了 Word 自动目录段落，保留正文段落编号、样式和文本。",
        "",
    ]
    current = []
    for item in paragraphs:
        level = item.get("level")
        text = str(item["text"])
        if isinstance(level, int) and level >= 1:
            hashes = "#" * min(level + 1, 6)
            lines.append(f"{hashes} P{item['paragraph']} {text}")
        elif item["style"] in {"Title", "Subtitle"}:
            lines.append(f"> P{item['paragraph']} [{item['style']}] {text}")
        else:
            lines.append(f"- P{item['paragraph']}: {text}")
        current.append(text)
    TEXT_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def numbered_heading_issues(paragraphs: list[dict[str, object]]) -> list[str]:
    issues = []
    current_h1 = ""
    h2_numbers: list[tuple[str, str, object, str]] = []
    for item in paragraphs:
        if item.get("style") == "Heading 1":
            current_h1 = str(item["text"])
        if item.get("style") == "Heading 2":
            text = str(item["text"])
            if text[:1] in "一二三四五六七八九十":
                h2_numbers.append((current_h1, text[:1], item["paragraph"], text))
    counts = Counter((parent, number) for parent, number, _, _ in h2_numbers)
    for (parent, number), count in counts.items():
        if count > 1:
            refs = "；".join(
                f"P{p} {text}"
                for item_parent, item_number, p, text in h2_numbers
                if item_parent == parent and item_number == number
            )
            issues.append(f"- `{parent}` 下二级标题编号 `{number}` 重复：{refs}")
    return issues


def term_frequency(paragraphs: list[dict[str, object]]) -> dict[str, int]:
    text = "\n".join(str(item["text"]) for item in paragraphs)
    return {term: text.count(term) for term in CORE_TERMS}


def write_audit(data: dict[str, object]) -> None:
    paragraphs: list[dict[str, object]] = data["paragraphs"]  # type: ignore[assignment]
    freq = term_frequency(paragraphs)
    headings = heading_lines(paragraphs)
    missing = [term for term, count in freq.items() if count == 0]
    sparse = [term for term, count in freq.items() if 0 < count <= 2]
    numbering = numbered_heading_issues(paragraphs)

    lines = [
        "# 规则书结构审计报告 v0.1",
        "",
        f"- 来源：`{data['source']}`",
        "- 范围：只审计 DOCX 正文，不处理 PDF。",
        "- 目的：发现结构、术语、流程和定义缺口；不直接重写规则。",
        "",
        "## 总体判断",
        "",
        "当前规则书已经覆盖了大量真实规则，尤其是战斗流程、特技结算、不利/有利、攻击/防御、在场/不在场等核心概念。",
        "",
        "主要问题不是内容少，而是：",
        "",
        "- 定义层和流程层混在一起。",
        "- 一些实际游戏中关键的术语没有进入规则书正文。",
        "- 部分术语已经有描述，但没有形成可引用的规范定义。",
        "- 标题编号和层级存在轻微混乱。",
        "- 特殊卡牌例外很多，但缺少“例外如何进入裁定集”的固定位置。",
        "",
        "## 当前章节树",
        "",
        *headings,
        "",
        "## 结构问题",
        "",
    ]
    if numbering:
        lines.extend(numbering)
    else:
        lines.append("- 未发现明显标题编号重复。")
    lines.extend(
        [
            "- `游戏流程` 中先讲摸牌/选卡/选敌/战斗，但牌堆、弃牌堆、本局弃卡堆没有独立章节，导致实际开局流程缺少完整闭环。",
            "- `战斗` 章节很细，但“作战/战斗/回合/轮”没有先作为术语统一定义，读者需要在后文推断。",
            "- `其他术语` 承载了过多基础规则，应拆成：术语表、状态与效果、目标与相关、空间与在场、胜负与名次。",
            "- `特技的结算` 写了优先级，但缺少统一的“事件/来源/对象/响应窗口/结算队列”框架。",
            "- `FAQ` 目前没有正文内容或结构，适合承接作者裁定、特殊例外和复杂卡牌案例。",
            "",
            "## 术语覆盖检查",
            "",
            "### 未出现但实际系统需要的术语",
            "",
        ]
    )
    if missing:
        lines.extend(f"- `{term}`" for term in missing)
    else:
        lines.append("- 无。")
    lines.extend(
        [
            "",
            "### 出现次数很少、建议补定义或交叉引用的术语",
            "",
        ]
    )
    lines.extend(f"- `{term}`：{freq[term]} 次" for term in sparse)
    lines.extend(
        [
            "",
            "### 高频但需要规范化的术语",
            "",
            "- `特技`：出现很多，但主动、被动、可控、身份特技、专属特技、学习/复制/屏蔽之间的边界需要独立小节。",
            "- `战斗` / `作战`：两词都大量使用，需要明确是否同义，还是“作战”是触发战斗的一类事件。",
            "- `效果` / `特技`：已有说明，但建议拆出“特技是来源，效果是结果”的定义模型，避免“效果是否可响应/可不中”的混乱。",
            "- `攻击` / `伤害` / `生命流失`：已有内容，但建议在术语表中先给一行硬定义，再在战斗章展开。",
            "- `在场` / `不在场` / `离场` / `无此人` / `找不到`：已有内容，但这是空间系统核心，应独立成章。",
            "",
            "## 重点缺口",
            "",
            "### 1. 牌堆与弃牌区",
            "",
            "当前规则书正文没有 `弃牌堆` 和 `本局弃卡`。但实际规则中存在抽牌堆、弃牌堆、本局弃卡堆，而且某些特技会和本局弃卡交互。",
            "",
            "建议新增小节：",
            "",
            "- 抽牌堆",
            "- 弃牌堆",
            "- 本局弃卡堆",
            "- 随机弃掉和自己弃掉的去向差异",
            "- 本局结束或结算后本局弃卡进入弃牌堆的时机",
            "",
            "### 2. 回合与轮",
            "",
            "`回合` 出现较多，但 `轮` 只出现 1 次。实际规则中二者差异非常重要，例如“马钰下轮后归还”。",
            "",
            "建议新增硬定义：",
            "",
            "- 回合：某人物自己出战并完成一次战斗流程。",
            "- 轮：己方任一人物出战一回合后，己方相关人物经过一轮。",
            "",
            "以上定义需由作者确认后写入规则书。",
            "",
            "### 3. 人物、人物单元、卡",
            "",
            "规则书目前有战斗人物和其他卡的关系，但没有把 `卡`、`人物`、`人物单元` 拆开。",
            "",
            "这会影响：",
            "",
            "- 多人一卡",
            "- 共享生命",
            "- 清除卡 vs 杀死人物",
            "- 附加人物/物品/称号随卡清除时的处理",
            "- 五个人头这种计人数特殊卡",
            "",
            "建议新增小节：`物理卡、人物、人物单元`。",
            "",
            "### 4. 生命系统",
            "",
            "规则书有攻击、伤害、防御、生命不能低于某值等内容，但缺少生命系统总览。",
            "",
            "建议明确：",
            "",
            "- 有生命人物",
            "- 无生命属性人物",
            "- 多生命阶段",
            "- 共享生命池",
            "- 生命到 0 是否死亡",
            "- 杀死是否绕过生命",
            "- 生命流失与伤害的差异",
            "",
            "### 5. 场景与地点",
            "",
            "规则书已有“战斗所处的位置场景”，但没有先定义场景、当前场、地点、不在场地点、独立空间。",
            "",
            "建议新增：`空间与场景`，再把现有 P131-P144 纳入其中。",
            "",
            "### 6. 人工裁定与破坏规则层",
            "",
            "规则书没有明确说明删字、只剩某行文字、重新解释牌面这类规则应如何裁定。",
            "",
            "建议新增：",
            "",
            "- 文本修改类效果",
            "- 人工裁定优先级",
            "- 无法程序化/无法穷举时的处理",
            "- 裁定记录进入 FAQ/裁定集",
            "",
            "## 建议新版规则书骨架",
            "",
            "1. 游戏组件与核心对象",
            "2. 开局与选卡流程",
            "3. 牌堆、弃牌堆、本局弃卡",
            "4. 人物、人物单元、生命与离场",
            "5. 场景、地点、在场与不在场",
            "6. 战斗流程",
            "7. 五行卡、放卡、平克与动卡",
            "8. 攻击、伤害、生命流失、防御",
            "9. 特技类型、使用时机、对象与结算",
            "10. 状态：异常、非异常、有利、不利",
            "11. 玩家、一方、阵营、结盟",
            "12. 胜负、失败、并列名次",
            "13. 特殊文本规则与人工裁定",
            "14. FAQ/裁定集",
            "",
            "## 第一批需要问作者的问题",
            "",
            "1. `战斗` 和 `作战` 是否应视为同义？还是作战是“发起一场战斗”的上层事件？",
            "2. `回合` 和 `轮` 的定义是否按我们此前讨论写入规则书？",
            "3. `离场` 是否应拆成若干类型：暂时离场、退出本局、破空、清除？",
            "4. `无此人` 与 `找不到` 是否都应保留为独立状态，而不是并入不在场？",
            "5. `本局弃卡堆` 的结算时点是否固定为“本局相关结算完成后进入弃牌堆”？",
            "6. `人物单元` 这个术语是否可以正式写进规则书？",
            "7. `生命流失` 是否统一写作“生命流失”，并把“体力流失/生命流逝”作为旧称？",
            "8. `普通方式：正面按照回合之和，侧面按照单次计算` 这句需要补上下文，它具体指攻击次数、伤害上限，还是效果累计？",
            "",
            "## 下一步建议",
            "",
            "先不要直接重写整本规则书。",
            "",
            "建议下一步只做一件事：建立 `规则术语表 v0.1`，每个术语只写一到三句硬定义，并标记是否已经作者确认。",
        ]
    )
    AUDIT_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    data = extract_docx()
    DATA_OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_extract(data)
    write_audit(data)
    print(DATA_OUT)
    print(TEXT_OUT)
    print(AUDIT_OUT)


if __name__ == "__main__":
    main()
