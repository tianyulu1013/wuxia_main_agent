---
name: wuxia-card-change-flow
description: Use when the user wants to create, revise, discuss, approve, apply, resume, or finish a 五行卡牌 change; start directly from an existing card-change TODO; generate copy-paste card text; reconcile an author-edited card face back into Excel/SQLite/JSONL; remove a completed TODO; or produce a full-database Excel and player update log. This skill enforces the author-card-face workflow: candidates are discussion aids, while the author's actual final card text is authoritative.
---

# 五行卡牌改卡闭环流程

Use this skill for both candidate discussion and confirmed application. Help the author discuss a change, receive exact copy-paste text, edit the physical card, then synchronize the actual final card text into every database deliverable.

## Required References

Read these before doing substantive work:

- `PROJECT_STATE.md`
- `docs/source-of-truth-policy.md`
- `docs/change-candidate-framework.md`
- `docs/skills/wuxia-data-query.md`
- `docs/ai-understanding/core/game-flow.md`
- `docs/ai-understanding/core/combat-baseline.md`
- 当前卡牌对应的`docs/ai-understanding/evaluation/card-types/`类别模块

战斗人物的改卡讨论还应根据主要功能读取`docs/ai-understanding/evaluation/functions/`中的相关模块。

If the request touches special terms or unclear mechanics, use the routing index instead of loading the whole rule corpus:

- `docs/skills/wuxia-rulebook-work.md`
- `docs/ai-understanding/rules/README.md`
- `data/review/rule_terms.json`中的实际相关词条

## Non-Negotiable Rules

- Treat the user as the sole author and final authority.
- Do not modify source database, Excel, PSD, or current card facts during discussion.
- Store unconfirmed ideas only in `data/change_candidates.json`.
- Keep AI comments, strength estimates, strategy, and electronic-game assumptions out of source data.
- If the AI position is `caution` or `oppose`, still generate an editable candidate text that follows the author intent.
- Ask questions only when the missing answer is necessary to produce a coherent candidate; otherwise make a clearly labeled tentative draft.
- A candidate/TODO is never the final source of truth. After the author edits the card face, use the author's actual final card text even when it differs from the candidate.
- Do not mark a candidate `applied`, remove it from the visible TODO, or rebuild source data merely because the author approved the idea. Wait until the author says the card face has actually been changed.
- The author may apply several cards over time as one update batch. Synchronize and verify each completed card immediately, but defer the full-database Excel and final update log until the author says the batch is finished.
- Never commit, push, publish, or update public versions unless the author separately requests it.

## Choose the Entry Point

Do not assume every task begins with design discussion. At the start, identify the user's current stage:

- **New discussion:** no existing candidate; begin at Phase 1.
- **Resume candidate review:** load the existing candidate/TODO and continue only the unresolved discussion.
- **Author is editing the card face:** load the candidate and provide its copy-paste text or layout notes; remain at Phase 2.
- **Author already changed the card face:** begin directly at Phase 3. Do not repeat the design review unless the author asks.
- **Source data already synchronized but TODO remains:** verify the actual final text and synchronization evidence, then continue at Phase 5.

For any resume path:

1. Locate the candidate by stable ID when supplied; otherwise match by card title.
2. If several active candidates match the same card and the intended one is not clear, ask which candidate was completed.
3. Load the current database text as well as the candidate snapshot. Do not assume the database still equals the snapshot if time has passed.
4. Continue from the earliest incomplete phase only. Do not force the author to repeat prior discussion or approval.

## Phase 1: Discussion and Candidate

1. Classify the request as `new_card`, `revision`, `rules_text`, or `other`.
2. For an existing card, query current data first:
   - Prefer `data/cards.sqlite` or `scripts/query_cards.py`.
   - Check card image only when text or layout uncertainty matters.
