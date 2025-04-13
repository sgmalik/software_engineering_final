"""
betting_manager is adapted from pypokerengine's RoundManager class,
"""
from .constants import Action
from .table import Table
from .constants import PlayerState


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
        #check all_in so all_in player doesn't get added to pending betters
        self._check_all_in(current_player)

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
        current_player.collect_bet(blind)
        self.table.pot.add_to_pot(blind)

    def _fold(self, current_player):
        """
        change playerState, remove from pending betters
        """
        current_player.state = PlayerState.FOLDED
        self._remove_better(current_player)

    def _raise(self, current_player, raise_amount):
        """
        pay current bet, raise bet 
        """
        # Handle the call portion
        call_amount = max(0, self.current_bet - current_player.contribuition)
        actual_call = min(call_amount, current_player.stack)

        current_player.collect_bet(actual_call)
        self.table.pot.add_to_pot(actual_call)

        #Determine raise cap
        remaining_stack = current_player.stack
        actual_raise = min(raise_amount, remaining_stack)
        # Execute raise

        self._raise_bet(actual_raise)
        current_player.collect_bet(actual_raise)
        self.table.pot.add_to_pot(actual_raise)
        self._add_betters(current_player)

    
    def _check_all_in(self, current_player):
        """
        change to all_in state when player's stack hits 0
        """
        #if players stack is 0, they are all in
        if current_player.stack == self.get_max_raise(current_player):
            current_player.is_allin()
        
    def _call(self, current_player):
        """
        pay current bet
        """
        # Calculate how much is needed to call
        call_amount = max(0, self.current_bet - current_player.contribuition)
        actual_call = min(call_amount, current_player.stack)

        current_player.collect_bet(actual_call)
        self.table.pot.add_to_pot(actual_call)
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
        return len(self.pending_betters) == 0 or len(self.table.active_players()) == 1

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
        call_amount = max(0, self.current_bet - current_player.contribuition)
        max_raise_after_call = current_player.stack - call_amount

        opponents = [p for p in self.table.players if p != current_player and p.is_active()]
        if not opponents:
            return max_raise_after_call

        opponent = opponents[0] 
        opponent_matchable = opponent.stack + opponent.contribuition - current_player.contribuition

        return max(0, min(max_raise_after_call, opponent_matchable))