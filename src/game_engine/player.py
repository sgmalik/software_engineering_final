"""
This module contains the Player class
"""

from .constants import Action, Street, PlayerState
from .card import Card
from typing import Union, List, Optional, cast


class Player:
    """
    represents a player in the game
    """

    def __init__(self, initial_stack, name: Optional[str] = None):
        self.hole_cards = []
        self.stack = initial_stack
        self.state = PlayerState.ACTIVE
        self.round_action_histories: List[Union[None, List[dict]]] = [
            None for _ in range(4)
        ]
        # 4 == len(["preflop", "flop", "turn", "river"])
        self.contribuition = 0
        self.action_histories = []
        self.name = name

    def add_hole_card(self, cards: List[Card]):
        if len(self.hole_cards) != 0:
            raise ValueError("Player already has hold cards")
        if len(cards) != 2:
            raise ValueError("Player can osnly have 2 hole cards")
        if not all(isinstance(card, Card) for card in cards):
            raise ValueError("Player can only have cards as hole cards")
        self.hole_cards = cards

    # eq's for removing from pending_betters, assuming names are unique
    def __eq__(self, other_player):
        if isinstance(other_player, Player):
            return self.name == other_player.name
        return False

    def clear_hole_cards(self):
        """
        clears the hole cards of the player
        """
        self.hole_cards = []

    def add_to_stack(self, amount: float | int):
        """
        add amount to player's stack
        """
        self.stack += amount

    def collect_bet(self, amount: float | int):
        if self.stack < amount:
            raise ValueError("Player cannot afford this bet")
        self.stack -= amount
        self.contribuition += amount

    def reset_contribuition(self):
        self.contribuition = 0

    def is_active(self):
        return self.state == PlayerState.ACTIVE

    def is_folded(self):
        return self.state == PlayerState.FOLDED

    def is_allin(self):
        return self.state == PlayerState.ALLIN

    def is_waiting(self):
        return self.state == PlayerState.WAITING

    def is_winner(self):
        return self.state == PlayerState.WINNER

    def add_action_history(
        self,
        action: Action,
        chip_amount: Union[int, float] = 0,
        add_amount: Union[int, float] = 0,
        sb_amount: Union[int, float] = 0,
        bb_amount: Union[int, float] = 0,
    ):
        """
        add action to player's action history
        """
        history = None
        if action == Action.FOLD:
            history = {"action": action, "name": self.name, "stack": self.stack}
        elif action == Action.CALL:
            pay_history = [
                h
                for h in self.action_histories
                if h["action"] != Action.FOLD and h["action"] != Action.ANTE
            ]
            last_pay = pay_history[-1] if len(pay_history) != 0 else None
            last_pay_amount = last_pay.get("paid", 0) if last_pay else 0
            history = {
                "name": self.name,
                "action": action,
                "amount": chip_amount,
                "paid": chip_amount - last_pay_amount,
                "stack": self.stack
            }
        elif action == Action.RAISE:
            pay_history = [
                h
                for h in self.action_histories
                if h["action"] != Action.FOLD and h["action"] != Action.ANTE
            ]
            last_pay = pay_history[-1] if len(pay_history) != 0 else None
            last_pay_amount = last_pay.get("paid", 0) if last_pay else 0
            history = {
                "name": self.name,
                "action": action,
                "amount": chip_amount,
                "paid": chip_amount - last_pay_amount,
                "add_amount": add_amount,
                "stack": self.stack
            }
        elif action == Action.SMALL_BLIND:
            assert sb_amount is not None
            add_amount = sb_amount
            history = {
                "action": action,
                "amount": sb_amount,
                "add_amount": add_amount,
                "name": self.name,
                "paid": sb_amount,
                "stack": self.stack
            }
        elif action == Action.BIG_BLIND:
            assert bb_amount is not None
            add_amount = bb_amount
            history = {
                "action": action,
                "amount": bb_amount,
                "add_amount": add_amount,
                "name": self.name,
                "paid": bb_amount,
                "stack": self.stack
            }
        elif action == Action.CHECK:
            history = {
                "action": action,
                "name": self.name,
                "stack": self.stack
            }

        if history is not None:
            self.action_histories.append(history)

    def save_round_action_histories(self, street: Street):
        """
        Save the current action histories to the round action histories for the given street.
        If there are already histories for this street, append to them instead of overwriting.
        """
        if self.round_action_histories[street.value] is None:
            self.round_action_histories[street.value] = []
        
        histories = cast(List[dict], self.round_action_histories[street.value])
        histories.extend(self.action_histories)
        self.action_histories = []

    def clear_action_histories(self):
        self.round_action_histories = [None for _ in range(4)]
        self.action_histories = []
