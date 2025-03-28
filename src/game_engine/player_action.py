from .constants import PlayerState
from .round_manager import RoundManager
from .dealer import Dealer
from .table import Table

class PlayerAction:
    def __init__(self, table: Table, dealer: Dealer, round_manager: RoundManager):
        self.table = table
        self.dealer = dealer 
        self.round_manager = round_manager


    def blind(self, blind):
        self.table.current_player.bet(blind)
        self.table.add_to_pot(blind)

    def fold(self):
        self.table.current_player.state = PlayerState.FOLDED
        self.round_manager.remove_better(self.table.current_player)

    def raise_by_amount(self, raise_amount):
        # need to pay current bet first
        call_amount = self.dealer.current_bet - self.table.current_player.contribuition
        self.table.current_player.bet(call_amount)
        self.table.add_to_pot(call_amount)

        # do the raise action
        self.dealer.raise_bet(raise_amount)
        self.table.current_player.bet(raise_amount)
        self.table.add_to_pot(raise_amount)
        self.round_manager.add_betters(self.table.current_player)

    def call(self):
        call_amount = self.dealer.current_bet - self.table.current_player.contribuition
        self.table.current_player.bet(call_amount)

        self.table.add_to_pot(call_amount)
        self.round_manager.remove_better(self.table.current_player)
    
    