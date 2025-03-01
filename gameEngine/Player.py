from Deck import Deck

class Player:
    def __init__(self, initial_stack):
        self.hole_card = []
        self.stack = initial_stack


    def draw_card(self, deck: Deck):
        self.hole_card.append(deck.draw())
