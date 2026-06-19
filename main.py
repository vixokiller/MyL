from cards import Ally, Gold, Talisman, Totem, Weapon
from player import Player
from game import Game, Phase

jugador1 = Player("Jugador1")
jugador2 = Player("Jugador2")

juego = Game(jugador1, jugador2)

oro = Gold("Copihue")
oro2 = Gold("Araucaria")
zeus = Ally("Zeus", 2, 2)
espada = Weapon("Espada de Rayo", 1, 2)
totem = Totem("Tótem de Guerra", 1)

for card in [oro, oro2, zeus, espada, totem]:
    card.owner = jugador1
    card.controller = jugador1
    jugador1.hand.add_card(card)
    
print("Mano inicial:", jugador1.hand.show_cards())

juego.grouping_phase()

juego.play_card_from_hand(oro)
juego.play_card_from_hand(zeus)
juego.play_card_from_hand(espada, zeus)


print("Reserva de Oros:", jugador1.reserveGold.show_cards())
print("Línea de Defensa:", jugador1.defenseLine.show_cards())
print("Zona de Oro pagado:", jugador1.paidGoldZone.show_cards())
print("Armas de Zeus:", zeus.annexes)
print("Fuerza total:", zeus.total_strength)