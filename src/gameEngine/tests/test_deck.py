
from ..Deck import Deck
import random

class Test_Deck():
    def test_rank_sort(self):
        deck = Deck()

        cards = random.sample(deck.cards, 10)

        ranks = [card.get_card_rank() for card in cards]
        sorted_ranks = sorted(ranks, reverse=True)

        sorted_cards = Deck.sort_cards_by_rank(cards)
        sorted_cards_ranks = [card.get_card_rank() for card in sorted_cards]
        
        assert sorted_ranks == sorted_cards_ranks
        # assert that ranks are in ascending order
        
