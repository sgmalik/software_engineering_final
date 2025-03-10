
from ..Deck import Deck
import random

class Test_Deck():
    def test_rank_sort(self):
        deck = Deck()

        cards = random.sample(deck.cards, 10)
        sorted_cards = Deck.sort_cards_by_rank(cards)
        print(sorted_cards)
