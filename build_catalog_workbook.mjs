import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const outputPath = "/home/vixokiller/.codex/.chatgpt-projects/g-p-6a33f2f0db888191809d63b160136ccc/catalog/catalogo_cartas_helenica_olimpico.xlsx";
const previewPath = "/tmp/catalogo_cartas_helenica_olimpico.png";

const cards = [
  [1,"Lira","Lira","Oro",null,null,null,"Helénica",null,null,null,"Oro Inicial confirmado","Pendiente de ficha","Primera versión",null,"Parcial","Elegible como Oro Inicial; falta confirmar impresión y texto."],
  [2,"Almas de estigia","Almas de Estigia",null,null,null,null,"Helénica",null,null,null,"Máximo general","Pendiente de ficha","Por clasificar",null,"No",null],
  [1,"Astreo","Astreo",null,null,null,null,"Helénica",null,null,null,"Máximo general","Pendiente de ficha","Por clasificar",null,"No",null],
  [3,"Eros","Eros",null,null,null,null,"Helénica",null,null,null,"Máximo general","Pendiente de ficha","Por clasificar",null,"No",null],
  [3,"Ofrenda a los Dioses","Ofrenda a los Dioses",null,null,null,null,"Helénica",null,null,"Si Ofrenda a los Dioses está en tu Reserva, todos tus Aliados de raza Olímpico ganan 1 a la fuerza.","Máximo general","Texto visible; faltan datos","Primera versión",null,"Parcial","Continua simple candidata al prototipo."],
  [1,"Aceite de Oliva","Aceite de Oliva",null,null,null,null,"Helénica",null,null,null,"Limitada a 1; cumple","Pendiente de ficha","Por clasificar",null,"No",null],
  [2,"Ares","Ares",null,null,null,null,"Helénica",null,null,null,"Máximo general","Pendiente de ficha","Por clasificar",null,"No",null],
  [3,"Atenea","Atenea",null,null,null,null,"Helénica",null,null,null,"Máximo general","Pendiente de ficha","Por clasificar",null,"No",null],
  [2,"Panteon","Panteón",null,null,null,null,"Helénica",null,null,null,"Limitada a 2; cumple","Pendiente de ficha","Por clasificar",null,"No",null],
  [1,"Alastor","Alastor",null,null,null,null,"Helénica",null,null,null,"Máximo general","Pendiente de ficha","Por clasificar",null,"No",null],
  [1,"Comus","Comus",null,null,null,null,"Helénica",null,null,null,"Máximo general","Pendiente de ficha","Por clasificar",null,"No",null],
  [1,"Festin","Festín",null,null,null,null,"Helénica",null,null,null,"Máximo general","Pendiente de ficha","Por clasificar",null,"No",null],
  [1,"Figuras Negras","Figuras Negras",null,null,null,null,"Helénica",null,null,"Si este Oro está en tu Reserva de Oros, puedes desterrarlo para que un Oro en juego y todas sus copias pierdan su habilidad hasta la Fase Final.","Máximo general","Texto visible; faltan datos","Posterior",null,"Parcial","Requiere destierro y pérdida temporal de habilidades."],
  [1,"Gaia","Gaia",null,null,null,null,"Helénica",null,null,null,"Máximo general","Identidad confirmada; falta ficha","Por clasificar",null,"Parcial","Carta distinta de Gea."],
  [2,"Helios","Helios",null,null,null,null,"Helénica",null,null,null,"Limitada a 2; cumple","Pendiente de ficha","Por clasificar",null,"No",null],
  [1,"El Oscuro Hades","El Oscuro Hades",null,null,null,null,"Helénica",null,null,null,"Máximo general","Pendiente de ficha","Por clasificar",null,"No",null],
  [2,"Zagreus","Zagreus",null,null,null,null,"Helénica",null,null,null,"Máximo general","Pendiente de ficha","Por clasificar",null,"No",null],
  [2,"Arcas del Imperio","Arcas del Imperio",null,null,null,null,"Helénica",null,null,null,"Máximo general","Pendiente de ficha","Por clasificar",null,"No",null],
  [1,"Trono dorado","Trono Dorado",null,null,null,null,"Helénica",null,null,null,"Máximo general","Pendiente de ficha","Por clasificar",null,"No",null],
  [1,"Ave de Hera","Ave de Hera",null,null,null,null,"Helénica",null,null,null,"Máximo general","Pendiente de ficha","Por clasificar",null,"No",null],
  [1,"Hemera","Hemera",null,null,null,null,"Helénica",null,null,null,"Máximo general","Pendiente de ficha","Por clasificar",null,"No",null],
  [2,"Olimpicos","Olímpicos",null,null,null,null,"Helénica",null,null,null,"Máximo general","Pendiente de ficha","Por clasificar",null,"No",null],
  [1,"Sileno","Sileno",null,null,null,null,"Helénica",null,null,null,"Máximo general","Pendiente de ficha","Por clasificar",null,"No",null],
  [2,"Afrodita","Afrodita",null,null,null,null,"Helénica",null,null,null,"Limitada a 2; cumple","Pendiente de ficha","Por clasificar",null,"No",null],
  [1,"Triton","Tritón",null,null,null,null,"Helénica",null,null,null,"Máximo general","Pendiente de ficha","Por clasificar",null,"No",null],
  [1,"Hilo de Ariadna","Hilo de Ariadna",null,null,null,null,"Helénica",null,null,null,"Máximo general","Pendiente de ficha","Por clasificar",null,"No",null],
  [1,"Dionisio zagreo","Dionisio Zagreo",null,null,null,null,"Helénica",null,null,null,"Máximo general","Pendiente de ficha","Por clasificar",null,"No",null],
  [1,"Focea","Focea",null,null,null,null,"Helénica",null,null,"Cuando entra en juego, pon al tope del Mazo Castillo de su dueño una carta oponente en juego que no sea Oro. En Guerra de Talismanes, puedes destruir este Tótem para robar 2 cartas. Luego, descarta una carta de tu Mano.","Máximo general","Texto visible; faltan datos","Posterior",null,"Parcial","Requiere retorno, robo, descarte y Guerra de Talismanes."],
  [1,"Templo de la Cazadora","Templo de la Cazadora",null,null,null,null,"Helénica",null,null,null,"Máximo general","Pendiente de ficha","Por clasificar",null,"No",null],
  [1,"Lyssa","Lyssa",null,null,null,null,"Helénica",null,null,null,"Máximo general","Pendiente de ficha","Por clasificar",null,"No",null],
  [1,"Fenix","Fénix",null,null,null,null,"Helénica",null,null,null,"Máximo general","Pendiente de ficha","Por clasificar",null,"No",null],
  [1,"Hera","Hera",null,null,null,null,"Helénica",null,null,null,"Máximo general","Pendiente de ficha","Por clasificar",null,"No",null],
  [1,"Thanatos","Thanatos",null,null,null,null,"Helénica",null,null,null,"Máximo general","Pendiente de ficha","Por clasificar",null,"No",null],
  [1,"Aguila Imperial","Águila Imperial",null,null,null,null,"Helénica",null,null,null,"Máximo general","Pendiente de ficha","Por clasificar",null,"No",null],
  [1,"Titanes","Titanes",null,null,null,null,"Helénica",null,null,null,"Máximo general","Pendiente de ficha","Por clasificar",null,"No",null],
  [1,"El Gran Zeus","El Gran Zeus",null,null,null,null,"Helénica",null,null,"El Gran Zeus es indestructible. En tu Fase de Vigilia, sólo una vez por turno, puedes robar hasta 2 cartas. Carta única.","Única; una copia, cumple","Texto visible; faltan datos","Segunda etapa",null,"Parcial","Reglas definidas; falta compilar y probar."],
];

