class Card:
    def __init__(self, name, cost=None):
        self.name = name
        self.cost = cost
        
    def __str__(self):
        return self.name
        
class Ally(Card):
    def __init__(self,name, cost, strenght):
        super().__init__(name, cost)
        self.strenght = strenght
        
alido1 = Ally("Zeus", 1, 2)
oro1 = Card("Copihue")
hand = [alido1, oro1]
table = []


if not oro1.cost:
    hand.remove(oro1)
    table.append(oro1)
    

