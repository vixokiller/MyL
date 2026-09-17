import pytest

from myl.cards import (
    activate_festin,
    activate_gaia,
    activate_sileno,
    effective_strength,
    on_enter_play,
    on_leave_play,
)
from myl.errors import IllegalAction
from myl.model import CardType, Phase, Zone
from myl.testing import add_card


def definition(catalog, card_id):
    return catalog.by_id(card_id)


def first_definition(catalog, card_type: CardType, *, excluding=()):
    return next(
        card
        for card in catalog.cards
        if card.card_type is card_type and card.card_id not in excluding
    )


def test_lira_has_no_invented_ability_and_remains_provisional(catalog, game):
    lira = add_card(game, definition(catalog, "helenica-lira"), "p1", Zone.GOLD_RESERVE)
    assert lira.definition.effective_text is None
    assert not lira.definition.is_verified
    assert on_enter_play(game, lira, use_optional=False) == []


def test_eros_searches_up_to_two_gold_only_on_first_turn(catalog, game):
    eros = add_card(game, definition(catalog, "helenica-eros"), "p1", Zone.DEFENSE)
    gold_def = definition(catalog, "helenica-ofrenda-a-los-dioses")
    golds = [add_card(game, gold_def, "p1", Zone.CASTLE) for _ in range(2)]
    found = on_enter_play(game, eros, use_optional=True, selected=golds)
    assert found == golds
    assert all(card.zone is Zone.HAND for card in golds)

    late_game = type(game).for_players("p1", "p2")
    late_game.turn_number = 2
    late_eros = add_card(late_game, eros.definition, "p1", Zone.DEFENSE)
    with pytest.raises(IllegalAction, match="primer turno"):
        on_enter_play(late_game, late_eros, use_optional=True)


def test_ofrenda_bonifies_only_olympic_allies_while_in_reserve(catalog, game):
    ally = add_card(game, definition(catalog, "helenica-hemera"), "p1", Zone.DEFENSE)
    offering = add_card(
        game, definition(catalog, "helenica-ofrenda-a-los-dioses"), "p1", Zone.GOLD_RESERVE
    )
    assert effective_strength(game, ally) == 2
    game.move(offering, Zone.PAID_GOLD)
    assert effective_strength(game, ally) == 1


def test_panteon_requires_an_olympic_ally_and_bonifies_all_allies(catalog, game):
    pantheon = add_card(game, definition(catalog, "helenica-panteon"), "p1", Zone.SUPPORT)
    olympic = add_card(game, definition(catalog, "helenica-hemera"), "p1", Zone.DEFENSE)
    assert effective_strength(game, olympic) == 3
    game.move(olympic, Zone.GRAVEYARD)
    assert effective_strength(game, olympic) == 1
    assert pantheon.zone is Zone.SUPPORT


def test_festin_discards_two_and_draws_one_atomically(catalog, game):
    festin = add_card(game, definition(catalog, "helenica-festin"), "p1", Zone.GOLD_RESERVE)
    filler = first_definition(catalog, CardType.ALLY)
    hand = [add_card(game, filler, "p1", Zone.HAND) for _ in range(2)]
    drawn = add_card(game, filler, "p1", Zone.CASTLE)
    assert activate_festin(game, festin, discarded=hand) is drawn
    assert all(card.zone is Zone.GRAVEYARD for card in hand)
    assert drawn.zone is Zone.HAND

    bad_game = type(game).for_players("p1", "p2")
    bad_festin = add_card(bad_game, festin.definition, "p1", Zone.GOLD_RESERVE)
    only = add_card(bad_game, filler, "p1", Zone.HAND)
    with pytest.raises(IllegalAction):
        activate_festin(bad_game, bad_festin, discarded=[only])
    assert only.zone is Zone.HAND


def test_gaia_searches_one_ally_once_per_turn(catalog, game):
    gaia = add_card(game, definition(catalog, "helenica-gaia"), "p1", Zone.DEFENSE)
    target = add_card(game, definition(catalog, "helenica-hemera"), "p1", Zone.CASTLE)
    assert activate_gaia(game, gaia, selected=[target]) == [target]
    assert target.zone is Zone.HAND
    with pytest.raises(IllegalAction, match="ya se utilizó"):
        activate_gaia(game, gaia, selected=[])


def test_hemera_reorders_exactly_the_top_three(catalog, game):
    hemera = add_card(game, definition(catalog, "helenica-hemera"), "p1", Zone.DEFENSE)
    filler = first_definition(catalog, CardType.ALLY)
    cards = [add_card(game, filler, "p1", Zone.CASTLE) for _ in range(4)]
    requested = [cards[3], cards[1], cards[2]]
    on_enter_play(game, hemera, use_optional=True, top_order=requested)
    assert game.player("p1").cards(Zone.CASTLE)[-3:] == requested
    assert game.player("p1").cards(Zone.CASTLE)[0] is cards[0]


def test_sileno_pays_two_gold_and_shuffles_graveyard_card(catalog, game):
    sileno = add_card(game, definition(catalog, "helenica-sileno"), "p1", Zone.DEFENSE)
    gold_def = definition(catalog, "helenica-ofrenda-a-los-dioses")
    golds = [add_card(game, gold_def, "p1", Zone.GOLD_RESERVE) for _ in range(2)]
    target = add_card(game, definition(catalog, "helenica-hemera"), "p1", Zone.GRAVEYARD)
    assert activate_sileno(game, sileno, selected=target) is target
    assert all(card.zone is Zone.PAID_GOLD for card in golds)
    assert target.zone is Zone.CASTLE


def test_triton_draws_on_enter_and_after_leaving_play(catalog, game):
    triton = add_card(game, definition(catalog, "helenica-triton"), "p1", Zone.DEFENSE)
    filler = first_definition(catalog, CardType.ALLY)
    first = add_card(game, filler, "p1", Zone.CASTLE)
    second = add_card(game, filler, "p1", Zone.CASTLE)
    assert on_enter_play(game, triton, use_optional=True) == [second]
    game.move(triton, Zone.GRAVEYARD)
    assert on_leave_play(game, triton, use_optional=True) == [first]


def test_temple_bonifies_all_controlled_allies_only_while_in_play(catalog, game):
    ally = add_card(game, definition(catalog, "helenica-hemera"), "p1", Zone.DEFENSE)
    temple = add_card(
        game, definition(catalog, "helenica-templo-de-la-cazadora"), "p1", Zone.SUPPORT
    )
    assert effective_strength(game, ally) == 2
    game.move(temple, Zone.GRAVEYARD)
    assert effective_strength(game, ally) == 1


def test_activated_cards_require_own_vigilance(catalog, game):
    gaia = add_card(game, definition(catalog, "helenica-gaia"), "p1", Zone.DEFENSE)
    game.phase = Phase.FINAL
    with pytest.raises(IllegalAction, match="Vigilia"):
        activate_gaia(game, gaia, selected=[])

