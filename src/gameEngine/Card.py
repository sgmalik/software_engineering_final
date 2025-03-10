class Card:
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
        assert (len(suit) == 1)

        self.suit = suit
        self.card_val = card_val

    def get_card_rank(self) -> int:
        assert (self.card_val in self.CARD_RANK_MAP)
        return self.CARD_RANK_MAP[self.card_val]

    def __str__(self):
        return f"{self.card_val} of {self.suit}"

    def __repr__(self):
        return f"{self.card_val} of {self.suit}"
