import random
import sys
from pathlib import Path

from ability_system import AbilitySystem
from card_loader import load_card_database, load_deck


CARD_TYPES = {
    "Oro": 0,
    "Aliado": 1,
    "Arma": 2,
    "Totem": 3,
    "Talismán": 4,
    "Talisman": 4,
}

TYPE_NAMES = {
    0: "Oro",
    1: "Aliado",
    2: "Arma",
    3: "Totem",
    4: "Talismán",
}

PHASE_NAMES = {
    0: "Agrupacion",
    1: "Vigilia",
    2: "Declaracion de ataque",
    3: "Declaracion de bloqueo",
    4: "Guerra de talismanes",
    5: "Asignacion de dano",
    6: "Final",
    7: "Robar",
}


class Card:
    def __init__(self, name, type, cost=0):
        self.name = name
        self.type = type
        self.cost = cost or 0
        self.controller = None
        self.abilities = []
        self.text = ""
        self.id = None

    @property
    def type_name(self):
        return TYPE_NAMES.get(self.type, str(self.type))

    def __repr__(self):
        return self.name


class Ally(Card):
    def __init__(self, name, type, cost, strength):
        super().__init__(name, type, cost)
        self.strength = strength
        self.strenght = strength
        self.enter_turn = 0
        self.can_attack = True
        self.can_defense = True


class Gold(Card):
    def __init__(self, name, type, cost=0):
        super().__init__(name, type, cost)


class Zone:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def remove(self, card):
        if card in self.cards:
            self.cards.remove(card)
            return card
        return None

    def move_to(self, card, zone):
        moved_card = self.remove(card)
        if moved_card is None:
            return False
        zone.add(moved_card)
        return True

    def regroup(self, zone):
        while self.cards:
            self.move_to(self.cards[0], zone)

    def pay(self, card, paid_zone):
        if card.cost > len(self.cards):
            print(f"No tienes suficientes oros para jugar {card.name}.")
            return False

        for _ in range(card.cost):
            self.move_to(self.cards[0], paid_zone)
        return True

    def take_damage(self, graveyard, damage):
        for _ in range(damage):
            if not self.cards:
                print("El jugador no tiene cartas en el mazo.")
                break
            self.move_to(self.cards[-1], graveyard)

    def short_list(self):
        return ", ".join(card.name for card in self.cards) or "-"


class Deck(Zone):
    def __init__(self):
        super().__init__("Mazo")

    def shuffle_deck(self):
        random.shuffle(self.cards)

    def draw(self):
        if self.cards:
            return self.cards.pop()
        return None


class Graveyard(Zone):
    def __init__(self):
        super().__init__("Cementerio")


class Exile(Zone):
    def __init__(self):
        super().__init__("Destierro")


class GoldReserve(Zone):
    def __init__(self):
        super().__init__("Reserva de oros")


class PaidGoldZone(Zone):
    def __init__(self):
        super().__init__("Zona de oro pagado")


class SupportLine(Zone):
    def __init__(self):
        super().__init__("Línea de apoyo")


class DefenseLine(Zone):
    def __init__(self):
        super().__init__("Línea de defensa")


class AttackLine(Zone):
    def __init__(self):
        super().__init__("Línea de ataque")


class Player:
    def __init__(self, name):
        self.name = name
        self.deck = Deck()
        self.hand = Zone("Mano")
        self.graveyard = Graveyard()
        self.exile = Exile()
        self.gold_reserve = GoldReserve()
        self.paid_gold_zone = PaidGoldZone()
        self.support_line = SupportLine()
        self.defense_line = DefenseLine()
        self.attack_line = AttackLine()

    def draw_cards(self, amount):
        drawn = 0
        for _ in range(amount):
            card = self.deck.draw()
            if card is None:
                print(f"{self.name} no puede robar porque no tiene cartas en el mazo.")
                break
            self.hand.add(card)
            drawn += 1
        return drawn

    def discard_to_hand_limit(self, limit):
        discarded = []
        while len(self.hand.cards) > limit:
            card = self.hand.cards[0]
            self.hand.move_to(card, self.graveyard)
            discarded.append(card)
        return discarded


