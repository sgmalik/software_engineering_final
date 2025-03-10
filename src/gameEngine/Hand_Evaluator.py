from Card import Card


"""
HandEvaluator will provide information about the strength of a players hand
"""
class HandEvaluator():
    #these are the cards that make up the strength Ex. two pair = ["3S", "3C", "4S", "4D"]
    _strength_cards = []

    #these are the highest cards (in a 5 card hand) that aren't used to make up the strength
    _kickers = []

    _primary_cards = []

    STRENGTH_MAP = {
        "royal_flush": 10,
        "straight_flush": 9 ,
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
        
        hand_info = {
            "strength": {
                "hand_rank": 0,
                "primary_cards_rank": []
            },
            "kickers": []
        }

        hand_rank: str = ""

        if self._is_royal_flush(self, hole_cards, community_cards):
            pass
        elif self._is_straight_flush(self, hole_cards, community_cards):
            pass
        elif self._is_four_of_a_kind(self, hole_cards, community_cards):
            pass
        elif self._is_full_house(self, hole_cards, community_cards):
            pass
        elif self._is_four_of_a_kind(self, hole_cards, community_cards):
            pass
        elif self._is_straight(self, hole_cards, community_cards):
            pass
        elif self._is_three_of_a_kind(self, hole_cards, community_cards):
            pass
        elif self._is_two_pair(self, hole_cards, community_cards):
            pass
        elif self._is_pair(self, hole_cards, community_cards):
            pass
        else: 
            #highcard 
            self._highest_five(self,hole_cards, community_cards)
            hand_rank = self.STRENGTH_MAP["high_card"]
        
        self._kickers = self._get_kickers()

        hand_info["strength"]["hand_rank"] = self.STRENGTH_MAP[hand_rank]
        hand_info["kickers"] = self._kickers
        hand_info["strength"]["primary_cards"] = self._primary_cards
        return hand_info
    
    #get best 5 card hand 
    @classmethod
    def _best_hand(self, hole_cards, community_cards):
        pass
    
    #returns cards that are in best hand, but not used in hand rank
    @classmethod
    def _get_kickers(self):
        # set diff of 
        pass
    
    #strength of hand (calliing _is_)
    @classmethod
    def _calc_hand_strength(self, hole_cards, community_cards):
        pass
    

    #this method would probably make more sense somewhere else
    
    #functions to check for hand rank (used in _calc_hand_strength)
    #return cards that make, empty array is falsy
    #these will update strength_cards
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
    def _is_flush(self, hold_cards, community_cards):
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
    def _is_pair(self, hole_cards, community_cards):
        pass

    @classmethod 
    def _highest_five(self, hole_cards, community_cards):
        pass

    


