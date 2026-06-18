from enum import Enum
import random

class CardType(Enum):
    ALIADO = "Aliado"
    ORO = "Oro"
    TOTEM = "Totem"
    TALISMAN = "Talisman"
    ARMA = "Arma"

class Card:
    def __init__(self, name, type, cost, ability=None, strength=None):
        self.name = name
        self.type = type
        self.cost = cost
        self.ability = ability
        self.strength = strength

    def __repr__(self):
        return self.name
    
class Player:
    def __init__(self, name):
        self.name = name
        self.deck = []
        self.hand = []

Player1 = Player("Player 1")
Player2 = Player("Player 2")

def cheackWinCondition(player1, player2):
    if not player1.deck:
        print("Player 2 wins!")
    elif not player2.deck:
        print("Player 1 wins!")

def drawCard(numberOfCards, player):
    for i in range(numberOfCards):
        card = player.deck.pop(0)
        player.hand.append(card)

def damageDeck(numberOfCards, player):
    for i in range(numberOfCards):
        if player.deck:
            player.deck.pop(0)
        else:
            cheackWinCondition(Player1, Player2)
            break

def showCards(player):
    print(f"{player.name}'s Hand:")
    for card in player.hand:
        print(f"Name: {card.name}, Cost: {card.cost}, Ability: {card.ability}, Strength: {getattr(card, 'strength', 'N/A')}")
        
showCards(Player1)