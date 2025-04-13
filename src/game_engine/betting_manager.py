"""
betting_manager is adapted from pypokerengine's RoundManager class,
"""
from .constants import Action
from .table import Table
from .constants import PlayerState
from .game_evaluator import GameEvaluator



class BettingManager: 
    """
    the purpose of betting manager, is to track pending_betters (who is still in the hand)
    as well as update table information based on player action
    """
    def __init__(self, table, blind):
        
        self.table = table
        self.current_bet = 0
        self.blind = blind

        # this array represents active
        # players who haven't responded to a bet yet
        self.pending_betters = []

    def reset_betting_round(self):
        """
        set up betting state, for the next street
        """
        self.current_bet = 0
        self.pending_betters = self.table.active_players()
        self.table.reset_contribution()

    def apply_player_action(self, current_player, action: Action, raise_amount = None):
        """
        declare action for the current player
        """
        
        if action == Action.CALL:
            self._call(current_player)
        elif action == Action.CHECK:
            self._check(current_player)
        elif action == Action.RAISE:
            self._raise(current_player, raise_amount)
        elif action == Action.FOLD:
            self._fold(current_player)
        elif action == Action.SMALL_BLIND:
            self._blind(current_player, self.blind)
        elif action == Action.BIG_BLIND:
            self.current_bet = self.blind*2
            self._blind(current_player, self.blind*2)
        self.table.next_player()
        
        
    def _blind(self, current_player, blind):
        """
        blind player action
        """
        if self._is_all_in(current_player, blind):
            all_in_amount = current_player.stack
            current_player.collect_bet(all_in_amount)
            self.table.pot.add_to_pot(all_in_amount)
            current_player.state = PlayerState.ALLIN
            self._remove_better(current_player)
        else: 
            current_player.collect_bet(blind)
            self.table.pot.add_to_pot(blind)

    def _fold(self, current_player):
        """
        change playerState, remove from pending betters
        NOTE: since its 1v1 can just add pot to opposite player's stack
        """
        current_player.state = PlayerState.FOLDED
        winner = [player for player in self.table.players if player.state != PlayerState.FOLDED]
        GameEvaluator.add_money_to_winners(self.table, winner) 
        self._remove_better(current_player)

    def _raise(self, current_player, raise_amount):
        """
        pay current bet, raise bet 
        """
        
        call_amount = self.current_bet - current_player.contribuition

        if self._is_all_in(current_player, call_amount + raise_amount):
            all_in_amount = current_player.stack
        
            self._raise_bet(all_in_amount)
            current_player.state = PlayerState.ALLIN
            self.table.pot.add_to_pot(all_in_amount)
            current_player.collect_bet(all_in_amount)
            self._remove_better(current_player)
        else:
            # need to pay current bet first
            current_player.collect_bet(call_amount)
            self.table.pot.add_to_pot(call_amount)

            # do the raise action
            self._raise_bet(raise_amount)
            current_player.collect_bet(raise_amount)
            self.table.pot.add_to_pot(raise_amount)
            self._add_betters(current_player)

       
    def _is_all_in(self, current_player, amount):
        #if no money they are all in
        return current_player.stack <= amount
        
    def _call(self, current_player):
        """
        pay current bet
        """
        call_amount = self.current_bet - current_player.contribuition
        #if you can't pay full raise all_in
        if self._is_all_in(current_player, call_amount):
            all_in_amount = current_player.stack
            current_player.collect_bet(all_in_amount)
            self.table.pot.add_to_pot(all_in_amount)
            current_player.state = PlayerState.ALLIN
        else:
            current_player.collect_bet(call_amount)
            self.table.pot.add_to_pot(call_amount)
        self._remove_better(current_player)
    

    def _check(self, current_player):
        """
        Player checks if there is no bet to call
        """
        if current_player.contribuition < self.current_bet:
            raise ValueError("Cannot check when facing a bet.")
        self._remove_better(current_player)

    def is_betting_over(self) -> bool:
        """
        check if betting is over (to be used in dealer),
        if betting is over than the street is over
        """
        return len(self.pending_betters) == 0

    def _remove_better(self, current_player):
        """
        remove current player from current_betters
        """
        self.pending_betters.remove(current_player)

    def _add_betters(self, current_player):
        """
        add all other active players to current betters
        this will be called when a player raises the bet
        """
        self.pending_betters = []
        for player in self.table.active_players():
            if player != current_player:
                self.pending_betters.append(player)

    def _raise_bet(self, amount):
        """
        raise the current bet by the amount (this is so we can keep track of the current bet)
        """
        self.current_bet += amount

    def get_max_raise(self, current_player):
        """
        gets the maximum amount the current player can raise by
        """
        return current_player.stack - (self.current_bet - current_player.contribuition)