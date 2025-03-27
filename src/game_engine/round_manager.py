from .dealer import Dealer
from .table import Table
from .constants import Action
class RoundManager: 
    def __init__(self, dealer, table):
        self.table = table
        self.dealer = dealer
        
    
    def start_preflop(self):
        """
        do preflop actions 
        """
        self.table.deal_hole_cards()

        # blinds
        self.dealer.apply_player_action(Action.SMALL_BLIND)
        self.dealer.apply_player_action(Action.BIG_BLIND)


    def start_flop(self):
        """
        do start of flop actions
        """
        self.table.deal_community_cards(3)
        self.dealer.reset_current_bet()

   
    def start_turn(self):
        """
        do start of turn actions
        """
        self.table.deal_community_cards(1)
        self.dealer.reset_current_bet()

    
    def start_river(self):
        """
        do start of river actions
        """
        self.table.deal_community_cards(1)
        self.dealer.reset_current_bet()
    
    def remove_better(self, current_player):
        """
        remove current player from current_betters
        """
        self.dealer.pending_betters.remove(current_player)

    def add_betters(self, current_player):
        """
        add all other active players to current betters
        this will be called when a player raises the bet
        """
        self.dealer.pending_betters = []
        for player in self.table.active_players():
            if player != current_player:
                self.dealer.pending_betters.append(player)
    
    

    def _reset_current_bet(self):
        """
        reset current bet to 0
        """
        self.dealer.current_bet = 0