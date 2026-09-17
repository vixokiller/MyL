from __future__ import annotations

from collections.abc import Sequence

from .errors import IllegalAction, UnsupportedCard
from .model import CardInstance, CardType, GameState, Zone


FIRST_VERSION_CARD_IDS = frozenset(
    {
        "helenica-lira",
        "helenica-eros",
        "helenica-ofrenda-a-los-dioses",
        "helenica-panteon",
        "helenica-festin",
        "helenica-gaia",
        "helenica-hemera",
        "helenica-sileno",
        "helenica-triton",
        "helenica-templo-de-la-cazadora",
    }
)


def ensure_supported(source: CardInstance) -> None:
    if source.definition.card_id not in FIRST_VERSION_CARD_IDS:
        raise UnsupportedCard(
            f"{source.definition.name} no pertenece a la primera versión ejecutable."
        )


def _require_source(source: CardInstance, *zones: Zone) -> None:
    if source.zone not in zones:
        expected = ", ".join(zone.value for zone in zones)
        raise IllegalAction(f"La fuente debe estar en: {expected}.")


def _search_castle(
    game: GameState,
    player_id: str,
    *,
    card_type: CardType,
    selected: Sequence[CardInstance],
    maximum: int,
) -> list[CardInstance]:
    castle = game.player(player_id).cards(Zone.CASTLE)
    if len(selected) > maximum or len({c.instance_id for c in selected}) != len(selected):
        raise IllegalAction("La selección de búsqueda no es válida.")
    if any(c not in castle or c.definition.card_type is not card_type for c in selected):
        raise IllegalAction("La carta elegida no cumple el criterio de búsqueda.")
    for card in selected:
        game.move(card, Zone.HAND)
    # Según 7.7, una búsqueda con criterio baraja incluso cuando no encuentra.
    game.shuffle_castle(player_id)
    return list(selected)


def on_enter_play(
    game: GameState,
    source: CardInstance,
    *,
    use_optional: bool,
    selected: Sequence[CardInstance] = (),
    top_order: Sequence[CardInstance] = (),
) -> list[CardInstance]:
    """Resuelve únicamente disparos de entrada de la primera versión."""
    ensure_supported(source)
    card_id = source.definition.card_id
    owner = source.controller_id

    if card_id == "helenica-eros":
        _require_source(source, Zone.DEFENSE, Zone.ATTACK)
        if not use_optional:
            if selected:
                raise IllegalAction("No puede haber selección al rechazar la opción.")
            return []
        if game.turn_number != 1:
            raise IllegalAction("Eros solo busca Oros si entra durante el primer turno.")
        return _search_castle(
            game, owner, card_type=CardType.GOLD, selected=selected, maximum=2
        )

    if card_id == "helenica-hemera":
        _require_source(source, Zone.DEFENSE, Zone.ATTACK)
        if not use_optional:
            if top_order:
                raise IllegalAction("No puede haber orden al rechazar la opción.")
            return []
        castle = game.player(owner).cards(Zone.CASTLE)
        visible = castle[-min(3, len(castle)):]
        if len(top_order) != len(visible) or set(map(id, top_order)) != set(map(id, visible)):
            raise IllegalAction("El orden debe contener exactamente las cartas superiores miradas.")
        castle[-len(visible):] = list(top_order) if visible else []
        return list(top_order)

    if card_id == "helenica-triton":
        _require_source(source, Zone.DEFENSE, Zone.ATTACK)
        return game.draw(owner, 1) if use_optional else []

    # Lira y las continuas no generan un disparo de entrada compilado.
    if selected or top_order:
        raise IllegalAction("Esta carta no admite elecciones al entrar en juego.")
    return []


def on_leave_play(
    game: GameState, source: CardInstance, *, use_optional: bool
) -> list[CardInstance]:
    ensure_supported(source)
    if source.definition.card_id != "helenica-triton":
        return []
    if source.in_play:
        raise IllegalAction("Tritón todavía no ha salido del juego.")
    return game.draw(source.owner_id, 1) if use_optional else []


