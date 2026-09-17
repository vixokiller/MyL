import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const inputPath = "/home/vixokiller/Proyectos/MyL/catalog/catalogo_cartas_helenica_olimpico.xlsx";
const outputPath = "/home/vixokiller/.codex/.chatgpt-projects/g-p-6a33f2f0db888191809d63b160136ccc/catalog/catalogo_cartas_helenica_olimpico.xlsx";
const previewPath = "/tmp/catalogo_cartas_clasificado.png";

const first = new Set([
  "Lira", "Eros", "Ofrenda a los Dioses", "Panteón", "Festín", "Gaia",
  "Hemera", "Sileno", "Tritón", "Templo de la Cazadora",
]);
const second = new Set([
  "Almas de Estigia", "Astreo", "Aceite de Oliva", "Atenea", "Alastor",
  "Comus", "Trono Dorado", "Olímpicos", "Hilo de Ariadna", "El Gran Zeus",
]);
const posterior = new Set([
  "Ares", "Figuras Negras", "Helios", "El Oscuro Hades", "Zagreus",
  "Arcas del Imperio", "Ave de Hera", "Afrodita", "Dionisio Zagreo", "Focea",
  "Lyssa", "Fénix", "Hera", "Thanatos", "Águila Imperial", "Titanes",
]);

const input = await FileBlob.load(inputPath);
const wb = await SpreadsheetFile.importXlsx(input);
const sheet = wb.worksheets.getItem("Cartas");
const values = sheet.getRange("A1:Q37").values;

for (let row = 1; row < values.length; row++) {
  const name = values[row][2];
  let stage = "Por clasificar";
  if (first.has(name)) stage = "Primera versión";
  if (second.has(name)) stage = "Segunda etapa";
  if (posterior.has(name)) stage = "Posterior";
  sheet.getCell(row, 12).values = [["Datos provisionales; falta fuente/producto"]];
  sheet.getCell(row, 13).values = [[stage]];
}

// Thanatos es Única por su texto y la lista contiene una sola copia.
sheet.getRange("L34").values = [["Única; una copia, cumple"]];

const guide = wb.worksheets.getItem("Guía");
guide.getRange("D11:E14").values = [
  ["Clasificación","Cartas"],
  ["Primera versión",10],
  ["Segunda etapa",10],
  ["Posterior",16],
];
guide.getRange("D11:E11").format = {
  fill: "#1F4E78",
  font: { name: "Arial", size: 10, bold: true, color: "#FFFFFF" },
};
guide.getRange("D11:E14").format.verticalAlignment = "center";

wb.recalculate();
const check = await wb.inspect({
  kind: "table",
  sheetId: "Cartas",
  range: "A1:Q37",
  include: "values,formulas",
  tableMaxRows: 37,
  tableMaxCols: 17,
  maxChars: 50000,
});
console.log(check.ndjson);
const errors = await wb.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!",
  options: { useRegex: true, maxResults: 100 },
  summary: "final formula error scan",
});
console.log(errors.ndjson);
const preview = await wb.render({ sheetName: "Guía", range: "A1:F17", scale: 1.5, format: "png" });
await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));
const output = await SpreadsheetFile.exportXlsx(wb);
await output.save(outputPath);
