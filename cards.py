from enum import Enum, auto

class CardType(Enum):
    ORO = auto()
    ALIADO = auto()
    TALISMAN = auto()
    TOTEM = auto()
    ARMA = auto()
    
class Card:
    def __init__(self, name, type, cost=0, ability=None,):
        self.name = name
        self.type = type
        self.cost = cost
        self.ability = ability
        self.owner = None
        self.controller = None

    def __repr__(self):
        return self.name

class Gold(Card):
    def __init__(self, name):
        super().__init__(name, CardType.ORO, cost=0)

class Ally(Card):
    def __init__(self, name, cost, strength,):
        super().__init__(name, CardType.ALIADO, cost)
        self.base_strength = strength
        self.annexes = []
        self.weapon_limit = 1
        self.came_on_field = 0
        self.can_attack = True
        self.can_block = True
                
    def annexed_weapons(self):
        return [card for card in self.annexes if card.type == CardType.ARMA]
    
    def can_annex_weapon(self):
        return len(self.annexed_weapons()) < self.weapon_limit
    
    def annex_weapon(self, weapon):
        if weapon.type != CardType.ARMA:
            print("Esta carta no es un Arma.")
            return False
        if not self.can_annex_weapon():
            print(f"{self.name} ya tiene el máximo de Armas anexadas.")
            return False
        self.annexes.append(weapon)
        return True
    
    @property
    def total_strength(self):
        total = self.base_strength
        for card in self.annexes:
            if card.type == CardType.ARMA:
                total += card.strength_bonus
        return total

class Talisman(Card):
    def __init__(self, name, cost):
        super().__init__(name, CardType.TALISMAN, cost)
        
    def play(self, player):
        print(f"{player.name} juega {self.name}")
        
        player.hand.remove_card(self)
        player.graveyard.add_card(self)
    
class Totem(Card):
    def __init__(self, name, cost):
        super().__init__(name, CardType.TOTEM, cost)

class Weapon(Card):
    def __init__(self, name, cost, strength_bonus):
        super().__init__(name, CardType.ARMA, cost)
        self.strength_bonus = strength_bonus