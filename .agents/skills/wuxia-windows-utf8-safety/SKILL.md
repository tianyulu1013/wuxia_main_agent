---
name: wuxia-windows-utf8-safety
description: UTF-8 and Chinese-text safety rules for the 五行卡牌 project on this Windows/PowerShell machine. Use whenever Codex reads, writes, patches, validates, or generates Chinese content, JSON, Markdown, rule notes, card notes, skills, scripts, or project documents through PowerShell, Python, shell commands, or pipelines; especially before editing data/review/*.json, docs/*.md, .agents/skills/*, or any Chinese filename/content.
---

# 五行卡牌 Windows 中文编码安全

## Core Rule

Assume this Windows PowerShell environment can corrupt Chinese text when Chinese content is passed through command text, pipelines, here-strings, or default PowerShell file-writing cmdlets.

Never risk source data, review JSON, Markdown notes, skills, or rule documents by casually piping Chinese through PowerShell.

## Do Not Do

- Do not send Chinese-heavy Python code through `@' ... '@ | python -`.
- Do not use shell heredocs or here-strings for Chinese JSON/Markdown/file content.
- Do not use `Set-Content`, `Out-File`, `Add-Content`, or redirection (`>`, `>>`) for Chinese project files unless encoding is explicitly controlled and then verified.
- Do not trust `Get-Content` terminal output for Chinese correctness; PowerShell may display mojibake even when the file is valid.
- Do not run bulk JSON edits if the command string itself contains large Chinese literals.
- Do not continue after seeing `question-mark placeholder` or mojibake in generated JSON. Stop and inspect with Python.

## Safe Patterns

Prefer these patterns, in order:

1. Use `apply_patch` for manual edits to Markdown, skills, and small text files.
2. For structured JSON changes with many Chinese strings, create a temporary `.py` file with `apply_patch`, run it with the bundled Python, then delete the temporary file with `apply_patch`.
3. For inspection, use Python with `encoding="utf-8"` and print only small targeted snippets.
4. For validation, use `python -m json.tool <file>` and then targeted Python checks for keys/values.
5. When using `python -c`, keep the command mostly ASCII and avoid embedding Chinese literals.

Bundled Python path normally used in this project:

```powershell
& "C:\Users\biaaa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" ...
```

When terminal output looks garbled, verify with Python rather than assuming the file is broken:

```powershell
$env:PYTHONIOENCODING='utf-8'; & "C:\Users\biaaa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -c "from pathlib import Path; s=Path('path/to/file.md').read_text(encoding='utf-8'); print(s.splitlines()[0]); print('question-mark placeholder' in s)"
```

## Required Verification After Chinese Writes

After writing any Chinese JSON or Markdown file:

- For JSON: run `python -m json.tool <file>`.
- For important review data: print the exact updated key names and 1-2 representative values using Python.
- For Markdown: read the file with Python `encoding="utf-8"` and check the title/header plus whether `question-mark placeholder` appears.
- If `question-mark placeholder` appears in a data file, fix it immediately before continuing.

## Project-Specific Guardrails

- Never let encoding accidents pollute `data/cards.sqlite`, `data/cards_current/*.jsonl`, `data/review/*.json`, `data/review/card_notes/*.md`, or `.agents/skills/*`.
- If a temporary script is needed, name it clearly, run it once, validate outputs, then remove it.
- If PowerShell output displays mojibake but Python checks show correct text, mention that it is display encoding only and proceed.
- If data was corrupted, restore or surgically repair the affected key/value immediately; do not leave placeholder keys such as `question-mark placeholder`.
