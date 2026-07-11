import sqlite3
import json
import re
from pathlib import Path

# 非标准术语与推荐词字典
NON_STANDARD_TERMS = {
    "扣血": "生命流失 / 损失生命",
    "掉血": "生命流失 / 损失生命",
    "掉生命": "生命流失 / 损失生命",
    "扣生命": "生命流失 / 损失生命",
    "血量": "生命值",
    "体力": "生命 / 生命值",
    "减少伤害": "抵挡 / 伤害减免",
    "降低伤害": "抵挡 / 伤害减免",
    "不吃伤害": "免除伤害 / 不中",
    "免疫伤害": "免除伤害 / 不中",
    "死掉": "死亡",
    "打死": "杀死"
}

# 规则书时序阶段词（用来检查特技是否缺乏明确时机说明）
TIMING_KEYWORDS = [
    "前", "后", "时", "开始", "结束", "阶段", "回合", "转轮", "对阵", "比拼"
]

def check_card_static(title, category, identity, description):
    issues = []
    
    # 1. 真实英文单词检测 (忽略代数变量如 n, x, y 及常见单字母，只匹配长度 >= 2 的英文单词)
    clean_desc = re.sub(r'\[.*?\]\(.*?\)', '', description)
    # 匹配长度大于等于 2 的英文字母单词
    eng_matches = re.findall(r'\b[a-zA-Z]{2,}\b', title + clean_desc)
    # 排除一些非术语的常用标记或缩写
    eng_filtered = [w for w in eng_matches if w.lower() not in ["json", "fields", "id"]]
    if eng_filtered:
        issues.append(f"含有非标准英文单词: {', '.join(eng_filtered)}")
        
    # 2. 术语规范化检测
    found_terms = []
    for term, recommend in NON_STANDARD_TERMS.items():
        if term in description or (identity and term in identity):
            found_terms.append(f"使用非标准词「{term}」（规则书推荐：「{recommend}」)")
    if found_terms:
        issues.extend(found_terms)
        
    # 3. 特技名与类型匹配度检测
    lines = description.splitlines()
    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue
        # 匹配特技定义行，通常形如 "*特技名：" 或 "*【特技名】：" 或 "【特技名】："
        skill_match = re.match(r'^\*?\s*【([^】]+)】|^\*?\s*([^*：:\s]+)\s*[：:]', line_str)
        if skill_match:
            skill_name = skill_match.group(1) or skill_match.group(2)
            # 检查是否有专属符号 【】
            if "【" in line_str and "】" in line_str:
                # 如果有专属特技符号，检查特技描述本身
                pass
            
            # 检查时机词
            has_timing = any(k in line_str for k in TIMING_KEYWORDS)
            if not has_timing and len(line_str) > 10:
                issues.append(f"特技「{skill_name}」描述中疑似缺失明确的触发/生效时机限制词")
                
            # 检查是否以“（身份）”结尾但不是身份特技
            if "（身份）" in line_str or "(身份)" in line_str:
                issues.append(f"特技「{skill_name}」文案带有“（身份）”，请核对该特技在数据层是否已正确标记为身份特技类型")
                
    return issues

def audit_cards_database():
    db_path = Path("data/cards.sqlite")
    report_path = Path("reports/2-card-text-audit-todos.md")
    
    if not db_path.exists():
        print(f"Error: Database {db_path} not found.")
        return
        
    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()
    
    # 仅审计人物卡和物品卡这类含有核心特技逻辑的卡牌
    c.execute("select title, category, identity, description, source_work from cards order by category, title")
    rows = c.fetchall()
    
    audit_results = {}
    total_audited = 0
    total_issues = 0
    
    for title, category, identity, description, source_work in rows:
        if not description:
            continue
            
        total_audited += 1
        issues = check_card_static(title, category, identity, description)
        
        if issues:
            total_issues += 1
            if source_work not in audit_results:
                audit_results[source_work] = []
            audit_results[source_work].append((title, category, issues, description))
            
    # 写入 TODO 报告
    report_lines = []
    report_lines.append("# 五行卡牌卡牌文案本地静态审计 TODO List\n")
    report_lines.append(f"- **审计源数据**: `data/cards.sqlite` 中的 `{total_audited}` 张卡牌")
    report_lines.append(f"- **问题发现**: 共发现 `{total_issues}` 张卡牌文案可能存在术语混淆、时机模糊或格式不规范问题。\n")
    report_lines.append("> [!NOTE]")
    report_lines.append("> 本报告由 `scripts/audit_cards.py` 静态筛查器自动生成，不消耗大模型 Token。优先纠正术语不匹配与时机模糊问题，可极大提升未来卡牌自动化比对逻辑的稳定性。\n")
    
    for work, cards in sorted(audit_results.items()):
        report_lines.append(f"## 📖 来源作品：{work or '未知'}\n")
        
        for title, category, issues, desc in cards:
            report_lines.append(f"### 🎴 [{category}] {title}")
            report_lines.append("#### 🚨 发现的问题：")
            for iss in issues:
                report_lines.append(f"- {iss}")
            report_lines.append("#### 📄 原始卡牌描述：")
            report_lines.append("```text")
            report_lines.append(desc)
            report_lines.append("```\n")
            
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Static card audit completed. Found {total_issues} suspicious cards. Report saved to {report_path}")

if __name__ == "__main__":
    audit_cards_database()
