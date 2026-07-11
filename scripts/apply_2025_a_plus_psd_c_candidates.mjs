import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const root = path.resolve(".");
const inputPath = path.join(root, "已制作.xlsx");
const classificationPath = path.join(root, "data", "excel_patch_candidates", "2025_diff_classification.json");
const outputDir = path.join(root, "outputs", "2025-excel-sync-candidate");
const outputPath = path.join(outputDir, "已制作_2025日志同步候选_PSD校准.xlsx");
const auditPath = path.join(root, "docs", "2025-a-plus-psd-c-excel-patch-audit.md");

const psdConfirmedTitles = new Set(["卫宫切嗣", "原随云", "曹秋道", "罗格"]);
const psdRejectedPatchKeys = new Set([
  "曹秋道|2025/4/27|战斗人物|94|description|（可用三次）",
]);

const fieldHeaders = {
  title: "名称",
  life: "血量",
  identity: "身份",
  description: "描述",
  relationships: "关系",
  weapons: "兵器",
  source_work: "出处",
  author_group: "作者",
  gender: "性别",
  traits: "特性",
  item_category: "类别",
};

function asString(value) {
  if (value === null || value === undefined) return "";
  return String(value);
}

function shouldApply(record) {
  const rejectedKey = `${record.title}|${record.date}|${record.sheet}|${record.row}|${record.field}|${(record.changes || []).map((change) => change.text || "").join("")}`;
  if (psdRejectedPatchKeys.has(rejectedKey)) return false;
  return (
    record.category === "A_可直接同步候选" ||
    (record.category === "C_需要规则裁定" && psdConfirmedTitles.has(record.title))
  );
}

async function main() {
  await fs.mkdir(outputDir, { recursive: true });

  const input = await FileBlob.load(inputPath);
  const workbook = await SpreadsheetFile.importXlsx(input);

  const classification = JSON.parse(await fs.readFile(classificationPath, "utf8"));
  const records = classification.records
    .filter((record) => shouldApply(record) && record.field)
    .map((record) => ({
      ...record,
      patch: record.patch ?? { old_text: record.excel_text, new_text: record.log_text },
      source_decision: record.category === "C_需要规则裁定" ? "PSD 与日志一致，按 PSD 校准" : "A 类机械同步",
    }));

  const headerCache = new Map();
  const audit = [];

  for (const record of records) {
    const sheet = workbook.worksheets.getItem(record.sheet);
    if (!headerCache.has(record.sheet)) {
      const headers = sheet.getRange("A1:Z1").values[0].map(asString);
      headerCache.set(record.sheet, headers);
    }

    const headers = headerCache.get(record.sheet);
    const header = fieldHeaders[record.field];
    const colIndex = headers.indexOf(header);
    if (colIndex < 0) {
      audit.push({ ...record, result: "skipped", reason: `找不到表头 ${header}` });
      continue;
    }

    const cell = sheet.getRangeByIndexes(record.row - 1, colIndex, 1, 1);
    const current = asString(cell.values[0][0]).replace(/\r\n/g, "\n").replace(/\r/g, "\n");
    const oldText = record.patch.old_text;
    const newText = record.patch.new_text;

    if (!current.includes(oldText)) {
      audit.push({ ...record, result: "skipped", reason: "当前单元格不包含候选旧文本，可能已被改过或定位不再准确" });
      continue;
    }

    cell.values = [[current.replace(oldText, newText)]];
    audit.push({ ...record, result: "applied", reason: "已替换单元格内匹配段落" });
  }

  const preview = await workbook.render({
    sheetName: "战斗人物",
    range: "A1:K20",
    scale: 1,
    format: "png",
  });
  await fs.writeFile(
    path.join(outputDir, "after_psd_calibrated_战斗人物_A1_K20.png"),
    new Uint8Array(await preview.arrayBuffer()),
  );

  const output = await SpreadsheetFile.exportXlsx(workbook);
  await output.save(outputPath);

  const applied = audit.filter((item) => item.result === "applied");
  const skipped = audit.filter((item) => item.result === "skipped");
  const lines = [
    "# 2025 A 类 + PSD 校准 C 类 Excel 副本生成审计",
    "",
    `- 输入：\`${path.relative(root, inputPath)}\``,
    `- 输出副本：\`${path.relative(root, outputPath)}\``,
    `- 候选总数：${records.length}`,
    `- 已应用：${applied.length}`,
    `- 已跳过：${skipped.length}`,
    "",
    "## 已应用",
    "",
  ];

  for (const item of applied) {
    lines.push(`- ${item.title} / ${item.date} / ${item.sheet}!${item.row} / \`${item.field}\` / ${item.source_decision}`);
    for (const change of item.changes || []) {
      lines.push(`  - ${change.summary}`);
    }
  }

  lines.push("", "## 已跳过", "");
  if (skipped.length === 0) {
    lines.push("- 无");
  } else {
    for (const item of skipped) {
      lines.push(`- ${item.title} / ${item.date} / ${item.sheet}!${item.row} / \`${item.field || "未定位字段"}\`: ${item.reason}`);
    }
  }

  await fs.writeFile(auditPath, lines.join("\n"), "utf8");
  console.log(JSON.stringify({ outputPath, auditPath, applied: applied.length, skipped: skipped.length }, null, 2));
}

main();
