
"""
    HandEvaluator will take in the hole cards and community 
    cards and return the strength of the hand
"""

from .deck import Deck


class HandEvaluator():

    """
        Evalute hand returns the strength of the hand and the kickers
        (Kickers will be used for tie breaking in GameEvaluator)

        Its input could be the cards: 
            hole_cards = "3S, 7H"
            community_cards = "5C, 5D, 6D, 3S, 2S"

        its output will look like this:
        {
            "strength": {
                "hand_rank": TWO_PAIR (which would be strength = 3),
                "primary_cards_rank": [5, 3]
            },
            "kickers": [7]
        }

        NOTE: primary_cards are the cards that make up the hand rank (in this case, the pairs)

    """

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

    def __init__(self):
        # these are the cards that make up the strength Ex. two pair = ["3S", "3C", "4S", "4D"]
        # this is used for finding the kickers
        self._strength_cards = []

        # these are the highest cards (in a 5 card hand)
        # that aren't used to make up the strength (need for tie breaking)
        self._kicker_cards = []

        # cards that are used for tie breaking similar strength hands
        # Ex. two pair = ["3S","4S"]
        self._primary_cards = []

    @classmethod
    def hand_eval(cls, hole_cards, community_cards):
        """
        main function to evaluate the hand, will call helper functions to determine the strength 
        of the hand and the kickers to create an object that will be used for tie breaking
        """
        # sort the cards in decensding order
        sorted_cards = Deck.sort_cards_by_rank(hole_cards + community_cards)
        hand_rank: str = ""

        # check and update strength
        if cls._is_royal_flush(sorted_cards):
            pass
        elif cls._is_straight_flush(sorted_cards):
            pass
        elif cls._is_four_of_a_kind(sorted_cards):
            pass
        elif cls._is_full_house(sorted_cards):
            pass
        elif cls._is_four_of_a_kind(sorted_cards):
            pass
        elif cls._is_straight(sorted_cards):
            pass
        elif cls._is_three_of_a_kind(sorted_cards):
            pass
        elif cls._is_two_pair(sorted_cards):
            pass
        elif cls._is_pair(sorted_cards):
            pass
        else:
            # highcard
            cls._highest_five(sorted_cards)
            hand_rank = cls.STRENGTH_MAP["high_card"]

        cls._set_kickers(sorted_cards)

        #to use information about the hand rank in the future
        return {
            "hand_rank": hand_rank,
            "primary_cards_rank": cls._primary_cards,
            "kickers": cls._kicker_cards
        }

    # gets the kickers based on the cards used to make up hand rank

    @classmethod
    def _set_kickers(cls, sorted_cards):
        """
        gets the kickers based on the cards used to make up hand rank
        """

        assert len(cls._strength_cards) > 0

        kickers = [
            card for card in sorted_cards if card not in cls._strength_cards]

        kickers_amount: int = 5 - len(cls._strength_cards)
        cls._kicker_cards = kickers[0:kickers_amount]

    # these will update _strength_cards, and _primary_cards
    @classmethod
    def _is_royal_flush(cls, sorted_cards) -> bool:
        pass

    @classmethod
    def _is_straight_flush(cls, sorted_cards) -> bool:
        pass

    @classmethod
    def _is_four_of_a_kind(cls, sorted_cards) -> bool:
        pass

    @classmethod
    def _is_full_house(cls, sorted_cards) -> bool:
        pass

    @classmethod
    def _is_flush(cls, sorted_cards) -> bool:
        pass

    @classmethod
    def _is_straight(cls, sorted_cards) -> bool:
        pass

    @classmethod
    def _is_three_of_a_kind(cls, sorted_cards) -> bool:
        pass

    @classmethod
    def _is_two_pair(cls, sorted_cards) -> bool:
        pass

    @classmethod
    def _is_pair(cls, sorted_cards) -> bool:
        pass

    @classmethod
    def _highest_five(cls, sorted_cards):
        cls._strength_cards = sorted_cards[0:5]
        cls._primary_cards = cls._strength_cards
