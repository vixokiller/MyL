import json
from pathlib import Path
import subprocess
import sys

from myl.cards import FIRST_VERSION_CARD_IDS


ROOT = Path(__file__).resolve().parents[1]


def test_catalog_preserves_provenance_and_unverified_fields(catalog):
    assert catalog.status == "provisional"
    assert catalog.provenance["kind"] == "user_transcription"
    assert len(catalog.cards) == 36
    assert sum(card.quantity_in_mirror_deck for card in catalog.cards) == 50
    assert all(not card.is_verified for card in catalog.cards)
    assert all(card.product is None and card.source_url is None for card in catalog.cards)


def test_exactly_the_selected_ten_are_executable(catalog):
    selected = catalog.first_version()
    assert len(selected) == 10
    assert {card.card_id for card in selected} == FIRST_VERSION_CARD_IDS


def test_generator_reproduces_the_committed_catalog(tmp_path):
    output = tmp_path / "cards.json"
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "generate_cards_provisional.py"),
            str(ROOT / "catalog" / "catalogo_cartas_helenica_olimpico.xlsx"),
            str(output),
            "--generated-at",
            "2026-09-17",
        ],
        check=True,
    )
    expected = json.loads((ROOT / "catalog" / "cards.provisional.json").read_text())
    actual = json.loads(output.read_text())
    assert actual == expected

