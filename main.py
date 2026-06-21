import random

class Card:
    def __init__(self, name, type, cost=None):
        self.name = name
        self.type = type
        self.cost = cost
        
    def __repr__(self):
        return self.name
        
class Ally(Card):
    def __init__(self, name, type, cost, strenght):
        super().__init__(name, type, cost)
        self.strenght = strenght

class Gold(Card):
    def __init__(self, name, type, cost=None):
        super().__init__(name, type, cost)
 
class Zone():
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
        if moved_card:
            zone.add(moved_card)        
    
    def regroup(self, zone):
        while self.cards:
            self.move_to(self.cards[0], zone)
    
    def show_cards(self):
        print(self.cards)
      
def paid(zone1, zone2, card):
    if card.cost <= len(zone1):
        for _ in range(card.cost):
            gold = zone1.pop()
            zone2.append(gold)
    else:
        print(f"No tienes suficientes Oros para jugar a '{card.name}'.")

def do_damage(zone1, zone2,  damage):
      for i in range(damage):
          x = zone1.pop()
          zone2.append(x)

def battle(attacker, defender, graveyard_attacker, graveyard_defender, deck_defender, defender_line, attacker_line):
    diference = attacker.strenght - defender.strenght
    
    if diference > 0:
        play_card(defender_line, graveyard_defender, defender)
        do_damage(deck_defender,graveyard_defender, diference)
        
    elif diference < 0:
        play_card(attacker_line, graveyard_attacker, attacker)
        
    else:
        play_card(attacker_line, graveyard_attacker, attacker)
        play_card(defender_line, graveyard_defender, defender)


     
aliado1 = Ally("Zeus", "Aliado", 2, 2)
aliado2 = Ally("Apolo", "Aliado", 1, 1)
oro1 = Gold("Copihue", "Oro")
oro2 = Gold("Aguila imperial", "Oro")
mazo = [aliado1, oro1 ,oro2]
mazo2 = [aliado2, oro1 ,oro2]
random.shuffle(mazo)
gold_reserve = []
paid_gold_zone = []
hand = []
defense_line = [aliado2]
attack_line = [aliado1]
graveyard1 = []
graveyard2 = []



