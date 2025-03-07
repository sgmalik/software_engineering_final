class Card: 
    CARD_RANK_MAP = {
      2  :  '2',
      3  :  '3',
      4  :  '4',
      5  :  '5',
      6  :  '6',
      7  :  '7',
      8  :  '8',
      9  :  '9',
      10 : 'T',
      11 : 'J',
      12 : 'Q',
      13 : 'K',
      14 : 'A'
    }

    def __init__(self, suit: str, card_val: str):
        assert(len(suit) == 1)
        assert(len(card_val) == 1)

        self.suit = suit
        self.card_val = card_val

    def get_card_rank(self) -> int:
        assert(self.card_val in self.CARD_RANK_MAP.values())
        return self.CARD_RANK_MAP[self.card_val]

    def __str__(self):
        return f"{self.card_val} of {self.suit}"

    def __repr__(self):
        return f"{self.card_val} of {self.suit}"