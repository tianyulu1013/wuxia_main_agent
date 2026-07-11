import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const root = path.resolve(".");
const inputPath = path.join(root, "已制作.xlsx");
const classificationPath = path.join(root, "data", "excel_patch_candidates", "2025_diff_classification.json");
const outputDir = path.join(root, "outputs", "2025-excel-sync-candidate");
const outputPath = path.join(outputDir, "已制作_2025日志A类同步候选.xlsx");
const auditPath = path.join(root, "docs", "2025-a-class-excel-patch-audit.md");

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

async function main() {
  await fs.mkdir(outputDir, { recursive: true });

  const input = await FileBlob.load(inputPath);
  const workbook = await SpreadsheetFile.importXlsx(input);

  const beforePreview = await workbook.render({
    sheetName: "战斗人物",
    range: "A1:K20",
    scale: 1,
    format: "png",
  });
  await fs.writeFile(
    path.join(outputDir, "before_战斗人物_A1_K20.png"),
    new Uint8Array(await beforePreview.arrayBuffer()),
  );

  const classification = JSON.parse(await fs.readFile(classificationPath, "utf8"));
  const records = classification.records.filter(
    (record) => record.category === "A_可直接同步候选" && record.patch && record.field,
  );

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

    const next = current.replace(oldText, newText);
    cell.values = [[next]];
    audit.push({ ...record, result: "applied", reason: "已替换单元格内匹配段落" });
  }

  const afterPreview = await workbook.render({
    sheetName: "战斗人物",
    range: "A1:K20",
    scale: 1,
    format: "png",
  });
  await fs.writeFile(
    path.join(outputDir, "after_战斗人物_A1_K20.png"),
    new Uint8Array(await afterPreview.arrayBuffer()),
  );

  const output = await SpreadsheetFile.exportXlsx(workbook);
  await output.save(outputPath);

  const applied = audit.filter((item) => item.result === "applied");
  const skipped = audit.filter((item) => item.result === "skipped");
  const lines = [
    "# 2025 A 类差异 Excel 副本生成审计",
    "",
    `- 输入：\`${path.relative(root, inputPath)}\``,
    `- 输出副本：\`${path.relative(root, outputPath)}\``,
    `- A 类候选总数：${records.length}`,
    `- 已应用：${applied.length}`,
    `- 已跳过：${skipped.length}`,
    "",
    "## 已应用",
    "",
  ];

  for (const item of applied) {
    lines.push(`- ${item.title} / ${item.date} / ${item.sheet}!${item.row} / \`${item.field}\``);
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
