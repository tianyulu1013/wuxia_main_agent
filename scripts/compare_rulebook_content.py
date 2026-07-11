import re
from pathlib import Path

def clean_text(text):
    # 去除标点符号、空格和非中文字符，仅保留核心字句以便进行包含度比对
    return "".join(re.findall(r"[\u4e00-\u9fa5\d]+", text))

def calculate_coverage(orig_clean, ref_clean):
    if not orig_clean or not ref_clean:
        return 0.0
    set_orig = set(orig_clean)
    set_ref = set(ref_clean)
    intersection = set_orig.intersection(set_ref)
    # 计算原始段落中的字在新版某行中被包含的比例 (Coverage)
    return len(intersection) / len(set_orig)

def audit_rulebooks():
    extract_path = Path("docs/rulebook-docx-extract.md")
    refactored_path = Path("docs/rulebook-refactored.md")
    report_path = Path("reports/3-rulebook-discrepancy-report.md")
    
    if not extract_path.exists() or not refactored_path.exists():
        print("Error: Source files missing.")
        return
        
    extract_content = extract_path.read_text(encoding="utf-8")
    refactored_content = refactored_path.read_text(encoding="utf-8")
    
    # 1. 提取原版所有段落 Pxx
    original_rules = []
    pattern = re.compile(r"(?:-|>)\s*P(\d+)(?:[^:\n]*:)?\s*(.*)")
    
    for line in extract_content.splitlines():
        match = pattern.search(line)
        if match:
            p_num = int(match.group(1))
            text = match.group(2).strip()
            if text:
                original_rules.append((p_num, text))
                
    # 2. 提取新版所有正文行
    refactored_lines = [line.strip() for line in refactored_content.splitlines() if line.strip()]
    
    missing_rules = []
    low_sim_rules = []
    
    # 3. 开始包含度比对
    for p_num, orig_text in original_rules:
        orig_clean = clean_text(orig_text)
        if not orig_clean or len(orig_clean) < 2: # 忽略极短的无意义符号
            continue
            
        best_cov = 0.0
        best_match_line = ""
        
        for ref_line in refactored_lines:
            ref_clean = clean_text(ref_line)
            cov = calculate_coverage(orig_clean, ref_clean)
            if cov > best_cov:
                best_cov = cov
                best_match_line = ref_line
                
        # 判定门槛：如果包含度低于 0.65，判定为未被包含（缺失）
        if best_cov < 0.65:
            missing_rules.append((p_num, orig_text))
        elif best_cov < 0.85:
            low_sim_rules.append((p_num, orig_text, best_match_line, best_cov))
            
    # 4. 强校验：结算顺序优先级链 (P247 - P261) 强校验结果
    priority_keys = [
        (247, "特殊声明"),
        (248, "场景vs无视场景"),
        (249, "无法响应"),
        (250, "身份描述"),
        (251, "看不见"),
        (252, "破防"),
        (253, "反弹效果"),
        (254, "失灵"),
        (255, "不敢用"),
        (256, "禁制"),
        (257, "使无效"),
        (258, "抹去"),
        (259, "正常的特技"),
        (260, "习得"),
        (261, "同一级")
    ]
    
    # 截取第九章 9.2 结算优先级段落以内的行
    lines_in_chapter_9_2 = []
    in_chapter = False
    for line in refactored_content.splitlines():
        line_str = line.strip()
        if "#### 9.2" in line_str:
            in_chapter = True
        if in_chapter:
            if "#### 9.3" in line_str or "## 第四部分" in line_str:
                break
            if line_str:
                lines_in_chapter_9_2.append(line_str)
                
    priority_discrepancies = []
    found_positions = []
    for p_num, key in priority_keys:
        clean_key = clean_text(key)
        found_line_idx = -1
        for idx, ref_line in enumerate(lines_in_chapter_9_2):
            if clean_key in clean_text(ref_line):
                found_line_idx = idx
                break
        found_positions.append((p_num, key, found_line_idx))
        
    last_idx = -1
    for p_num, key, idx in found_positions:
        if idx == -1:
            priority_discrepancies.append(f"错误: 结算规则 P{p_num} ('{key}') 在第九章 9.2 结算优先级正文中完全未找到！")
        else:
            if idx < last_idx:
                priority_discrepancies.append(f"错误: 结算规则 P{p_num} ('{key}') 的相对顺序发生了错位（颠倒）！当前索引 {idx}，上一个索引 {last_idx}")
            last_idx = idx

    # 5. 撰写差异审计报告
    report_lines = []
    report_lines.append("# 五行卡牌新旧规则书自动化比对审计报告\n")
    report_lines.append(f"- **审计源数据 A**: [rulebook-docx-extract.md](file:///{extract_path.absolute().as_posix()})")
    report_lines.append(f"- **审计目标 B**: [rulebook-refactored.md](file:///{refactored_path.absolute().as_posix()})\n")
    
    report_lines.append("## 1. 核心优先级结算链 (P247 - P261) 强校验结果\n")
    if not priority_discrepancies:
        report_lines.append("[OK] 合格: 优先级结算链的全部条款顺序在新版规则书重构版中完全一致，没有缺失与错位。\n")
    else:
        report_lines.append("[FAIL] 不合格 (发现严重偏差):\n")
        for err in priority_discrepancies:
            report_lines.append(f"- {err}")
        report_lines.append("\n")
        
    report_lines.append("## 2. 完全缺失的原始规则条目\n")
    if not missing_rules:
        report_lines.append("[OK] 合格: 没有检测到缺失条目。\n")
    else:
        report_lines.append(f"共发现 **{len(missing_rules)}** 条可能缺失的原始规则：\n")
        for p_num, text in missing_rules:
            report_lines.append(f"- **P{p_num}**: {text}")
        report_lines.append("\n")
        
    report_lines.append("## 3. 疑似内容篡改或相似度较低的规则条目\n")
    if not low_sim_rules:
        report_lines.append("[OK] 合格: 所有对应条目语义高度重合。\n")
    else:
        report_lines.append(f"共发现 **{len(low_sim_rules)}** 条可能被过度精简或篡改的条目：\n")
        for p_num, orig_text, ref_line, cov in low_sim_rules:
            report_lines.append(f"- **P{p_num} 原始文本**: {orig_text}")
            report_lines.append(f"  - **新版对应文本**: {ref_line}")
            report_lines.append(f"  - **字符覆盖度**: {cov:.2f}\n")
            
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    print("Discrepancy report successfully saved.")

if __name__ == "__main__":
    audit_rulebooks()
