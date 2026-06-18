class Card:
    def __init__(self, name, cost, ability=None):
        self.name = name
        self.cost = cost
        self.ability = ability

class Aliado(Card):
    def __init__(self, name, cost, ability=None, strength=0):
        super().__init__(name, cost, ability)
        self.strength = strength

Zeus = Aliado("Zeus", 5, "Thunder Strike", 10)

class Player:
    def __init__(self, name):
        self.name = name
        self.deck = [Zeus]
        self.hand = [Zeus]

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