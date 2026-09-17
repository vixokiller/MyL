from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Iterable

from .errors import CatalogError
from .model import CardDefinition, CardType, VerificationStatus


FIRST_VERSION = "Primera versión"


@dataclass(frozen=True, slots=True)
class CardCatalog:
    catalog_id: str
    status: str
    provenance: dict[str, Any]
    cards: tuple[CardDefinition, ...]

    def by_id(self, card_id: str) -> CardDefinition:
        for card in self.cards:
            if card.card_id == card_id:
                return card
        raise KeyError(card_id)

    def first_version(self) -> tuple[CardDefinition, ...]:
        return tuple(c for c in self.cards if c.implementation_stage == FIRST_VERSION)


def _optional_int(value: Any, field: str) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int):
        raise CatalogError(f"{field} debe ser entero o null")
    return value


def _card_from_json(raw: dict[str, Any], provenance_kind: str) -> CardDefinition:
    required = {
        "card_id", "received_name", "name", "type", "cost", "strength", "race",
        "edition", "product", "printed_text", "effective_text", "legality",
        "implementation_stage", "source_url", "verification_status",
        "quantity_in_mirror_deck",
    }
    missing = sorted(required - raw.keys())
    if missing:
        raise CatalogError(f"Faltan campos en una carta: {', '.join(missing)}")
    try:
        card_type = CardType(raw["type"])
        verification = VerificationStatus(raw["verification_status"])
    except ValueError as exc:
        raise CatalogError(str(exc)) from exc

    card = CardDefinition(
        card_id=str(raw["card_id"]),
        received_name=str(raw["received_name"]),
        name=str(raw["name"]),
        card_type=card_type,
        cost=_optional_int(raw["cost"], "cost"),
        strength=_optional_int(raw["strength"], "strength"),
        race=raw["race"],
        edition=str(raw["edition"]),
        product=raw["product"],
        printed_text=raw["printed_text"],
        effective_text=raw["effective_text"],
        legality=str(raw["legality"]),
        implementation_stage=str(raw["implementation_stage"]),
        source_url=raw["source_url"],
        verification_status=verification,
        provenance_kind=provenance_kind,
        quantity_in_mirror_deck=_optional_int(
            raw["quantity_in_mirror_deck"], "quantity_in_mirror_deck"
        ) or 0,
        notes=raw.get("notes"),
    )
    if card.quantity_in_mirror_deck <= 0:
        raise CatalogError("quantity_in_mirror_deck debe ser mayor que cero")
    if card.card_type is CardType.ALLY and card.strength is None:
        raise CatalogError(f"{card.card_id}: un Aliado requiere Fuerza")
    return card


def load_catalog(path: str | Path) -> CardCatalog:
    source = Path(path)
    try:
        raw = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CatalogError(f"No se pudo cargar {source}: {exc}") from exc

    provenance = raw.get("provenance")
    if not isinstance(provenance, dict) or not provenance.get("kind"):
        raise CatalogError("El catálogo debe declarar provenance.kind")
    rows = raw.get("cards")
    if not isinstance(rows, list):
        raise CatalogError("cards debe ser una lista")
    cards = tuple(_card_from_json(row, provenance["kind"]) for row in rows)
    ids = [card.card_id for card in cards]
    if len(ids) != len(set(ids)):
        raise CatalogError("El catálogo contiene card_id duplicados")
    return CardCatalog(
        catalog_id=str(raw.get("catalog_id", "")),
        status=str(raw.get("status", "")),
        provenance=provenance,
        cards=cards,
    )


def select_first_version(cards: Iterable[CardDefinition]) -> tuple[CardDefinition, ...]:
    return tuple(card for card in cards if card.implementation_stage == FIRST_VERSION)