const headers = ["Cantidad","Nombre recibido","Nombre oficial","Tipo","Coste","Fuerza","Raza","Edición","Producto","Texto impreso","Texto efectivo","Legalidad","Estado de catálogo","Etapa del motor","Fuente URL","Verificado","Notas"];
const wb = Workbook.create();
const guide = wb.worksheets.add("Guía");
const sheet = wb.worksheets.add("Cartas");
guide.showGridLines = false;
sheet.showGridLines = false;

guide.getRange("A2:F2").merge();
guide.getRange("A2").values = [["Catálogo Helénica – Olímpico"]];
guide.getRange("A2").format.font = { name: "Arial", size: 16, bold: true, color: "#1F2937" };
guide.getRange("A3:F3").format.borders = { bottom: { style: "thin", color: "#64748B" } };
guide.getRange("A5:B11").values = [
  ["Paso","Qué hacer y dónde"],
  ["1. Datos de carta","Completar las celdas amarillas de la hoja Cartas: Tipo, Coste, Fuerza, Raza, Producto, textos y Fuente URL."],
  ["2. Verificación","Cambiar Verificado a Sí solo cuando los datos coincidan con una ficha identificable. Si hay dudas, usar Parcial."],
  ["3. Legalidad","No modificar manualmente salvo que exista una fuente nueva. Codex mantiene la banlist y sus límites."],
  ["4. Etapa del motor","Codex clasifica cada carta como Primera versión, Segunda etapa o Posterior según sus mecánicas."],
  ["5. Archivos técnicos","No editar los JSON. Codex trasladará los datos verificados del Excel al catálogo del motor."],
  ["6. Programación","Cuando haya un grupo de cartas verificadas, Codex creará las definiciones y pruebas Python."],
];
guide.getRange("A13:B17").values = [
  ["Estado","Significado"],
  ["No","La ficha todavía no fue comprobada."],
  ["Parcial","Existe información útil, pero falta al menos un dato o una fuente."],
  ["Sí","Todos los campos necesarios fueron contrastados con una fuente."],
  ["Regla práctica","Puedes pegar texto o una URL aunque no sepas clasificarla; Codex revisará el resto."],
];
guide.getRange("D5:E9").values = [
  ["Resumen","Valor"],
  ["Cartas distintas",36],
  ["Copias totales",50],
  ["Fichas verificadas",null],
  ["Fichas pendientes",null],
];
guide.getRange("E8").formulas = [["=COUNTIF(Cartas!P2:P37,\"Sí\")"]];
guide.getRange("E9").formulas = [["=36-E8"]];

