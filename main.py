import random

class Card:
    def __init__(self, name, cost=None):
        self.name = name
        self.cost = cost
        
    def __str__(self):
        return self.name
        
class Ally(Card):
    def __init__(self, name, cost, strenght):
        super().__init__(name, cost)
        self.strenght = strenght

class Gold(Card):
    def __init__(self, name, cost=None):
        super().__init__(name, cost)
      
def show_cards(zone):
    for card in zone:
        print(card)

def draw(zone1, zone2, amount):
    for i in range(amount):
        draw_card = zone1.pop()
        zone2.append(draw_card)

def paid(zone1, zone2, card):
    if card.cost <= len(zone1):
        for _ in range(card.cost):
            gold = zone1.pop()
            zone2.append(gold)
    else:
        print(f"No tienes suficientes Oros para jugar a '{card.name}'.")

def play_card(zone1, zone2, card):
    if isinstance(card, Ally):
        zone1.remove(card)
        zone2.append(card)
        
    elif isinstance(card, Gold):
        zone1.remove(card)
        zone2.append(card)

def regroup(zone1, zone2):
    while zone1:
        card = zone1.pop()
        zone2.append(card)
  
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


     
aliado1 = Ally("Zeus", 2, 2)
aliado2 = Ally("Apolo", 1, 1)
oro1 = Gold("Copihue")
oro2 = Gold("Aguila imperial")
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



