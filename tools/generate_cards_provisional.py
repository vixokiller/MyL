#!/usr/bin/env python3
"""Genera el JSON provisional sin inferir ni verificar campos ausentes."""

from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re
from xml.etree import ElementTree as ET
from zipfile import ZipFile


NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
RID_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_NS = {"r": "http://schemas.openxmlformats.org/package/2006/relationships"}
HEADERS = [
    "Cantidad", "Nombre recibido", "Nombre oficial", "Tipo", "Coste", "Fuerza",
    "Raza", "Edición", "Producto", "Texto impreso", "Texto efectivo", "Legalidad",
    "Estado de catálogo", "Etapa del motor", "Fuente URL", "Verificado", "Notas",
]


def slug(value: str) -> str:
    table = str.maketrans("áéíóúÁÉÍÓÚ", "aeiouAEIOU")
    return re.sub(r"[^a-z0-9ñ]+", "-", value.translate(table).lower()).strip("-")


def _shared_strings(book: ZipFile) -> list[str]:
    try:
        root = ET.fromstring(book.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    return ["".join(node.itertext()) for node in root.findall("m:si", NS)]


def _sheet_path(book: ZipFile, title: str) -> str:
    workbook = ET.fromstring(book.read("xl/workbook.xml"))
    sheet = next(s for s in workbook.findall("m:sheets/m:sheet", NS) if s.attrib["name"] == title)
    relation_id = sheet.attrib[f"{{{RID_NS}}}id"]
    rels = ET.fromstring(book.read("xl/_rels/workbook.xml.rels"))
    relation = next(r for r in rels.findall("r:Relationship", PKG_NS) if r.attrib["Id"] == relation_id)
    target = relation.attrib["Target"].lstrip("/")
    return target if target.startswith("xl/") else f"xl/{target}"


def _cell_value(cell: ET.Element, shared: list[str]):
    cell_type = cell.attrib.get("t")
    value = cell.find("m:v", NS)
    if cell_type == "inlineStr":
        inline = cell.find("m:is", NS)
        return "".join(inline.itertext()) if inline is not None else None
    if value is None:
        return None
    if cell_type == "s":
        return shared[int(value.text)]
    if cell_type in {"str", "b"}:
        return value.text
    number = float(value.text)
    return int(number) if number.is_integer() else number


def read_cards(path: Path) -> list[dict[str, object]]:
    with ZipFile(path) as book:
        shared = _shared_strings(book)
        root = ET.fromstring(book.read(_sheet_path(book, "Cartas")))
    rows: list[list[object]] = []
    for row in root.findall("m:sheetData/m:row", NS):
        values = [None] * len(HEADERS)
        for cell in row.findall("m:c", NS):
            column = re.match(r"[A-Z]+", cell.attrib["r"]).group()
            index = 0
            for char in column:
                index = index * 26 + ord(char) - 64
            if index <= len(HEADERS):
                values[index - 1] = _cell_value(cell, shared)
        rows.append(values)
    if not rows or rows[0] != HEADERS:
        raise ValueError("La hoja Cartas no tiene las 17 columnas esperadas.")

    cards = []
    for values in rows[1:]:
        if not values[2]:
            continue
        verified = str(values[15]).strip().casefold() == "sí"
        cards.append(
            {
                "card_id": f"helenica-{slug(str(values[2]))}",
                "quantity_in_mirror_deck": int(values[0]),
                "received_name": values[1],
                "name": values[2],
                "type": values[3],
                "cost": values[4],
                "strength": values[5],
                "race": values[6],
                "edition": values[7],
                "product": values[8],
                "printed_text": values[9],
                "effective_text": values[10],
                "legality": values[11],
                "catalog_status": values[12],
                "implementation_stage": values[13],
                "source_url": values[14],
                "verification_status": "verified" if verified else "partial",
                "notes": values[16],
            }
        )
    return cards


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--generated-at", default=date.today().isoformat())
    args = parser.parse_args()
    cards = read_cards(args.input)
    document = {
        "catalog_id": "helenica-olimpico-provisional-v1",
        "status": "provisional",
        "generated_from": args.input.name,
        "generated_at": args.generated_at,
        "scope": {
            "format": "Racial Edición — Primer Bloque",
            "edition": "Helénica",
            "race": "Olímpico",
            "deck_mode": "mirror",
            "distinct_cards": len(cards),
            "total_copies": sum(card["quantity_in_mirror_deck"] for card in cards),
        },
        "provenance": {
            "kind": "user_transcription",
            "missing_fields": ["product", "source_url"],
            "interpretation": "Usable for prototype implementation and tests; not an official verified database.",
        },
        "cards": cards,
    }
    args.output.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()

