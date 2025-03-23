"""Test the Deck class in the Deck module."""
import random
from ..deck import Deck

class TestDeck():
    """
    test deck methods
    """
    def test_rank_sort(self):
        """
        testing rank sort by comparing sorted() to our method
        """
        deck = Deck()

        cards = random.sample(deck.cards, 10)

        ranks = [card.get_card_rank() for card in cards]
        sorted_ranks = sorted(ranks, reverse=True)

        sorted_cards = Deck.sort_cards_by_rank(cards)
        sorted_cards_ranks = [card.get_card_rank() for card in sorted_cards]
        # assert that ranks are in ascending order
        assert sorted_ranks == sorted_cards_ranks
        
        
