
"""
HandEvaluator will provide information about the strength of a players hand
"""
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
            "hand_rank": TWO_PAIR,
            "primary_cards_rank": [5, 3]
        },
        "kickers": [7]
    }

    NOTE: primary_cards are the cards that make up the hand rank (in this case, the pairs)
    
    """
    
    @classmethod
    def evaluate_hand(self, hole_cards, community_cards):
        #return hand rank, kickers
        pass
    
    #get best 5 card hand 
    @classmethod
    def _best_hand(self, hole_cards, community_cards):
        pass
    
    #returns cards that are in best hand, but not used in hand rank
    @classmethod
    def _get_kickers(self, hole_cards, best_hand):
        pass
    
    #strength of hand (calliing _is_)
    @classmethod
    def _calc_hand_strength(self, hole_cards, community_cards):
        pass
    

    #functions to check for hand rank (used in _calc_hand_strength)
    @classmethod
    def _is_royal_flush(self, hole_cards, community_cards):
        pass
    
    @classmethod
    def _is_straight_flush(self, hole_cards, community_cards):
        pass

    @classmethod
    def _is_four_of_a_kind(self, hole_cards, community_cards):
        pass
    
    @classmethod
    def _is_full_house(self, hole_cards, community_cards):
        pass
    
    @classmethod
    def _is_straight(self, hole_cards, community_cards):
        pass

    @classmethod
    def _is_three_of_a_kind(self, hole_cards, community_cards):
        pass

    @classmethod
    def _is_two_pair(self, hole_cards, community_cards):
        pass

    @classmethod
    def _is_high_card(self, hole_cards, community_cards):
        pass

    @classmethod
    def _is_pair(self, hole_cards, community_cards):
        pass


