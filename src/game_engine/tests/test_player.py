import pytest
from game_engine.player import Player
from game_engine.card import Card
from game_engine.constants import Action, Street, PlayerState


@pytest.fixture
def player():
    return Player(initial_stack=1000)


def test_add_hole_cards_valid(player):
    cards = [Card("H", "A"), Card("D", "K")]
    player.add_hole_card(cards)
    assert player.hole_cards == cards


def test_add_hole_cards_twice_raises(player):
    cards = [Card("H", "A"), Card("D", "K")]
    player.add_hole_card(cards)
    with pytest.raises(ValueError):
        player.add_hole_card(cards)


def test_add_hole_cards_invalid_count(player):
    with pytest.raises(ValueError):
        player.add_hole_card([Card("H", "A")])


def test_add_hole_cards_invalid_type(player):
    with pytest.raises(ValueError):
        player.add_hole_card(["not a card", "still not a card"])


def test_clear_hole_cards(player):
    cards = [Card("H", "A"), Card("D", "K")]
    player.add_hole_card(cards)
    player.clear_hole_cards()
    assert player.hole_cards == []


def test_add_to_stack(player):
    player.add_to_stack(500)
    assert player.stack == 1500


def test_collect_bet_valid(player):
    player.collect_bet(200)
    assert player.stack == 800


def test_collect_bet_insufficient_stack(player):
    with pytest.raises(ValueError):
        player.collect_bet(2000)


@pytest.mark.parametrize(
    "state,checker",
    [
        (PlayerState.ACTIVE, Player.is_active),
        (PlayerState.FOLDED, Player.is_folded),
        (PlayerState.ALLIN, Player.is_allin),
        (PlayerState.WAITING, Player.is_waiting),
        (PlayerState.WINNER, Player.is_winner),
    ],
)
def test_player_states(player, state, checker):
    player.state = state
    assert checker(player) is True


def test_add_action_history_fold(player):
    player.add_action_history(Action.FOLD)
    assert player.action_histories[-1] == {"action": Action.FOLD}


def test_add_action_history_call(player):
    player.add_action_history(Action.CALL, chip_amount=100)
    history = player.action_histories[-1]
    assert history["action"] == Action.CALL
    assert "amount" in history and "paid" in history


def test_add_action_history_raise(player):
    player.add_action_history(Action.RAISE, chip_amount=300, add_amount=200)
    history = player.action_histories[-1]
    assert history["action"] == Action.RAISE
    assert "amount" in history and "paid" in history and "add_amount" in history


def test_add_action_history_small_blind(player):
    player.add_action_history(Action.SMALL_BLIND, sb_amount=50)
    assert player.action_histories[-1]["amount"] == 50


def test_add_action_history_big_blind(player):
    player.add_action_history(Action.BIG_BLIND, bb_amount=100)
    assert player.action_histories[-1]["amount"] == 100


def test_add_action_history_ante(player):
    player.add_action_history(Action.ANTE, chip_amount=10)
    assert player.action_histories[-1]["amount"] == 10


def test_add_action_history_invalid(player):
    class FakeAction:
        value = "INVALID"

    with pytest.raises(ValueError):
        player.add_action_history(FakeAction())


def test_save_round_action_histories(player):
    player.add_action_history(Action.FOLD)
    player.save_round_action_histories(Street.PREFLOP)
    assert player.round_action_histories[Street.PREFLOP.value] is not None
    assert player.action_histories == []


def test_clear_action_histories(player):
    player.add_action_history(Action.FOLD)
    player.clear_action_histories()
    assert player.round_action_histories == [None] * 4
    assert player.action_histories == []


def test_bet(player):
    player.collect_bet(250)
    assert player.stack == 750
    assert player.contribuition == 250
