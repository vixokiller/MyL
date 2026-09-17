import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const path = "/home/vixokiller/Proyectos/MyL/catalog/catalogo_cartas_helenica_olimpico.xlsx";
const input = await FileBlob.load(path);
const wb = await SpreadsheetFile.importXlsx(input);
const overview = await wb.inspect({
  kind: "workbook,sheet,table",
  maxChars: 8000,
  tableMaxRows: 5,
  tableMaxCols: 17,
  tableMaxCellChars: 160,
});
console.log(overview.ndjson);
const cards = await wb.inspect({
  kind: "table",
  sheetId: "Cartas",
  range: "A1:Q37",
  include: "values,formulas",
  tableMaxRows: 37,
  tableMaxCols: 17,
  tableMaxCellChars: 500,
  maxChars: 50000,
});
console.log(cards.ndjson);
const errors = await wb.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!",
  options: { useRegex: true, maxResults: 100 },
  summary: "formula errors",
});
console.log(errors.ndjson);
