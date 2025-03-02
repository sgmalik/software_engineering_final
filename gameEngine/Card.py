class Card: 
    
    def __init__(self, suit: str, card_rank: str):
        assert(len(suit) == 1)
        assert(len(card_rank) == 1)

        self.suit = suit
        self.card_rank = card_rank

    def __str__(self):
        return f"{self.value} of {self.suit}"

    def __repr__(self):
        return f"{self.value} of {self.suit}"