from Card import Card
from Deck import Deck


"""
HandEvaluator will provide information about the strength of a players hand
"""


class HandEvaluator():
    # these are the cards that make up the strength Ex. two pair = ["3S", "3C", "4S", "4D"]
    _strength_cards = []

    # these are the highest cards (in a 5 card hand) that aren't used to make up the strength
    _kicker_cards = []

    _primary_cards = []

    # can make this an enum
    STRENGTH_MAP = {
        "royal_flush": 10,
        "straight_flush": 9,
        "full_house": 8,
        "flush": 7,
        "four_of_a_kind": 6,
        "straight": 5,
        "three_of_a_kind": 4,
        "two_pair": 3,
        "pair": 2,
        "high_card": 1,
    }

    """
    Evalute hand returns the strength of the hand and the kickers
    (Kickers will be used for tie breaking in GameEvaluator)

    Its input could be the cards: 
        hole_cards = "3S, 7H"
        community_cards = "5C, 5D, 6D, 3S, 2S"

    its output will look like this:
    {
        "strength": {
            "hand_rank": TWO_PAIR,
            "primary_cards_rank": [5, 3]
        },
        "kickers": [7]
    }

    NOTE: primary_cards are the cards that make up the hand rank (in this case, the pairs)
    
    """

    @classmethod
    def hand_eval(self, hole_cards, community_cards):

        

        sorted_cards = Deck.sort_cards_by_rank(hole_cards + community_cards)
        hand_rank: str = ""

        if self._is_royal_flush(sorted_cards):
            pass
        elif self._is_straight_flush(sorted_cards):
            pass
        elif self._is_four_of_a_kind(sorted_cards):
            pass
        elif self._is_full_house(sorted_cards):
            pass
        elif self._is_four_of_a_kind(sorted_cards):
            pass
        elif self._is_straight(sorted_cards):
            pass
        elif self._is_three_of_a_kind(sorted_cards):
            pass
        elif self._is_two_pair(sorted_cards):
            pass
        elif self._is_pair(sorted_cards):
            pass
        else:
            # highcard
            self._highest_five(sorted_cards)
            hand_rank = self.STRENGTH_MAP["high_card"]

        self._set_kickers(sorted_cards)

        return {
            "strength": {
                "hand_rank": hand_rank,
                "primary_cards_rank": self._primary_cards
            },
            "kickers": self._kickers
        }

        

    # get best 5 card hand
    @classmethod
    def _best_hand(self, hole_cards, community_cards):
        pass

    
    #gets the kickers based on the cards used to make up hand rank
    @classmethod
    def _set_kickers(self, sorted_cards):
        assert (len(self._strength_cards) > 0)

        kickers = [
            card for card in sorted_cards if card not in self._strength_cards]
        
        kickers_amount: int = 5 - len(self._strength_cards)
        self._kicker_cards = kickers[0:kickers_amount]  

    # strength of hand (calliing _is_)
    @classmethod
    def _calc_hand_strength(self, sorted_cards):
        pass

    # functions to check for hand rank (used in _calc_hand_strength)
    # return cards that make, empty array is falsy
    # these will update strength_cards

    @classmethod
    def _is_royal_flush(self, sorted_cards):
        pass

    @classmethod
    def _is_straight_flush(self, sorted_cards):
        pass

    @classmethod
    def _is_four_of_a_kind(self, sorted_cards):
        pass

    @classmethod
    def _is_full_house(self, sorted_cards):
        pass

    @classmethod
    def _is_flush(self, sorted_cards):
        pass

    @classmethod
    def _is_straight(self, sorted_cards):
        pass

    @classmethod
    def _is_three_of_a_kind(self, sorted_cards):
        pass

    @classmethod
    def _is_two_pair(self, sorted_cards):
        pass

    @classmethod
    def _is_pair(self, sorted_cards):
        pass

    @classmethod
    def _highest_five(self, sorted_cards):
        self._strength_cards = sorted_cards[0:5]
        self._primary_cards = self._strength_cards
