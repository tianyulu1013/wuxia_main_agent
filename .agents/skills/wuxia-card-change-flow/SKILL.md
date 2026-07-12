---
name: wuxia-card-change-flow
description: Use when the user wants to create a new 五行卡牌 card, modify an existing card, evaluate a proposed card change, turn natural-language card design intent into candidate card text, record a change candidate, or discuss whether a change should become PSD/Excel/database work. This skill enforces the candidate-layer workflow: AI may warn or oppose, but must still generate editable candidate text and must not modify source card data before author confirmation.
---

# 五行卡牌改卡候选流程

Use this skill for new-card and card-revision work. The objective is not to make AI the final judge; the objective is to help the author produce reviewable card text and track it safely.

## Required References

Read these before doing substantive work:

- `PROJECT_STATE.md`
- `docs/source-of-truth-policy.md`
- `docs/change-candidate-framework.md`
- `docs/skills/wuxia-card-review.md`
- `docs/skills/wuxia-data-query.md`
- `docs/rule-terms-understanding.md`

If the request touches rules terms or unclear mechanics, also read:

- `docs/skills/wuxia-rulebook-work.md`
- `data/review/rule_terms.json`

## Non-Negotiable Rules

- Treat the user as the sole author and final authority.
- Do not modify source database, Excel, PSD, or current card facts unless the user explicitly confirms the candidate and asks to apply it.
- Store unconfirmed ideas only in `data/change_candidates.json`.
- Keep AI comments, strength estimates, strategy, and electronic-game assumptions out of source data.
- If the AI position is `caution` or `oppose`, still generate an editable candidate text that follows the author intent.
- Ask questions only when the missing answer is necessary to produce a coherent candidate; otherwise make a clearly labeled tentative draft.

## Standard Workflow

1. Classify the request as `new_card`, `revision`, `rules_text`, or `other`.
2. For an existing card, query current data first:
   - Prefer `data/cards.sqlite` or `scripts/query_cards.py`.
   - Check card image only when text or layout uncertainty matters.
3. Restate the author intent in one sentence.
4. Give a short review:
   - artistic/flavor fit
   - strength impact
   - rules stability
   - text clarity
   - electronic-game risk if relevant
   For flavor fit, do not guess from the card text alone. For public literary/film/game characters, use source knowledge or perform a focused lookup when needed; for internal friends/private characters, ask the author.
5. Set `ai_position`: `support`, `caution`, `oppose`, or `uncertain`.
6. Produce candidate text:
   - full card text for new cards or large rewrites
   - local patch text for small changes
7. Produce player-facing patch notes.
8. List author decisions needed.
9. If the user asks to record it, write a candidate with `scripts/add_change_candidate.py`; otherwise leave it in the conversation only.

## Output Shape

Prefer this structure:

```text
当前理解：...

简评：
- 形象：...
- 强度：...
- 规则稳定：...
- 文本清晰：...

AI 态度：caution

候选文本：
...

更新说明草稿：
- ...

待你裁定：
- ...
```

## Recording Candidates

Use the bundled project script, not ad hoc JSON editing:

```powershell
python scripts/add_change_candidate.py "<卡名>" "<作者请求>" --candidate-type revision --ai-position caution --full-text "<候选文本>"
```

In this environment, `python` may not be on PATH. Use the bundled runtime when needed:

```powershell
& "C:\Users\biaaa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts/add_change_candidate.py ...
```

Useful options:

- `--dry-run`: print JSON without writing.
- `--design-goal`: record the design objective.
- `--current-snapshot`: record current-card context.
- `--patch`: record one local change.
- `--patch-note`: record player-facing update notes.
- `--risk`: record rules or balance risks.
- `--question`: record author decisions needed.

## Confirmed Application

Only after author confirmation should the work move to:

1. PSD edit by author.
2. Excel update.
3. Database rebuild.
4. Player update notes.
5. Release card image update.

Do not skip directly from a candidate to source-data mutation.
