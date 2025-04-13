
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

        #init maps
        card_match_map = cls._create_card_match_map(sorted_cards)
        suit_map = cls._create_suit_map(sorted_cards)

        # check and update strength
        if cls._is_royal_flush(suit_map):
            pass
        elif cls._is_straight_flush(suit_map):
            pass
        elif cls._is_four_of_a_kind(card_match_map):
            pass
        elif cls._is_full_house(card_match_map):
            pass
        elif cls._is_flush(suit_map):
            pass
        elif cls._is_straight(suit_map):
            pass
        elif cls._is_three_of_a_kind(card_match_map):
            pass
        elif cls._is_two_pair(card_match_map):
            hand_rank = cls.STRENGTH_MAP["two_pair"]
        elif cls._is_pair(card_match_map):
            hand_rank = cls.STRENGTH_MAP["pair"]
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
    def _create_card_match_map(cls, sorted_cards):
        """
        create a map of the cards and their ranks
        """
        #this map will be used to check pair, two pair, three of a kind, fullhouse
        card_match_map = {
            1:[],
            2:[],
            3:[],
            4:[],
            5:[],
            6:[],
            7:[],
            8:[],
            9:[],
            10:[],
            11:[],
            12:[],
            13:[],
            14:[],
        }

        for card in sorted_cards:
            card_rank = card.get_card_rank()
            card_match_map[card_rank].append(card)
        
        return card_match_map


    @classmethod
    def _create_suit_map(cls, sorted_cards):
        """
        create a map of the cards and their suits
        """
         #this map will used to check royal flush, flush, straight flush
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
    def _set_kickers(cls, sorted_cards):
        """
        gets the kickers based on the cards used to make up hand rank
        """

        assert len(cls._primary_cards) > 0

        kickers = [
            card for card in sorted_cards if card not in cls._primary_cards]

        kickers_amount: int = 5 - len(cls._primary_cards)
        cls._kicker_cards = kickers[0:kickers_amount]

    # pypoker uses bit mask which is probably better
    #there's a lot of overlapping logic. 
    @classmethod
    def _is_royal_flush(cls, suit_map) -> bool:
        pass

    @classmethod
    def _is_straight_flush(cls, suit_map) -> bool:
        pass

    @classmethod
    def _is_four_of_a_kind(cls, card_match_map) -> bool:
        pass

    @classmethod
    def _is_full_house(cls, card_match_map) -> bool:
        pass

    @classmethod
    def _is_flush(cls, card_match_map) -> bool:
        pass

    @classmethod
    def _is_straight(cls, card_match_map) -> bool:
        pass

    @classmethod
    def _is_three_of_a_kind(cls, card_match_map) -> bool:
        pass

    @classmethod
    def _is_two_pair(cls, card_match_map) -> bool:
        pairs = 0
        cards_to_add = []
        print("card_match_map", card_match_map)
        for cards in card_match_map.values():
            if len(cards) == 2:
                cards_to_add.append(cards[0])
                cards_to_add.append(cards[1])
                pairs += 1

        if pairs == 2:
            cls._add_primary_cards(cards_to_add)
            return True
        return False

    @classmethod
    def _is_pair(cls, card_match_map) -> bool:
        """
        find if two cards have the same rank
        """
        for cards in card_match_map.values():
            if len(cards) == 2:
                cls._primary_cards = cards
                return True
        return False


    @classmethod
    def _highest_five(cls, sorted_cards):
        cls._primary_cards = sorted_cards[0:5]


    @classmethod
    def _add_primary_cards(cls, cards):
        """
        add the primary cards to the hand evaluator
        """
        for card in cards:
            cls._primary_cards.append(card)