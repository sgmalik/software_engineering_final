"""
Card class
"""

class Card:
    """
    represents a card with suit and value
    has overloaded operators to compare cards in game_evaluator, and hand_evaluator
    """
    CARD_RANK_MAP = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '10': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14,
    }

    def __init__(self, suit: str, card_val: str):
        assert len(suit) == 1

        self.suit = suit
        self.card_val = card_val

    # overloading operators

    def __eq__(self, other_card):
        if isinstance(other_card, Card):
            return self.suit == other_card.suit and self.card_val == other_card.card_val
        return False

    def __lt__(self, other_card):
        pass

    def __gt__(self, other_card):
        pass

    def __ge__(self, other_card):
        pass

    def __le__(self, other_card):
        pass

    # debug prints

    def __str__(self):
        return f"{self.card_val}{self.suit}"

    def __repr__(self):
        return f"{self.suit}{self.card_val}"

    # methods

    def get_card_rank(self) -> int:
        """
        returns the rank of the card based on rank map
        """
        assert self.card_val in self.CARD_RANK_MAP
        return self.CARD_RANK_MAP[self.card_val]

