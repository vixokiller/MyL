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

def paid(gold_reserve, paid_gold_zone, card):
    for _ in range(card.cost):
        gold = gold_reserve.pop()
        paid_gold_zone.append(gold)
    show_cards(paid_gold_zone)
    
def play_card(hand, zone, card):
    if isinstance(card, Ally):
        hand.remove(card)
        zone.append(card)
        show_cards(zone)
        
    elif isinstance(card, Gold):
        hand.remove(card)
        zone.append(card)
        show_cards(zone)
         
aliado1 = Ally("Zeus", 2, 2)
oro1 = Gold("Copihue")
oro2 = Gold("Aguila imperial")
gold_reserve = []
paid_gold_zone = []
hand = [aliado1, oro1, oro2]
defense_line = []
play_card(hand, gold_reserve, oro1)
play_card(hand, gold_reserve, oro2)
paid(gold_reserve, paid_gold_zone, aliado1)




