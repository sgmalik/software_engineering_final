"""
    used to determine who won the hand 
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
        Uses hand evaluator to determine the winners of the hand 
        """
        #get each hand 
        hands = {}
        winners = []
        for player in table.players:
            hand_info = HandEvaluator.hand_eval(player.hole_cards, table.community_cards)
            hands[player.name] = hand_info
               
                
            
        winners = reduce(cls.determine_winning_hand, hands.values())
        # if this is a tie check primary_cards

        # if primary cards are a tie check kickers

        # return list of winners

        # for testing purposes I am returning the 1st player always wins
        return winners
    
    @classmethod
    def determine_winning_hand(cls, hand1, hand2):
        """
        return the winning hand out of two hands 
        """
        #if list of two hands just use the first hand (they are the same)

        hand1 = hand1[0] if isinstance(hand1, list) else hand1
        hand2 = hand2[0] if isinstance(hand2, list) else hand2

        #check hand ranks first 
        if hand1["hand_rank"] > hand2["hand_rank"]:
            return [hand1]
        if hand1["hand_rank"] < hand2["hand_rank"]:
            return [hand2]
        
        #check primary cards 
        if max(hand1["primary_cards_rank"]) > max(hand2["primary_cards_rank"]):
            return [hand1]
        if max(hand1["primary_cards_rank"]) < max(hand2["primary_cards_rank"]):
            return [hand2]
        
        #check kickers
        if max(hand1["kickers"]) > max(hand2["kickers"]):
            return [hand1]
        if max(hand1["kickers"]) < max(hand2["kickers"]):
            return [hand2]
        
        # hand is tied  
        return [hand1, hand2]
        

    # distribute money to winners
    @classmethod
    def add_money_to_winners(cls, table, winners):
        """
        Once winners are determine, add money to winners stacks based on pot.
        NOTE: doesn't handle side pots rn 
        """
        for winner in winners:
            winner.stack += (table.pot.value / len(winners))

    @classmethod
    def _eligible_players(cls, table):
        """
        To be called in determine, winners, to get the players that are still in the hand
        """

    @classmethod
    def _handle_pot(cls):
        """
        handle pot
        """

    @classmethod
    def _get_side_pots(cls):
        """
        handle side pots
        """
