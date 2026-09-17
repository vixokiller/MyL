from pathlib import Path

import pytest

from myl.catalog import load_catalog
from myl.model import GameState


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def catalog():
    return load_catalog(ROOT / "catalog" / "cards.provisional.json")


@pytest.fixture
def game():
    return GameState.for_players("p1", "p2", seed=7)