def activate_festin(
    game: GameState,
    source: CardInstance,
    *,
    discarded: Sequence[CardInstance],
) -> CardInstance:
    ensure_supported(source)
    if source.definition.card_id != "helenica-festin":
        raise IllegalAction("La fuente no es Festín.")
    _require_source(source, Zone.GOLD_RESERVE)
    owner = source.controller_id
    game.require_vigilance_of(owner)
    hand = game.player(owner).cards(Zone.HAND)
    if len(discarded) != 2 or len({c.instance_id for c in discarded}) != 2:
        raise IllegalAction("Festín exige descartar exactamente dos cartas distintas.")
    if any(card not in hand for card in discarded):
        raise IllegalAction("Las cartas descartadas deben estar en tu Mano.")
    if not game.player(owner).cards(Zone.CASTLE):
        raise IllegalAction("No hay carta disponible para robar.")
    for card in discarded:
        game.move(card, Zone.GRAVEYARD)
    return game.draw(owner, 1)[0]


def activate_gaia(
    game: GameState,
    source: CardInstance,
    *,
    selected: Sequence[CardInstance],
) -> list[CardInstance]:
    ensure_supported(source)
    if source.definition.card_id != "helenica-gaia":
        raise IllegalAction("La fuente no es Gaia.")
    _require_source(source, Zone.DEFENSE, Zone.ATTACK)
    owner = source.controller_id
    game.require_vigilance_of(owner)
    # Se valida antes de consumir el uso.
    castle = game.player(owner).cards(Zone.CASTLE)
    if len(selected) > 1 or any(
        card not in castle or card.definition.card_type is not CardType.ALLY
        for card in selected
    ):
        raise IllegalAction("Gaia solo puede buscar un Aliado.")
    game.mark_once_per_turn(source, "buscar_aliado")
    return _search_castle(
        game, owner, card_type=CardType.ALLY, selected=selected, maximum=1
    )


def activate_sileno(
    game: GameState,
    source: CardInstance,
    *,
    selected: CardInstance,
) -> CardInstance:
    ensure_supported(source)
    if source.definition.card_id != "helenica-sileno":
        raise IllegalAction("La fuente no es Sileno.")
    _require_source(source, Zone.DEFENSE, Zone.ATTACK)
    owner = source.controller_id
    game.require_vigilance_of(owner)
    if selected not in game.player(owner).cards(Zone.GRAVEYARD):
        raise IllegalAction("Sileno debe elegir una carta de tu Cementerio.")
    # Validación completa antes de pagar o mover.
    if len(game.player(owner).cards(Zone.GOLD_RESERVE)) < 2:
        raise IllegalAction("Sileno requiere pagar 2 de Oro.")
    game.pay_physical_gold(owner, 2)
    game.move(selected, Zone.CASTLE)
    game.shuffle_castle(owner)
    return selected


def effective_strength(game: GameState, ally: CardInstance) -> int:
    """Calcula las tres bonificaciones continuas respaldadas por el catálogo."""
    if ally.definition.card_type is not CardType.ALLY or ally.definition.strength is None:
        raise IllegalAction("Solo los Aliados tienen Fuerza en este alcance.")
    if not ally.in_play:
        return ally.definition.strength

    controller = ally.controller_id
    cards = game.all_cards(controller, Zone)
    bonus = 0
    for source in cards:
        card_id = source.definition.card_id
        if (
            card_id == "helenica-ofrenda-a-los-dioses"
            and source.zone is Zone.GOLD_RESERVE
            and ally.definition.race == "Olímpico"
        ):
            bonus += 1
        elif card_id == "helenica-templo-de-la-cazadora" and source.zone is Zone.SUPPORT:
            bonus += 1
        elif card_id == "helenica-panteon" and source.zone is Zone.SUPPORT:
            has_olympic = any(
                candidate.definition.card_type is CardType.ALLY
                and candidate.definition.race == "Olímpico"
                and candidate.in_play
                for candidate in cards
            )
            if has_olympic:
                bonus += 2
    return ally.definition.strength + bonus
