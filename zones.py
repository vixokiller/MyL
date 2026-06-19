import random
from cards import CardType

class Zone:
    def __init__(self, name):
        self.name = name
        self.cards = []
        
    def add_card(self, card):
        self.cards.append(card)
    
    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)
            return card
        return None
    
    def move_to(self, card, target_zone):
        moved_card = self.remove_card(card)
        if moved_card:
            target_zone.add_card(moved_card)
    
    def show_cards(self):
        return self.cards
    
class Deck(Zone):
    def __init__(self):
        super().__init__("Castillo")
        
    def shuffle(self):
        random.shuffle(self.cards)
        
    def draw(self):
        if self.cards:
            return self.cards.pop(0)
        return None
        
class graveyard(Zone):
    def __init__(self):
        super().__init__("Cementerio")
        
class removePile(Zone):
    def __init__(self):
        super().__init__("Zona de Destierro")
        
class reserveGold(Zone):
    def __init__(self):
        super().__init__("Reserva de Oros")
        
    def add_gold(self, card):
        if card.type == CardType.ORO:
            self.add_card(card)
        else:
            print("Solo se pueden jugar oros en la Reserva de Oros.")

class paidGoldZone(Zone):
    def __init__(self):
        super().__init__("Zona de Oro Pagado")
    
class supportLine(Zone):
    def __init__(self):
        super().__init__("Linea de Apoyo")
        
    def add_cards(self, card):
        if card.type == CardType.TOTEM:
            self.add_card(card)
        else:
            print("Solo se pueden jugar Totems en la Linea de Apoyo.")
            
class defenseLine(Zone):
    def __init__(self):
        super().__init__("Linea de Defensa")
        
    def add_cards(self, card):
        if card.type == CardType.ALIADO:
            self.add_card(card)
        else:
            print("Solo se pueden jugar Aliados en la Linea de Defensa.")

class attackLine(Zone):
    def __init__(self):
        super().__init__("Linea de Ataque")
        
    def add_cards(self, card):
        if card.type == CardType.ALIADO:
            card.can_block = False
            self.card.append(card)
        else:
            print("Solo los Aliados pueden ir en la Linea de Ataque.")