class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.actual_turn = 1
        self.actual_phase = 1
        self.active_player_index = 0
        self.some_card_play_vigil = False
        self.played_card_this_vigil = False
        self.played_gold_this_turn = False
        self.hand_limit = 8
        self.game_over = False
        self.winner = None
        self.loser = None
        self.locks = {}
        self.ability_system = AbilitySystem(self)

    @property
    def active_player(self):
        return self.players[self.active_player_index]

    @property
    def defender_player(self):
        return self.players[1 - self.active_player_index]

    def draw_starting_hands(self, amount=8):
        for player in self.players:
            player.draw_cards(amount)

    def setup_initial_gold(self):
        for player in self.players:
            initial_gold = next((card for card in player.deck.cards if card.type == 0), None)
            if initial_gold is None:
                print(f"{player.name} no tiene oro inicial disponible.")
                continue
            player.deck.move_to(initial_gold, player.gold_reserve)
            initial_gold.controller = player
            print(f"{player.name} comienza con {initial_gold.name} como oro inicial.")

    def regroup_phase(self):
        player = self.active_player
        player.attack_line.regroup(player.defense_line)
        player.paid_gold_zone.regroup(player.gold_reserve)
        self.actual_phase = 1

    def play_card_from_hand(self, card):
        if self.game_over:
            print("La partida ya terminó.")
            return False

        player = self.active_player
        if card not in player.hand.cards:
            print("Esta carta no está en la mano.")
            return False

        if card.type == 0:
            if self.played_gold_this_turn:
                print("Ya jugaste un oro este turno.")
                return False
            if self.played_card_this_vigil:
                print("El oro debe ser la primera carta que juegas en la vigilia.")
                return False
            player.hand.move_to(card, player.gold_reserve)
            card.controller = player
            self.some_card_play_vigil = True
            self.played_card_this_vigil = True
            self.played_gold_this_turn = True
            print(f"{player.name} juega {card.name} en la reserva de oros.")
            return True

        if not player.gold_reserve.pay(card, player.paid_gold_zone):
            return False

        card.controller = player
        self.played_card_this_vigil = True

        if card.type == 1:
            player.hand.move_to(card, player.defense_line)
            card.enter_turn = self.actual_turn
            print(f"{player.name} juega {card.name} en la línea de defensa.")
            self.ability_system.resolve(card, "on_enter_play", player)
            return True

        if card.type in (2, 3):
            player.hand.move_to(card, player.support_line)
            print(f"{player.name} juega {card.name} en la línea de apoyo.")
            self.ability_system.resolve(card, "on_enter_play", player)
            return True

        if card.type == 4:
            player.hand.move_to(card, player.graveyard)
            print(f"{player.name} juega {card.name}.")
            self.ability_system.resolve(card, "on_play", player)
            return True

        player.hand.move_to(card, player.support_line)
        print(f"{player.name} juega {card.name}.")
        self.ability_system.resolve(card, "on_play", player)
        return True

    def play_card_hand(self, card):
        return self.play_card_from_hand(card)

    def statement_attack(self, allies):
        player = self.active_player
        for ally in allies:
            if ally.enter_turn == self.actual_turn:
                print("Este aliado no puede atacar porque entró este turno.")
                continue
            if not ally.can_attack:
                print(f"{ally.name} no puede atacar.")
                continue
            player.defense_line.move_to(ally, player.attack_line)

    def declare_blocks(self, locks):
        defender = self.defender_player
        player = self.active_player
        for attacker, blocker in locks.items():
            if attacker not in player.attack_line.cards:
                print(f"{attacker.name} no está atacando.")
                return False
            if blocker not in defender.defense_line.cards:
                print(f"{blocker.name} no está en la línea de defensa.")
                return False
            if not blocker.can_defense:
                print(f"{blocker.name} no puede defender.")
                return False
        self.locks = locks
        return True

    def destroy_card(self, card):
        player = card.controller
        if player is None:
            return False

        for zone in (player.attack_line, player.defense_line, player.support_line):
            if card in zone.cards:
                zone.move_to(card, player.graveyard)
                return True
        return False

    def damage_assignment(self):
        if self.game_over:
            return

        for attacker, blocker in self.locks.items():
            if attacker.strength > blocker.strength:
                self.destroy_card(blocker)
                damage = attacker.strength - blocker.strength
                self.defender_player.deck.take_damage(self.defender_player.graveyard, damage)
                self.check_deck_loss(self.defender_player)
            elif attacker.strength < blocker.strength:
                self.destroy_card(attacker)
            else:
                self.destroy_card(attacker)
                self.destroy_card(blocker)

    def final_draw(self):
        if self.game_over:
            print("La partida ya terminó.")
            return

        self.active_player.draw_cards(1)
        self.check_deck_loss(self.active_player)
        if self.game_over:
            return

        discarded = self.active_player.discard_to_hand_limit(self.hand_limit)
        for card in discarded:
            print(f"{self.active_player.name} descarta {card.name} por limite de mano.")
        self.actual_turn += 1
        self.locks = {}
        self.active_player_index = 1 - self.active_player_index
        self.some_card_play_vigil = False
        self.played_card_this_vigil = False
        self.played_gold_this_turn = False
        self.actual_phase = 0

    def check_deck_loss(self, player):
        if self.game_over or player.deck.cards:
            return False

        self.game_over = True
        self.loser = player
        self.winner = self.get_opponent(player)
        print(f"{player.name} se quedó sin cartas en el Castillo y pierde la partida.")
        print(f"{self.winner.name} gana la partida.")
        return True

    def move_card(self, card, origin_zone, destination_zone):
        return origin_zone.move_to(card, destination_zone)

    def get_opponent(self, player):
        return self.players[1] if self.players[0] == player else self.players[0]


