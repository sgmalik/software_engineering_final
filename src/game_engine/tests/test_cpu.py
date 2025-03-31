import pytest
from game_engine.constants import PlayerState
from game_engine.cpu.equityCPU import equityCPU
from game_engine.cpu.expectedValueCPU import expectedValueCPU
from game_engine.cpu.potOddsCPU import potOddsCPU
from game_engine.cpu.baselineCPU import baselineCPU


@pytest.fixture
def dummy_round_state():
    return {
        "community_card": ["HA", "D5", "C9"],
        "pot": {"main": 200, "side": []},
        "action_histories": {},
        "seats": [
            {"uuid": "player1", "stack": 800, "state": "participating"},
            {"uuid": "ai-uuid", "stack": 1200, "state": "participating"},
        ],
    }


@pytest.fixture
def dummy_valid_actions():
    return [
        {"action": "fold"},
        {"action": "call", "amount": 50},
        {"action": "raise", "amount": {"min": 100, "max": 1000, "raisable": True}},
    ]


@pytest.fixture
def dummy_hole_cards():
    return ["H2", "H7"]


def test_equity_cpu_action(dummy_valid_actions, dummy_hole_cards, dummy_round_state):
    cpu = equityCPU(initial_stack=1000)
    action, amount = cpu.declare_action(
        dummy_valid_actions, dummy_hole_cards, dummy_round_state
    )
    assert action in ["fold", "call", "raise"]
    assert isinstance(amount, int)


def test_expected_value_cpu_action(
    dummy_valid_actions, dummy_hole_cards, dummy_round_state
):
    cpu = expectedValueCPU(initial_stack=1000)
    action, amount = cpu.declare_action(
        dummy_valid_actions, dummy_hole_cards, dummy_round_state
    )
    assert action in ["fold", "call", "raise"]
    assert isinstance(amount, int)


def test_pot_odds_cpu_action(dummy_valid_actions, dummy_hole_cards, dummy_round_state):
    cpu = potOddsCPU(initial_stack=1000)
    action, amount = cpu.declare_action(
        dummy_valid_actions, dummy_hole_cards, dummy_round_state
    )
    assert action in ["fold", "call", "raise"]
    assert isinstance(amount, int)


def test_baseline_cpu_methods():
    cpu = baselineCPU(initial_stack=1000)
    assert cpu.stack == 1000
    cpu.add_to_stack(100)
    assert cpu.stack == 1100
    cpu.bet(200)
    assert cpu.stack == 900
    assert cpu.contribuition == 200
    cpu.fold()
    assert cpu.state == PlayerState.FOLDED
    cpu.clear_hole_cards()
    assert cpu.hole_cards == []
