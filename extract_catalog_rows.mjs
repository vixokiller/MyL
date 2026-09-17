import { SpreadsheetFile } from "@oai/artifact-tool";

const workbook = await SpreadsheetFile.importXlsx(
  "catalog/catalogo_cartas_helenica_olimpico.xlsx",
);
const sheet = workbook.worksheets.getItem("Cartas");
const result = await workbook.inspect({
  kind: "table",
  range: "Cartas!A1:Q37",
  include: "values",
  tableMaxRows: 40,
  tableMaxCols: 17,
});

const matrix = result.values ?? result.data?.values;
if (!Array.isArray(matrix) || matrix.length < 2) {
  throw new Error("No se pudieron leer las filas del catálogo.");
}

process.stdout.write(JSON.stringify({ headers: matrix[0], rows: matrix.slice(1) }));
