import random

class Deck:
    def __init__(self):
        self.cards = []

    def add_card(self, card, amount=1):
        """
        Agrega una o varias copias de una carta al mazo.
        """
        for _ in range(amount):
            self.cards.append(card.copy())

    def barajar(self):
        """
        Mezcla las cartas del mazo.
        """
        random.shuffle(self.cards)
    
    def draw(self):
        """
        Roba una carta del mazo.
        La carta robada se elimina del mazo.
        """
        if len(self.cards) == 0:
            print("No quedan cartas en el mazo.")
            return None

        return self.cards.pop(0)
    
    def amount_cards(self):
        return len(self.cards)
    
    def show_deck(self):
        print("===Mazo===")
        for card in self.cards:
            print(f"{card.name}")