sheet.getRange("A1:Q1").values = [headers];
sheet.getRange("A2").write(cards);
const table = sheet.tables.add("A1:Q37", true, "CatalogoCartas");
table.style = "TableStyleMedium2";
sheet.freezePanes.freezeRows(1);
sheet.freezePanes.freezeColumns(3);
sheet.getRange("D2:K37").format.fill = "#FFF2CC";
sheet.getRange("O2:P37").format.fill = "#FFF2CC";
sheet.getRange("P2:P37").dataValidation = { rule: { type: "list", values: ["No","Parcial","Sí"] } };
sheet.getRange("D2:D37").dataValidation = { rule: { type: "list", values: ["Aliado","Arma","Tótem","Talismán","Oro"] } };
sheet.getRange("N2:N37").dataValidation = { rule: { type: "list", values: ["Por clasificar","Primera versión","Segunda etapa","Posterior"] } };
sheet.getRange("A2:A37").format.numberFormat = "0";

for (const s of [guide, sheet]) {
  const used = s.getUsedRange();
  used.format.font = { name: "Arial", size: 10, color: "#1F2937" };
  used.format.verticalAlignment = "center";
}
guide.getRange("A5:B5").format = { fill: "#1F4E78", font: { name: "Arial", size: 10, bold: true, color: "#FFFFFF" } };
guide.getRange("A13:B13").format = { fill: "#1F4E78", font: { name: "Arial", size: 10, bold: true, color: "#FFFFFF" } };
guide.getRange("D5:E5").format = { fill: "#1F4E78", font: { name: "Arial", size: 10, bold: true, color: "#FFFFFF" } };
guide.getRange("A6:B11").format.wrapText = true;
guide.getRange("A14:B17").format.wrapText = true;
guide.getRange("A:A").format.columnWidth = 24;
guide.getRange("B:B").format.columnWidth = 72;
guide.getRange("C:C").format.columnWidth = 3;
guide.getRange("D:D").format.columnWidth = 24;
guide.getRange("E:E").format.columnWidth = 16;
guide.getRange("A5:B11").format.autofitRows();
guide.getRange("A13:B17").format.autofitRows();

sheet.getRange("A1:Q1").format = { fill: "#1F4E78", font: { name: "Arial", size: 10, bold: true, color: "#FFFFFF" }, wrapText: true, horizontalAlignment: "center", verticalAlignment: "center" };
sheet.getRange("A:A").format.columnWidth = 10;
sheet.getRange("B:C").format.columnWidth = 24;
sheet.getRange("D:D").format.columnWidth = 14;
sheet.getRange("E:F").format.columnWidth = 10;
sheet.getRange("G:I").format.columnWidth = 16;
sheet.getRange("J:K").format.columnWidth = 48;
sheet.getRange("L:N").format.columnWidth = 24;
sheet.getRange("O:O").format.columnWidth = 34;
sheet.getRange("P:P").format.columnWidth = 12;
sheet.getRange("Q:Q").format.columnWidth = 42;
sheet.getRange("J2:Q37").format.wrapText = true;
sheet.getRange("A1:Q37").format.autofitRows();
sheet.getRange("A2:A37").format.horizontalAlignment = "right";

wb.recalculate();
const inspection = await wb.inspect({ kind: "table", sheetId: "Cartas", range: "A1:Q8", include: "values,formulas", tableMaxRows: 8, tableMaxCols: 17 });
console.log(inspection.ndjson);
const errors = await wb.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!", options: { useRegex: true, maxResults: 100 }, summary: "final formula error scan" });
console.log(errors.ndjson);
const preview = await wb.render({ sheetName: "Guía", range: "A1:F18", scale: 1.5, format: "png" });
await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));
await fs.mkdir(new URL(".", `file://${outputPath}`).pathname, { recursive: true });
const output = await SpreadsheetFile.exportXlsx(wb);
await output.save(outputPath);