def card_classes():
    return {"Card": Card, "Ally": Ally, "Gold": Gold}


def build_game():
    base_dir = Path(__file__).resolve().parent
    database = load_card_database(base_dir / "card.json")

    player1 = Player("Jugador 1")
    player2 = Player("Jugador 2")

    player1.deck.cards = load_deck(base_dir / "deck_player1.json", database, card_classes())
    player2.deck.cards = load_deck(base_dir / "deck_player2.json", database, card_classes())

    game = Game(player1, player2)
    game.setup_initial_gold()
    player1.deck.shuffle_deck()
    player2.deck.shuffle_deck()
    game.draw_starting_hands(8)
    return game


def format_card(card):
    details = f"{card.name} [{card.type_name}]"
    if card.cost:
        details += f" coste {card.cost}"
    if isinstance(card, Ally):
        details += f" fuerza {card.strength}"
    if card.text:
        details += f" - {card.text}"
    return details


def show_board(player):
    print(f"\n{player.name}")
    print(f"Mazo: {len(player.deck.cards)} | Mano: {len(player.hand.cards)} | Cementerio: {len(player.graveyard.cards)}")
    print(f"Oros disponibles: {len(player.gold_reserve.cards)} | Oros pagados: {len(player.paid_gold_zone.cards)}")
    print(f"Defensa: {player.defense_line.short_list()}")
    print(f"Ataque: {player.attack_line.short_list()}")
    print(f"Apoyo: {player.support_line.short_list()}")


def choose_card_from_hand(player):
    if not player.hand.cards:
        print("No tienes cartas en la mano.")
        return None

    print("\nMano:")
    for index, card in enumerate(player.hand.cards, start=1):
        print(f"{index}. {format_card(card)}")

    choice = input("Elige una carta para jugar, o Enter para pasar: ").strip()
    if not choice:
        return None
    if not choice.isdigit():
        print("Opción inválida.")
        return None

    index = int(choice) - 1
    if index < 0 or index >= len(player.hand.cards):
        print("Opción fuera de rango.")
        return None
    return player.hand.cards[index]


def run_console_game():
    game = build_game()
    print("Juego iniciado. Cada jugador parte con 8 cartas en la mano.")

    while True:
        player = game.active_player
        opponent = game.defender_player

        game.regroup_phase()
        print(f"\nTurno {game.actual_turn}: juega {player.name}")
        show_board(player)
        show_board(opponent)

        while True:
            card = choose_card_from_hand(player)
            if card is None:
                break
            game.play_card_from_hand(card)
            show_board(player)

        command = input("\nEnter para terminar turno, 'q' para salir: ").strip().lower()
        if command == "q":
            break
        game.final_draw()

    print("Partida terminada.")


if __name__ == "__main__":
    if "--console" in sys.argv:
        run_console_game()
    else:
        from gui import run_gui

        run_gui()
