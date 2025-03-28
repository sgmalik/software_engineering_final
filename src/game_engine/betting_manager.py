from .constants import Action
from .table import Table
from .constants import PlayerState

class BettingManager: 
    def __init__(self, table, blind):
        
        self.table = table
        self.current_bet = 0
        self.blind = blind
        self.pending_betters = []

    def reset_betting_round(self):
        self.current_bet = 0
        self.pending_betters = self.table.active_players()
        self.table.reset_contribution()

    def apply_player_action(self, current_player, action: Action, raise_amount = None):
        """
        declare action for the current player
        """
        if action == Action.CALL:
            self._call(current_player)
        elif action == Action.RAISE:
            self._raise(current_player, raise_amount)
        elif action == Action.FOLD:
            # TODO: replace this with player fold function
            self._fold(current_player)
        elif action == Action.SMALL_BLIND:
            self._blind(current_player, self.blind)
        elif action == Action.BIG_BLIND:
            self.current_bet = self.blind*2
            self._blind(current_player, self.blind*2)
        self.table.next_player()

    def _blind(self, current_player, blind):
        current_player.bet(blind)
        self.table.pot.add_to_pot(blind)

    def _fold(self, current_player):
        current_player.state = PlayerState.FOLDED
        self._remove_better(current_player)

    def _raise(self, current_player, raise_amount):
        # need to pay current bet first
        call_amount = self.current_bet - current_player.contribuition
        current_player.bet(call_amount)
        self.table.pot.add_to_pot(call_amount)

        # do the raise action
        self._raise_bet(raise_amount)
        current_player.bet(raise_amount)
        self.table.pot.add_to_pot(raise_amount)
        self._add_betters(current_player)

    def _call(self, current_player):
        call_amount = self.current_bet - current_player.contribuition
        current_player.bet(call_amount)

        self.table.pot.add_to_pot(call_amount)
        self._remove_better(current_player)

    def is_betting_over(self) -> bool:
        """
        check if betting is over (to be used in game_engine),
        if betting is over than the street is over 
        """
        # so going to have pending actions array. players that are still active will go in the array
        # so if they check they aren't in the array anymore
        # if they raise all the other players are in the array as well
        # if betting is over need to set current bet to 0 (in game_engine)

        # should this check if every other player is folded.

        # when checking if betting is over and thats true, you should check if the round is over
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