from Card import Card
import random

class Deck:
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self):
        self.deck: list[Card] = [Card(suit, card_rank) for suit in Deck.SUITS for card_rank in Deck.RANKS]
        Deck.shuffle(self.deck)

    def draw_card(self):
        return self.deck.pop()
    
    def draw_cards(self, num_cards):
        return [self.deck.pop() for _ in range(num_cards)]
    
    @staticmethod
    def sort_cards_by_rank(cards: list[Card]):
         return sorted(cards, key=lambda card: card.get_card_rank())
        
    def shuffle(self):
       random.shuffle(self.deck)

    def restore(self):
        self.deck = Deck()

   