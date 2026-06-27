def mill_cards(game, player, amount):
    """
    Bota cartas desde el mazo del jugador al cementerio.
    """
    for _ in range(amount):
        if player.deck.cards:
            card = player.deck.cards[-1]
            game.move_card(card, player.deck, player.graveyard)
            print(f"{player.name} bota {card.name} al cementerio.")
            if game.check_deck_loss(player):
                break
        else:
            print(f"{player.name} no tiene cartas en el mazo.")
            game.check_deck_loss(player)
            break


def discard_cards(game, player, amount):
    """
    Descarta cartas desde la mano del jugador al cementerio.
    """
    for _ in range(amount):
        if player.hand.cards:
            card = player.hand.cards[0]
            game.move_card(card, player.hand, player.graveyard)
            print(f"{player.name} descarta {card.name}.")
        else:
            print(f"{player.name} no tiene cartas en la mano.")
            break


def draw_cards(game, player, amount):
    """
    Roba cartas desde el mazo a la mano.
    """
    for _ in range(amount):
        card = player.deck.draw()
        if card:
            player.hand.add(card)
            print(f"{player.name} roba una carta.")
            if game.check_deck_loss(player):
                break
        else:
            print(f"{player.name} no puede robar porque no tiene cartas en el mazo.")
            game.check_deck_loss(player)
            break


def destroy_card(game, card):
    """
    Destruye una carta en juego y la manda al cementerio de su controlador.
    """
    player = card.controller

    if player is None:
        print(f"{card.name} no tiene controlador.")
        return

    possible_zones = [
        player.attack_line,
        player.defense_line,
        player.support_line
    ]

    for zone in possible_zones:
        if card in zone.cards:
            game.move_card(card, zone, player.graveyard)
            print(f"{card.name} fue destruida.")
            return

    print(f"{card.name} no está en una zona destruible.")
