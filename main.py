import random

class Card:
    '''
    Tipos de carta:
    Oro = 0
    Aliado = 1
    Arma = 2
    Tótem = 3
    Talismán = 4
    '''
    def __init__(self, name, type, cost=None):
        self.name = name
        self.type = type
        self.cost = cost
        self.controller = None
        
    def __repr__(self):
        return self.name
        
class Ally(Card):
    def __init__(self, name, type, cost, strenght):
        super().__init__(name, type, cost)
        self.strenght = strenght
        self.enter_turn = 0
        self.can_attack = True
        self.can_defense = True

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
        Batalla Mitológica:
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
        self.some_card_play_vigil = False
        self.locks = {}
        
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
        
    def play_card_hand(self, card):
        player = self.active_player
        if card.type == 0:
            if self.some_card_play_vigil:
                print("Ya jugaste tú primera carta.")
                return False
            player.hand.move_to(card, player.gold_reserve)
            self.some_card_play_vigil = True
            return True
        if card.type == 1:
            player.hand.move_to(card, player.defense_line)
            card.enter_turn = self.actual_turn
            return True
        return False
    
    def statement_attack(self, allys):
        player = self.active_player
        for ally in allys:
            if ally.enter_turn == self.actual_turn:
                print("Este aliado no puede atacar por qué entro este turno.")
                continue
            if ally.can_attack == False:
                print(f"{ally.name} no puede atacar.")
                continue
            player.defense_line.move_to(ally, player.attack_line)
    
    def lockers(self, attacker, blocker):
        self.lock.update({f"{attacker}":f"{blocker}"})
        
    def declare_blocks(self, locks):
        defender = self.defender_player
        player = self.active_player
        for attacker, blocker in locks:
            if attacker not in player.attack_line.cards:
                print(f"{attacker.name} no esta atacando.")
                return False
            if blocker not in defender.defense_line.cards:
                print(f"{blocker.name} no esta en la Línea de defensa.")
                return False
            if blocker.can_defense == False:
                print(f"{blocker.name} no puede defender.")
                return False
        self.locks = locks
        return True
    
    def detroy_card(self, card):
        player = card.cotroller
        zones = [player.attack_line, player.defense_line, player.support_line]
        for zone in zones:
            if card in zone.cards:
                zone.move_to(card, player.graveyard)
        
    def damage_assignment(self):
        attacker = self.active_player
        defender = self.defender_player
        
        
aliado1 = Ally("Zeus", 1, 3, 2)
aliado2 = Ally("Apolo", 1, 1, 1)
oro1 = Gold("Copihue", 0)
oro2 = Gold("Aguila imperial", 0)
jugador1 = Player("Vicente")
jugador2 = Player("Gabriel")
partida = Game(jugador1, jugador2)







