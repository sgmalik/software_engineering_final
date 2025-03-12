
from Table import Table
"""
Game Evaluator will:
     decide who the winners are 
     handle side pots (will worry about this once, 1v1 is working)
        #see https://github.com/ishikota/PyPokerEngine/blob/master/pypokerengine/engine/game_evaluator.py
     distribute money to winners
"""
class GameEvaluator():

    #uses hand evaluator on each hand to determine winnners
    @classmethod
    def determine_winners(self, table):
        #first check compare rank of hand ("pair", "two-pair", etc)

        #if this is a tie check primary_cards

        #if primary cards are a tie check kickers 

        #return list of winners

        #for testing purposes I am returning the 1st player always wins
        return [table.players[0]]

    #distribute money to winners
    @classmethod
    def add_money_to_winners(self, table, winners):
        pass

    #returns the players that are still active, or allin 
    @classmethod
    def eligible_players(self, table):
        pass

    @classmethod
    def handle_pot():
        pass
    
    #to get side pots you would check all the players that are allin, and use Player.contribuition
    @classmethod 
    def get_side_pots():
        pass
