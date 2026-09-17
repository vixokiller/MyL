from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
import random
from typing import Iterable

from .errors import IllegalAction


class CardType(StrEnum):
    ALLY = "Aliado"
    WEAPON = "Arma"
    TOTEM = "Tótem"
    TALISMAN = "Talismán"
    GOLD = "Oro"


class VerificationStatus(StrEnum):
    PARTIAL = "partial"
    VERIFIED = "verified"


class Phase(StrEnum):
    GROUPING = "agrupacion"
    VIGILANCE = "vigilia"
    BATTLE = "batalla_mitologica"
    FINAL = "final"


class Zone(StrEnum):
    CASTLE = "mazo_castillo"
    HAND = "mano"
    GOLD_RESERVE = "reserva_de_oro"
    PAID_GOLD = "oro_pagado"
    DEFENSE = "linea_de_defensa"
    ATTACK = "linea_de_ataque"
    SUPPORT = "linea_de_apoyo"
    GRAVEYARD = "cementerio"
    EXILE = "destierro"


IN_PLAY_ZONES = frozenset(
    {Zone.GOLD_RESERVE, Zone.PAID_GOLD, Zone.DEFENSE, Zone.ATTACK, Zone.SUPPORT}
)


@dataclass(frozen=True, slots=True)
class CardDefinition:
    card_id: str
    name: str
    received_name: str
    card_type: CardType
    cost: int | None
    strength: int | None
    race: str | None
    edition: str
    product: str | None
    printed_text: str | None
    effective_text: str | None
    legality: str
    implementation_stage: str
    source_url: str | None
    verification_status: VerificationStatus
    provenance_kind: str
    quantity_in_mirror_deck: int
    notes: str | None = None

    @property
    def is_verified(self) -> bool:
        return self.verification_status is VerificationStatus.VERIFIED


@dataclass(slots=True)
class CardInstance:
    instance_id: str
    definition: CardDefinition
    owner_id: str
    zone: Zone

    @property
    def controller_id(self) -> str:
        # El alcance inicial no implementa cambio de control. La zona y el dueño
        # bastan para derivarlo en los escenarios soportados.
        return self.owner_id

    @property
    def in_play(self) -> bool:
        return self.zone in IN_PLAY_ZONES


@dataclass(slots=True)
class PlayerState:
    player_id: str
    zones: dict[Zone, list[CardInstance]] = field(
        default_factory=lambda: {zone: [] for zone in Zone}
    )

    def cards(self, zone: Zone) -> list[CardInstance]:
        return self.zones[zone]


@dataclass(slots=True)
class GameState:
    players: dict[str, PlayerState]
    active_player_id: str
    turn_number: int = 1
    phase: Phase = Phase.VIGILANCE
    rng: random.Random = field(default_factory=lambda: random.Random(0))
    uses_this_turn: set[tuple[str, str, int]] = field(default_factory=set)

    @classmethod
    def for_players(cls, *player_ids: str, seed: int = 0) -> GameState:
        if len(player_ids) != 2 or len(set(player_ids)) != 2:
            raise ValueError("El prototipo requiere exactamente dos jugadores distintos.")
        return cls(
            players={pid: PlayerState(pid) for pid in player_ids},
            active_player_id=player_ids[0],
            rng=random.Random(seed),
        )

    def player(self, player_id: str) -> PlayerState:
        return self.players[player_id]

    def add(self, card: CardInstance) -> None:
        self.player(card.owner_id).cards(card.zone).append(card)

    def move(self, card: CardInstance, destination: Zone) -> None:
        origin = self.player(card.owner_id).cards(card.zone)
        try:
            origin.remove(card)
        except ValueError as exc:
            raise IllegalAction(f"{card.instance_id} no está en su zona declarada") from exc
        card.zone = destination
        self.player(card.owner_id).cards(destination).append(card)

    def draw(self, player_id: str, amount: int = 1) -> list[CardInstance]:
        if amount < 0:
            raise ValueError("La cantidad a robar no puede ser negativa.")
        castle = self.player(player_id).cards(Zone.CASTLE)
        if len(castle) < amount:
            raise IllegalAction("No hay suficientes cartas en el Mazo Castillo.")
        drawn = []
        for _ in range(amount):
            card = castle[-1]
            self.move(card, Zone.HAND)
            drawn.append(card)
        return drawn

    def shuffle_castle(self, player_id: str) -> None:
        self.rng.shuffle(self.player(player_id).cards(Zone.CASTLE))

    def require_vigilance_of(self, player_id: str) -> None:
        if self.phase is not Phase.VIGILANCE or self.active_player_id != player_id:
            raise IllegalAction("La habilidad solo puede usarse en tu Fase de Vigilia.")

    def mark_once_per_turn(self, source: CardInstance, ability_key: str) -> None:
        key = (source.instance_id, ability_key, self.turn_number)
        if key in self.uses_this_turn:
            raise IllegalAction("Esta habilidad ya se utilizó durante este turno.")
        self.uses_this_turn.add(key)

    def pay_physical_gold(self, player_id: str, amount: int) -> list[CardInstance]:
        reserve = self.player(player_id).cards(Zone.GOLD_RESERVE)
        if len(reserve) < amount:
            raise IllegalAction("No hay suficiente Oro físico disponible.")
        paid = list(reserve[-amount:]) if amount else []
        for card in paid:
            self.move(card, Zone.PAID_GOLD)
        return paid

    def all_cards(self, player_id: str, zones: Iterable[Zone]) -> list[CardInstance]:
        player = self.player(player_id)
        return [card for zone in zones for card in player.cards(zone)]

