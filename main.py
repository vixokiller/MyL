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
 
class Zone:
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
      
    def paid1(self, card, zone):
        if card.cost <= len(self.cards):
            for _ in range(card.cost):
                self.move_to(self.cards[0], zone)
        else:
            print(f"No tienes suficientes Oros para jugar a '{card.name}'.")
    
    def do_damage(self, zone, damage):
        for _ in range(damage):
            self.move_to(self.cards[0], zone)
            
class Deck(Zone):
    def __init__(self):
        super().__init__("Mazo")
    
    def shuffle_deck(self):
        random.shuffle(self.cards)
        
    def draw(self):
        if self.cards:
            return self.cards.pop()
        return None
    
class Graveyard(Zone):
    def __init__(self):
        super().__init__("Cementerio")
    
class Exile(Zone):
    def __init__(self):
        super().__init__("Destierro")
        
class GoldReserve(Zone):
    def __init__(self):
        super().__init__("Reserva de oros")
        
class PAidGoldZone(Zone):
    def __init__(self):
        super().__init__("Zona de oro pagado")
        
class SupportLine(Zone):
    def __init__(self):
        super().__init__("Línea de apoyo")

class DefenseLine(Zone):
    def __init__(self):
        super().__init__("Línea de defensa")

class AttackLine(Zone):
    def __init__(self):
        super().__init__("Línea de ataque")

class Player:
    def __init__(self, name):
        self.name = name
        self.deck = Deck()
        self.hand = Zone("Mano")
        self.graveyard = Graveyard()
        self.exile = Exile()
        self.gold_reserve = GoldReserve()
        self.paid_gold_zone = PAidGoldZone()
        self.support_line = SupportLine()
        self.defense_line = DefenseLine()
        self.attack_line = AttackLine()

class Game:
    '''
    Turno
        Agrupación = 0
        Vigilia = 1
        Batalla Mitológica
            Declaración de Ataque = 2
            Declaración de Bloqueo = 3
            Guerra de Talismanes = 4
            Asignación de Daño = 5
        Final = 6
        Robar = 7
    '''
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.actual_turn = 1
        self.actual_phase = 0
        self.active_player_index = 0
        
    @property
    def active_player(self):
        return self.players[self.active_player_index]
    
    @property
    def defender_player(self):
        return self.players[1 - self.active_player_index]
           
    def regroup_phase(self):
        player = self.active_player
        player.attack_line.regroup(player.defense_line)
        player.paid_reserve_gold.regroup(player.gold_reserve)
    
aliado1 = Ally("Zeus", "Aliado", 3, 2)
aliado2 = Ally("Apolo", "Aliado", 1, 1)
oro1 = Gold("Copihue", "Oro")
oro2 = Gold("Aguila imperial", "Oro")
jugador1 = Player("Vicente")
jugador2 = Player("Gabriel")
partida = Game(jugador1, jugador2)



