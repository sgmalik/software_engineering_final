"""
Deck of 52 Cards
"""

import random
from .card import Card



class Deck:
    """
    Represents a deck of Cards, shuffles on init
    """
    SUITS = ['H', 'D', 'C', 'S']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self):
        self.cards: list[Card] = [Card(suit, card_val)
                                  for suit in Deck.SUITS for card_val in Deck.RANKS]
        self.shuffle()

    def draw_card(self):
        """
        takes and returns a card from self.cards
        """
        return self.cards.pop()

    def draw_cards(self, num_cards):
        """
        draws num_cards from self.cards
        """
        return [self.cards.pop() for _ in range(num_cards)]

    def shuffle(self):
        """
        shuffles deck using random module
        """
        random.shuffle(self.cards)

    def restore(self):
        """
        reset the deck to a new deck of cards
        """
        new_deck = Deck()
        self.cards = new_deck.cards

    @staticmethod
    def sort_cards_by_rank(cards: list[Card]) -> list[Card]:
        """
        returns sorted cards by rank (see card) by descending order
        """
        return sorted(cards, key=lambda card: card.get_card_rank(), reverse=True)
