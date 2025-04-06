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
        Uses hand evaluator to determine the winners of the hand,
        NOTE: only 1v1 for now 
        """
        #get each hand 
        hands = {}
        
        for player in table.players:
            hand_info = HandEvaluator.hand_eval(player.hole_cards, table.community_cards)
            hands[player.name] = hand_info
               
                
        player1 = table.players[0]
        player2 = table.players[1]
        hand1 = hands[table.players[0].name]
        hand2 = hands[table.players[1].name]

        #check hand ranks first
        if hand1["hand_rank"] > hand2["hand_rank"]:
            return [player1]
        if hand1["hand_rank"] < hand2["hand_rank"]:
            return [player2]
        
        #check primary cards 
        #will not work because its card class 
        if max(hand1["primary_cards_rank"]) > max(hand2["primary_cards_rank"]):
            return [player1]
        if max(hand1["primary_cards_rank"]) < max(hand2["primary_cards_rank"]):
            return [player2]
        
        #check kickers
        if max(hand1["kickers"]) > max(hand2["kickers"]):
            return [player1]
        if max(hand1["kickers"]) < max(hand2["kickers"]):
            return [player2]
        
        # should return array of players 
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
