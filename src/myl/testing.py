from __future__ import annotations

from itertools import count

from .model import CardDefinition, CardInstance, GameState, Zone


_ids = count(1)


def make_card(definition: CardDefinition, owner_id: str, zone: Zone) -> CardInstance:
    return CardInstance(
        instance_id=f"test-card-{next(_ids)}",
        definition=definition,
        owner_id=owner_id,
        zone=zone,
    )


def add_card(
    game: GameState, definition: CardDefinition, owner_id: str, zone: Zone
) -> CardInstance:
    card = make_card(definition, owner_id, zone)
    game.add(card)
    return card

