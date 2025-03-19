"""
    used to determine who won the hand 
"""
from .table import Table


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
        # first check compare rank of hand ("pair", "two-pair", etc)

        # if this is a tie check primary_cards

        # if primary cards are a tie check kickers

        # return list of winners

        # for testing purposes I am returning the 1st player always wins
        return [table.players[0]]

    # distribute money to winners
    @classmethod
    def add_money_to_winners(cls, table, winners):
        """
        Once winners are determine, add money to winners stacks based on pot 
        """

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
