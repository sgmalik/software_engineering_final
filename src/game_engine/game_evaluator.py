"""
    game_evaluator.py was inspired by 
    https://github.com/ishikota/PyPokerEngine/blob/master/pypokerengine/engine/game_evaluator.py
    the code is written by us, but the structure is based loosely on pypokerengine.
"""
from .table import Table
from .hand_evaluator import HandEvaluator
from functools import reduce


class GameEvaluator():

    """
Game Evaluator will:
     decide who the winners are 
     handle side pots (will worry about this once, 1v1 is working)
        #see https://github.com/ishikota/PyPokerEngine/blob/master/pypokerengine/engine/game_evaluator.py
     distribute money to winners
"""
    @classmethod
    def determine_winners(cls, table):
        """
        Uses hand evaluator to determine the winners of the hand,
        NOTE: only 1v1 for now 
        """
        #get each hand 
        hands = {}
        
        for player in table.players:
            hand_info = HandEvaluator.hand_eval(player.hole_cards, table.community_cards)
            hands[player.name] = hand_info
               
        print("hands", hands)
        player1 = table.players[0]
        player2 = table.players[1]
        hand1 = hands[table.players[0].name]
        hand2 = hands[table.players[1].name]

        #check hand ranks first
        if hand1["hand_rank"] > hand2["hand_rank"]:
            return [player1]
        if hand1["hand_rank"] < hand2["hand_rank"]:
            return [player2]
        
        #NOTE: in these loops we are assuming every card array is in decending order
        #check primary cards 
        for i in range(len(hand1["primary_cards_rank"])):
            if hand1["primary_cards_rank"][i] > hand2["primary_cards_rank"][i]:
                return [player1]
            if hand1["primary_cards_rank"][i] < hand2["primary_cards_rank"][i]:
                return [player2]
        
        #check kickers
        for i in range(len(hand1["kickers"])):
            if hand1["kickers"][i] > hand2["kickers"][i]:
                return [player1]
            if hand1["kickers"][i] < hand2["kickers"][i]:
                return [player2]
        
        # if passed other checks, then the hands are tied 
        return [player1, player2]
        

    # distribute money to winners
    @classmethod
    def add_money_to_winners(cls, table, winners):
        """
        Once winners are determine, add money to winners stacks based on pot.
        NOTE: doesn't handle side pots rn 
        """
        for winner in winners:
            winner.stack += (table.pot.value / len(winners))

    #NOTE: these will be unimplemented for now, because just 1v1
    @classmethod
    def _eligible_players(cls, table):
        """
        To be called in determine, winners, to get the players that are still in the hand
        """

    @classmethod
    def _get_side_pots(cls):
        """
        handle side pots
        """
