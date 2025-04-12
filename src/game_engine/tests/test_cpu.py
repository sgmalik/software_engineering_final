import pytest
from game_engine.constants import PlayerState
from game_engine.cpu.equityCPU import equityCPU
from game_engine.cpu.expectedValueCPU import expectedValueCPU
from game_engine.cpu.potOddsCPU import potOddsCPU
from game_engine.cpu.baselineCPU import baselineCPU
from game_engine.card import Card


@pytest.fixture
def dummy_round_state():
    return {
        "community_card": ["HA", "D5", "C9"],
        "pot": {"main": 200, "side": []},
        "action_histories": {},
        "seats": [
            {"name": "player1", "stack": 800, "state": "participating"},
            {"name": "ai", "stack": 1200, "state": "participating"},
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


@pytest.fixture
def dummy_game_info():
    return {
        "player_num": 2,
        "rule": {
            "initial_stack": 1000,
            "small_blind": 10,
            "max_round": 10,
            "ante": 0
        },
        "seats": [
            {"name": "player1", "stack": 1000},
            {"name": "ai", "stack": 1000}
        ]
    }


@pytest.fixture
def dummy_round_start():
    return {
        "round_count": 1,
        "hole_card": ["H2", "H7"],
        "seats": [
            {"name": "player1", "stack": 1000, "state": "participating"},
            {"name": "ai", "stack": 1000, "state": "participating"}
        ]
    }


@pytest.fixture
def dummy_street_start():
    return {
        "street": "flop",
        "round_state": {
            "community_card": ["HA", "D5", "C9"],
            "pot": {"main": 200, "side": []},
            "action_histories": {},
            "seats": [
                {"name": "player1", "stack": 800, "state": "participating"},
                {"name": "ai", "stack": 1200, "state": "participating"},
            ],
        }
    }


@pytest.fixture
def dummy_game_update():
    return {
        "new_action": {
            "player_name": "player1",
            "action": "call",
            "amount": 50
        },
        "round_state": {
            "community_card": ["HA", "D5", "C9"],
            "pot": {"main": 200, "side": []},
            "action_histories": {},
            "seats": [
                {"name": "player1", "stack": 800, "state": "participating"},
                {"name": "ai", "stack": 1200, "state": "participating"},
            ],
        }
    }


@pytest.fixture
def dummy_round_result():
    return {
        "winners": [{"name": "ai"}],
        "hand_info": {
            "player1": {"hand": ["H2", "H7"], "hand_rank": "high_card"},
            "ai": {"hand": ["HA", "D5"], "hand_rank": "pair"}
        },
        "round_state": {
            "community_card": ["HA", "D5", "C9"],
            "pot": {"main": 200, "side": []},
            "action_histories": {},
            "seats": [
                {"name": "player1", "stack": 800, "state": "participating"},
                {"name": "ai", "stack": 1200, "state": "participating"},
            ],
        }
    }


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
    cpu.collect_bet(200)
    assert cpu.stack == 900
    assert cpu.contribuition == 200
    cpu.clear_hole_cards()
    assert cpu.hole_cards == []


def test_equity_cpu_game_start(dummy_game_info):
    cpu = equityCPU(initial_stack=1000)
    cpu.receive_game_start_message(dummy_game_info)
    assert cpu.game_info == dummy_game_info
    assert cpu.stack == 1000


def test_equity_cpu_round_start(dummy_round_start):
    cpu = equityCPU(initial_stack=1000)
    cpu.receive_round_start_message(
        dummy_round_start["round_count"],
        dummy_round_start["hole_card"],
        dummy_round_start["seats"]
    )
    assert cpu.round_count == 1
    assert len(cpu.hole_cards) == 2
    assert cpu.seats == dummy_round_start["seats"]


def test_equity_cpu_street_start(dummy_street_start):
    cpu = equityCPU(initial_stack=1000)
    cpu.receive_street_start_message(
        dummy_street_start["street"],
        dummy_street_start["round_state"]
    )
    assert cpu.street == "flop"
    assert len(cpu.community_cards) == 3


def test_equity_cpu_game_update(dummy_game_update):
    cpu = equityCPU(initial_stack=1000)
    cpu.receive_game_update_message(
        dummy_game_update["new_action"],
        dummy_game_update["round_state"]
    )
    assert len(cpu.opponent_actions) == 1
    assert cpu.opponent_actions[0] == dummy_game_update["new_action"]


def test_equity_cpu_round_result(dummy_round_result):
    cpu = equityCPU(initial_stack=1000)
    cpu.receive_round_result_message(
        dummy_round_result["winners"],
        dummy_round_result["hand_info"],
        dummy_round_result["round_state"]
    )
    assert cpu.state == PlayerState.WINNER
    assert cpu.stack == 1200


def test_equity_cpu_count_outs():
    cpu = equityCPU(initial_stack=1000)
    hole_cards = [Card("H", "2"), Card("H", "7")]
    community_cards = [Card("H", "A"), Card("D", "5"), Card("C", "9")]
    outs = cpu.count_outs(hole_cards, community_cards)
    assert isinstance(outs, int)
    assert outs >= 0


def test_pot_odds_cpu_game_start(dummy_game_info):
    cpu = potOddsCPU(initial_stack=1000)
    cpu.receive_game_start_message(dummy_game_info)
    assert cpu.game_info == dummy_game_info
    assert cpu.stack == 1000


def test_pot_odds_cpu_round_start(dummy_round_start):
    cpu = potOddsCPU(initial_stack=1000)
    cpu.receive_round_start_message(
        dummy_round_start["round_count"],
        dummy_round_start["hole_card"],
        dummy_round_start["seats"]
    )
    assert cpu.round_count == 1
    assert len(cpu.hole_cards) == 2
    assert cpu.seats == dummy_round_start["seats"]


def test_pot_odds_cpu_street_start(dummy_street_start):
    cpu = potOddsCPU(initial_stack=1000)
    cpu.receive_street_start_message(
        dummy_street_start["street"],
        dummy_street_start["round_state"]
    )
    assert cpu.street == "flop"
    assert len(cpu.community_cards) == 3


def test_pot_odds_cpu_game_update(dummy_game_update):
    cpu = potOddsCPU(initial_stack=1000)
    cpu.receive_game_update_message(
        dummy_game_update["new_action"],
        dummy_game_update["round_state"]
    )
    assert len(cpu.opponent_actions) == 1
    assert cpu.opponent_actions[0] == dummy_game_update["new_action"]


def test_pot_odds_cpu_round_result(dummy_round_result):
    cpu = potOddsCPU(initial_stack=1000)
    cpu.receive_round_result_message(
        dummy_round_result["winners"],
        dummy_round_result["hand_info"],
        dummy_round_result["round_state"]
    )
    assert cpu.state == PlayerState.WINNER
    assert cpu.stack == 1200


def test_pot_odds_cpu_count_outs():
    cpu = potOddsCPU(initial_stack=1000)
    hole_cards = [Card("H", "2"), Card("H", "7")]
    community_cards = [Card("H", "A"), Card("D", "5"), Card("C", "9")]
    outs = cpu.count_outs(hole_cards, community_cards)
    assert isinstance(outs, int)
    assert outs >= 0


def test_expected_value_cpu_game_start(dummy_game_info):
    cpu = expectedValueCPU(initial_stack=1000)
    cpu.receive_game_start_message(dummy_game_info)
    assert cpu.game_info == dummy_game_info
    assert cpu.stack == 1000


def test_expected_value_cpu_round_start(dummy_round_start):
    cpu = expectedValueCPU(initial_stack=1000)
    cpu.receive_round_start_message(
        dummy_round_start["round_count"],
        dummy_round_start["hole_card"],
        dummy_round_start["seats"]
    )
    assert cpu.round_count == 1
    assert len(cpu.hole_cards) == 2
    assert cpu.seats == dummy_round_start["seats"]


def test_expected_value_cpu_street_start(dummy_street_start):
    cpu = expectedValueCPU(initial_stack=1000)
    cpu.receive_street_start_message(
        dummy_street_start["street"],
        dummy_street_start["round_state"]
    )
    assert cpu.street == "flop"
    assert len(cpu.community_cards) == 3


def test_expected_value_cpu_game_update(dummy_game_update):
    cpu = expectedValueCPU(initial_stack=1000)
    cpu.receive_game_update_message(
        dummy_game_update["new_action"],
        dummy_game_update["round_state"]
    )
    assert len(cpu.opponent_actions) == 1
    assert cpu.opponent_actions[0] == dummy_game_update["new_action"]


def test_expected_value_cpu_round_result(dummy_round_result):
    cpu = expectedValueCPU(initial_stack=1000)
    cpu.receive_round_result_message(
        dummy_round_result["winners"],
        dummy_round_result["hand_info"],
        dummy_round_result["round_state"]
    )
    assert cpu.state == PlayerState.WINNER
    assert cpu.stack == 1200


def test_expected_value_cpu_count_outs():
    cpu = expectedValueCPU(initial_stack=1000)
    hole_cards = [Card("H", "2"), Card("H", "7")]
    community_cards = [Card("H", "A"), Card("D", "5"), Card("C", "9")]
    outs = cpu.count_outs(hole_cards, community_cards)
    assert isinstance(outs, int)
    assert outs >= 0


def test_baseline_cpu_game_start(dummy_game_info):
    cpu = baselineCPU(initial_stack=1000)
    cpu.receive_game_start_message(dummy_game_info)
    assert cpu.game_info == dummy_game_info
    assert cpu.stack == 1000


def test_baseline_cpu_round_start(dummy_round_start):
    cpu = baselineCPU(initial_stack=1000)
    cpu.receive_round_start_message(
        dummy_round_start["round_count"],
        dummy_round_start["hole_card"],
        dummy_round_start["seats"]
    )
    assert cpu.round_count == 1
    assert len(cpu.hole_cards) == 2
    assert cpu.seats == dummy_round_start["seats"]


def test_baseline_cpu_street_start(dummy_street_start):
    cpu = baselineCPU(initial_stack=1000)
    cpu.receive_street_start_message(
        dummy_street_start["street"],
        dummy_street_start["round_state"]
    )
    assert cpu.street == "flop"
    assert len(cpu.community_cards) == 3


def test_baseline_cpu_game_update(dummy_game_update):
    cpu = baselineCPU(initial_stack=1000)
    cpu.receive_game_update_message(
        dummy_game_update["new_action"],
        dummy_game_update["round_state"]
    )
    assert len(cpu.opponent_actions) == 1
    assert cpu.opponent_actions[0] == dummy_game_update["new_action"]


def test_baseline_cpu_round_result(dummy_round_result):
    cpu = baselineCPU(initial_stack=1000)
    cpu.receive_round_result_message(
        dummy_round_result["winners"],
        dummy_round_result["hand_info"],
        dummy_round_result["round_state"]
    )
    assert cpu.state == PlayerState.WINNER
    assert cpu.stack == 1200
