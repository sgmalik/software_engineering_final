from Card import Card
import random

class Deck:
    SUITS = ['H', 'D', 'C', 'S']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self):
        self.cards: list[Card] = [Card(suit, card_val) for suit in Deck.SUITS for card_val in Deck.RANKS]
        self.shuffle()

    def draw_card(self):
        return self.cards.pop()
    
    def draw_cards(self, num_cards):
        return [self.cards.pop() for _ in range(num_cards)]
        
    def shuffle(self):
       random.shuffle(self.cards)

    def restore(self):
        new_deck = Deck()
        self.cards = new_deck.cards

    #descending order 
    @staticmethod
    def sort_cards_by_rank(cards: list[Card]):
         return sorted(cards, key=lambda card: card.get_card_rank(), reverse=True)

   