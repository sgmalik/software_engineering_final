
"""
    hand_evaluator.py is an adaptation of 
    https://github.com/ishikota/PyPokerEngine/blob/master/pypokerengine/engine/deck.py
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
        "four_of_a_kind": 8,
        "full_house": 7,
        "flush": 6,
        "straight": 5,
        "three_of_a_kind": 4,
        "two_pair": 3,
        "pair": 2,
        "high_card": 1,
    }

    def __init__(self):
        # these are the highest cards (in a 5 card hand)
        # that aren't used to make up the strength (need for tie breaking)
        self._kicker_cards = []

        # cards that are used for tie breaking similar strength hands
        # Ex. two pair = ["4S", "4H", "3S", "3H"]
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

        # init maps
        card_match_map = cls._create_card_match_map(sorted_cards)
        suit_map = cls._create_suit_map(sorted_cards)

        match_rank, match_primary_cards = cls._check_matches(card_match_map)
        suits_rank, suit_primary_cards = cls._check_suits(suit_map, sorted_cards)
        primary_cards = []

        if match_rank > suits_rank:
            hand_rank = match_rank
            primary_cards = match_primary_cards
        elif match_rank < suits_rank:
            hand_rank = suits_rank
            primary_cards = suit_primary_cards
        else:
            hand_rank = cls.STRENGTH_MAP["high_card"]

        kickers = cls._set_kickers(sorted_cards, primary_cards)

        # to use information about the hand rank in the future
        return {
            "hand_rank": hand_rank,
            "primary_cards_rank": primary_cards,
            "kickers": kickers,
        }

    # gets the kickers based on the cards used to make up hand rank

    @classmethod
    def _create_card_match_map(cls, sorted_cards):
        """
        create a map of the cards and their ranks
        """
        # this map will be used to check pair, two pair, three of a kind, fullhouse
        card_match_map = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
            9: [],
            10: [],
            11: [],
            12: [],
            13: [],
            14: [],
        }

        for card in sorted_cards:
            card_rank = card.get_card_rank()
            card_match_map[card_rank].append(card)

        print("MAP", card_match_map)
        return card_match_map

    @classmethod
    def _create_suit_map(cls, sorted_cards):
        """
        create a map of the cards and their suits
        """
        # this map will used to check royal flush, flush, straight flush
        suit_map = {
            "H": [],
            "D": [],
            "C": [],
            "S": []
        }

        for card in sorted_cards:
            suit_map[card.suit].append(card)

        return suit_map

    @classmethod
    def _set_kickers(cls, sorted_cards, primary_cards):
        """
        gets the kickers based on the cards used to make up hand rank
        """

        kickers = [
            card for card in sorted_cards if card not in primary_cards]

        kickers_amount: int = 5 - len(primary_cards)
        return kickers[0:kickers_amount]

    @classmethod
    def _check_suits(cls, card_suit_map, sorted_cards):
        straight_counter = 0
        straight_cards = []

        for cards in card_suit_map.values():
            if len(cards) >= 5:
                sorted_cards = Deck.sort_cards_by_rank(cards)
                for i in range(len(sorted_cards) - 1):
                    next_card = sorted_cards[i + 1]
                    curr_card = sorted_cards[i]
                    if curr_card.get_card_rank() - 1 == next_card.get_card_rank():
                        straight_counter += 1

                if straight_counter >= 4:
                    straight_cards.extend(sorted_cards[:5])
                else:
                    return cls.STRENGTH_MAP["flush"], cards

        # if first card is an ace royal flush
        if straight_cards:
            if straight_cards[0].get_card_rank() == 14:
                return cls.STRENGTH_MAP["royal_flush"], straight_cards[:5]

            return cls.STRENGTH_MAP["straight_flush"], straight_cards[:5]
        
        #check for straight
        straight_cards = []
        for i in range(len(sorted_cards) - 1):
            next_card = sorted_cards[i + 1]
            curr_card = sorted_cards[i]
            if curr_card.get_card_rank() - 1 == next_card.get_card_rank():
                straight_cards.append(sorted_cards[i])

        if len(straight_cards) >= 5:
            return cls.STRENGTH_MAP["straight"], straight_cards[:5]


        return cls.STRENGTH_MAP["high_card"], []

    # pypoker uses bit mask which is probably better
    # there's a lot of overlapping logic.

    @classmethod
    def _check_matches(cls, card_match_map):
        pairs = [0, []]
        triples = [0, []]
        

        # TODO: use extend
        # this will be used to check for pair, two pair, three of a kind, full house
        for cards in card_match_map.values():
            if len(cards) == 2:
                for card in cards:
                    pairs[1].append(card)
                pairs[0] += 1
            elif len(cards) == 3:
                for card in cards:
                    triples[1].append(card)
                triples[0] += 1
            elif len(cards) == 4:
                return cls.STRENGTH_MAP["four_of_a_kind"], cards
            
            

        pair_cards = Deck.sort_cards_by_rank(pairs[1])
        triple_cards = Deck.sort_cards_by_rank(triples[1])[:3]

        if triples[0] >= 1 and pairs[0] >= 1:
            return cls.STRENGTH_MAP["full_house"], [*triple_cards, *pair_cards[:2]]
        elif triples[0] >= 1:
            return cls.STRENGTH_MAP["three_of_a_kind"], [*triple_cards]
        elif pairs[0] >= 2:
            return cls.STRENGTH_MAP["two_pair"], [*pair_cards]
        elif pairs[0] == 1:
            return cls.STRENGTH_MAP["pair"], [*pair_cards[:2]]

        return cls.STRENGTH_MAP["high_card"], []

    @classmethod
    def _highest_five(cls, sorted_cards):
        return sorted_cards[0:5]
