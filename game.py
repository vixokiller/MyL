from enum import Enum, auto
from cards import CardType

class Phase(Enum):
    AGRUPACION = auto()
    VIGILIA = auto()
    DECLARACION_ATAQUE = auto()
    DECLARACION_BLOQUEO = auto()
    GUERRA_TALISMANES = auto()
    ASIGNACION_DAÑO = auto()
    FINAL = auto()
    ROBAR = auto()

class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.actual_turn = 1
        self.active_player_index = 0
        self.actual_phase = Phase.AGRUPACION
        self.gold_played_first_card = False
        self.some_card_played_vigil = False
        
    @property
    def active_player(self):
        return self.players[self.active_player_index]
    
    @property
    def defending_player(self):
        return self.players[1 - self.active_player_index]
    
    def grouping_phase(self):
        player = self.active_player
        
        ally_to_move = list(player.attackLine.cards)
        
        for ally in ally_to_move:
            player.attackLine.move_to(ally, player.defenseLine)
            
        gold_to_move = list(player.paidGoldZone.cards)
        
        for gold in gold_to_move:
            player.paidGoldZone.move_to(gold, player.reserveGold)
            
        print("Fase de Agrupación terminada.")
        self.actual_phase = Phase.VIGILIA
        
    def play_card_from_hand(self, card, objetive=None):
        player = self.active_player
        if card not in player.hand.cards:
            print("La carta no esta en la mano.")
            return False
        
        if self.actual_phase != Phase.VIGILIA:
            print("Solo se pueden jugar cartas en la fase de Vigilia.")
            return False
        
        if card.type == CardType.ORO:
            if self.some_card_played_vigil:
                print("No puedes jugar un Oro después de haber jugado otra carta en esta fase.")
                return False
            player.hand.move_to(card, player.reserveGold)
            self.gold_played_first_card = True
            self.some_card_played_vigil = True
            return True
        
        if not self.pay_cost(player, card.cost):
            return False
        
        self.some_card_played_vigil = True
        
        if card.type == CardType.ALIADO:
            player.hand.move_to(card, player.defenseLine)
            card.came_on_field = self.actual_turn
            return True
        
        if card.type == CardType.TOTEM:
            player.hand.move_to(card, player.supportLine)
            return True
        
        if card.type == CardType.ARMA:
            if objetive is None:
                print("Debes elegir un aliado para anexar el arma.")
                return False
            
            if objetive not in player.defenseLine.cards:
                print("El arma debe anexarse a un aliado en juego.")
                return False
            
            if objetive.annex_weapon(card):
                player.hand.remove_card(card)
                return True
            
        return False
    
    def declare_attack(self, allys):
        player = self.active_player
        
        if self.actual_phase != Phase.DECLARACION_ATAQUE:
            print("No estás en Declaración de Ataque.")
            return False
        
        for ally in allys:
            if ally not in player.defenseLine.cards:
                print(f"{ally.name} no está en la Línea de Defensa.")
                continue
            
            if ally.came_on_field == self.actual_turn:
                print(f"{ally.name} no puede atacar este turno porque acaba de entrar en juego.")
                continue
            
            if not ally.can_attack:
                print(f"{ally.name} no puede atacar este turno.")
                continue
            
            player.defenseLine.move_to(ally, player.attackLine)
            
            self.actual_phase = Phase.DECLARACION_BLOQUEO
            return True
        
    def declare_block(self, blocks):
        defender = self.defending_player
        
        if self.actual_phase != Phase.DECLARACION_BLOQUEO:
            print("No estás en Declaración de Bloqueo.")
            return False
        
        for attacker, blocker in blocks.items():
            if attacker not in self.active_player.attackLine.cards:
                print(f"{attacker.name} no está atacando.")
                return False
            
            if blocker not in defender.defenseLine.cards:
                print(f"{blocker.name} no está en la Línea de Defensa.")
                return False
            
            if not blocker.can_block:
                print(f"{blocker.name} no puede bloquear este turno.")
                return False
        
        self.blocks = blocks
        self.actual_phase = Phase.GUERRA_TALISMANES
        return True
    
    def talisman_war(self):
        print("Comienza la Guerra de Talismanes.")
        print("Los jugadores pueden jugar talismanes o habilidades.")
        
        self.actual_phase = Phase.ASIGNACION_DAÑO
        
    def assign_damage(self):
        attacker = self.active_player
        defender = self.defending_player
        
        cards_to_destroy= []
        damage_deck = 0
        
        for attacking_ally in attacker.attackLine.cards:
            blocker = self.declare_block.get(attacking_ally)
            
            if blocker:
                strength_a = attacking_ally.total_strength
                strength_b = blocker.total_strength

                if strength_a > strength_b:
                    cards_to_destroy.append(blocker)
                    damage_deck += strength_a - strength_b
                
                elif strength_a == strength_b:
                    cards_to_destroy.append(attacking_ally)
                    cards_to_destroy.append(blocker)
                    
                else:
                    cards_to_destroy.append(attacking_ally)
            
            else:
                damage_deck += attacking_ally.total_strength
                
        for card in cards_to_destroy:
            self.destroy_card(card)
        
        self.damage_deck(defender, damage_deck)
        
        self.actual_phase = Phase.FINAL
        
    def destroy_card(self, card):
        player = card.controller
        
        zones = [player.attackLine, player.defenseLine, player.supportLine]
        
        for zone in zones:
            if card in zone.cards:
                zone.move_to(card, player.graveyard)
                print(f"{card.name} ha sido destruida.")
                return
            
    def damage_deck(self, player, damage):
        for _ in range(damage):
            card = player.deck.draw()
            
            if card:
                player.graveyard.add_card(card)
                print(f"{card.name} fue enviada al cementerio por el daño de mazo.")
            else:
                print(f"{player.name} no tiene más cartas en el mazo para recibir daño.")
    
    def final_phase(self):
         print("Terminan los efectos temporales del turno.")
         
         self.blocks = {}
         self.actual_phase = Phase.ROBAR
         
    def draw_phase(self):
        player = self.active_player
        
        draw_card = player.deck.draw()
        
        if draw_card:
            player.hand.add_card(draw_card)
            print(f"{player.name} roba {draw_card.name}")
        
        while len(player.hand.cards) > 8:
            discared_card = player.hand.cards[0]
            player.hand.move_to(discared_card, player.graveyard)
            print(f"{player.name} descarta {discared_card.name}")
        
        self.end_turn()
        
    def end_turn(self):
        self.active_player_index = 1 - self.active_player_index
        self.actual_turn += 1
        self.actual_phase = Phase.AGRUPACION
        
        self.gold_played_first_card = False
        self.some_card_played_vigil = False
        self.blocks = {}
        
        print("Termina el turno.")
        
    def can_pay(self, player, cost):
        return len(player.reserveGold.cards) >= cost
    
    def pay_cost(self, player, cost):
        if cost == 0:
            return True
        
        if not self.can_pay(player, cost):
            print(f"No tienes suficiente oro. Necesitas {cost}.")
            return False
        
        for _ in range(cost):
            gold = player.reserveGold.cards[0]
            player.reserveGold.move_to(gold, player.paidGoldZone)
            
        print(f"{player.name} pagó {cost} oro.")
        return True
        