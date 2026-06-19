from zones import (Zone, Deck, graveyard, removePile, reserveGold, paidGoldZone, supportLine, defenseLine, attackLine)

class Player:
    def __init__(self, name):
        self.name = name
        self.deck = Deck()
        self.graveyard = graveyard()
        self.removePile = removePile()
        self.reserveGold = reserveGold()
        self.paidGoldZone = paidGoldZone()
        self.supportLine = supportLine()
        self.defenseLine = defenseLine()
        self.attackLine = attackLine()
        self.hand = Zone("Mano")