3. Capture the exact current field text before proposing changes. This is the pre-change snapshot used later for the real update log.
4. Restate the author intent in one sentence.
5. Give a short review:
   - artistic/flavor fit
   - strength impact
   - rules stability
   - text clarity
   - electronic-game risk if relevant
   For flavor fit, do not guess from the card text alone. For public literary/film/game characters, use source knowledge or perform a focused lookup when needed; for internal friends/private characters, ask the author.
6. Set `ai_position`: `support`, `caution`, `oppose`, or `uncertain`.
7. Produce candidate text:
   - full card text for new cards or large rewrites
   - local patch text for small changes
   - always include a clean `可直接复制粘贴` block containing the exact proposed replacement text
8. Produce player-facing patch notes based on the candidate.
9. List author decisions needed.
10. When the author wants the change kept for later card editing, write it to `data/change_candidates.json` and regenerate `改卡TODO.md` with `scripts/export_card_change_todos.py`.

The visible TODO must contain:

- card name and stable candidate ID
- current text or exact old fragment
- exact proposed replacement text
- a clean copy-paste block
- unresolved author decisions
- draft player update note

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

修改对照：
...

可直接复制粘贴：
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

## Phase 2: Author Approval and Card-Face Editing

After the author approves the direction:

- Keep the candidate visible with status `approved` until the physical card edit is finished.
- Give the author the exact copy-paste text and any PSD/layout notes.
- Do not update the source database yet.
- Wait for the author to report that the card face has been changed.

## Phase 3: Reconcile the Actual Card Face

When the author says the card face is changed:

1. Obtain the actual final text:
   - read the updated card image/PSD/export when available, or
   - use the exact final text supplied by the author.
2. Compare three versions:
   - old database text
   - candidate/TODO text
   - actual final card text
3. Treat the actual final card text as authoritative. Differences from the TODO are allowed and must not be silently overwritten by the candidate.
4. If the card image is unreadable or the final wording is ambiguous, ask the author for the exact text before changing source data.
5. Show or record the exact old-to-final difference. Generate the final player update note from this real difference, not from the earlier candidate.

## Phase 4: Apply and Verify

After the actual final text is known:

1. Update the current baseline Excel/source record with the actual final text.
2. Rebuild `data/cards.sqlite` and `data/cards_current/*.jsonl`.
3. Verify the affected fields in all three places:
   - baseline Excel
   - SQLite
   - JSONL
4. Compare content exactly, preserving punctuation and line breaks except documented newline normalization. Do not substitute the TODO wording.
5. Use an author override only for structural metadata the card text cannot express reliably; do not use an override to conceal a mismatch between the card face and source text.

## Phase 5: Close the Card Item or Deliver the Batch

Only after the source update and verification succeed:

1. Record the actual final text/diff, completion date, affected source row, and affected card pile/deck.
2. If the author says more cards will be changed in the same batch:
   - set the candidate to `source_applied`
   - attach a stable `batch_id`
   - regenerate `改卡TODO.md` so this finished card leaves the visible TODO
   - keep the final full-database Excel, update log, and pile summary deferred
3. When the author says the batch is finished:
   - collect every `source_applied` candidate in that batch
   - produce a full-database Excel containing every current card and all current fields
   - produce a player-facing update log from the actual old-to-final differences
   - summarize every affected card pile/deck and the cards changed within it
   - mark those candidates `applied`
4. The full-database export must come from the final verified database/current baseline, not from candidate text.
5. Return clickable paths for:
   - the full-database Excel
   - the update log
   - the regenerated TODO
6. State which cards and piles were applied and confirm that no candidate-only wording was substituted.

Default deliverables may be placed under a dated directory in `outputs/card-database-deliverables/`. Use the spreadsheet skill for the Excel artifact and verify the workbook before delivery. Produce the update log as Markdown unless the author requests another format.

## Completion Gate

Do not call the update batch complete unless all are true:

- the author has finished the card-face edit
- the actual final text was obtained
- Excel, SQLite, and JSONL match the actual final text
- every finished card is recorded under the batch and marked `applied`
- the visible TODO no longer contains the completed item
- the full-database Excel was generated and checked
- the actual-change update log was generated
- the affected card piles/decks were summarized
