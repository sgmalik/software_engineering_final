import pytest
from game_engine.constants import PlayerState
from game_engine.cpu.equityCPU import equityCPU
from game_engine.cpu.expectedValueCPU import expectedValueCPU
from game_engine.cpu.potOddsCPU import potOddsCPU
from game_engine.cpu.baselineCPU import baselineCPU
from game_engine.card import Card
from game_engine.engine import Engine
from game_engine.cpu.mlCPU import MLCPU
from game_engine.cpu.mlCPU import parse_card_str
import tempfile
import os
from game_engine.constants import Action, Street

@pytest.fixture
def dummy_round_state():
    return {
        "community_card": ["AH", "5D", "9C"],
        "pot": {"main": 200, "side": []},
        "action_histories": {},
        "seats": [
            {"name": "player1", "stack": 800, "state": "participating"},
            {"name": "cpu", "stack": 1200, "state": "participating"},
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
    return ["2H", "7H"]


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
            {"name": "cpu", "stack": 1000}
        ]
    }


@pytest.fixture
def dummy_round_start():
    return {
        "round_count": 1,
        "hole_card": ["2H", "7H"],
        "seats": [
            {"name": "player1", "stack": 1000, "state": "participating"},
            {"name": "cpu", "stack": 1000, "state": "participating"}
        ]
    }


@pytest.fixture
def dummy_street_start():
    return {
        "street": "flop",
        "round_state": {
            "community_card": ["AH", "5D", "9C"],
            "pot": {"main": 200, "side": []},
            "action_histories": {},
            "seats": [
                {"name": "player1", "stack": 800, "state": "participating"},
                {"name": "cpu", "stack": 1200, "state": "participating"},
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
            "community_card": ["AH", "5D", "9C"],
            "pot": {"main": 200, "side": []},
            "action_histories": {},
            "seats": [
                {"name": "player1", "stack": 800, "state": "participating"},
                {"name": "cpu", "stack": 1200, "state": "participating"},
            ],
        }
    }


@pytest.fixture
def dummy_round_result():
    return {
        "winners": [{"name": "cpu"}],
        "hand_info": {
            "player1": {"hand": ["2H", "7H"], "hand_rank": "high_card"},
            "cpu": {"hand": ["AH", "5D"], "hand_rank": "pair"}
        },
        "round_state": {
            "community_card": ["AH", "5D", "9C"],
            "pot": {"main": 200, "side": []},
            "action_histories": {},
            "seats": [
                {"name": "player1", "stack": 800, "state": "active"},
                {"name": "cpu", "stack": 1200, "state": "winner"},
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


def test_ml_cpu_action(dummy_valid_actions, dummy_hole_cards, dummy_round_state):
    """
    Test that the MLCPU can make decisions based on the current game state.
    """
    
    # Create an MLCPU with a small initial stack
    ml_cpu = MLCPU(initial_stack=1000)
    
    # Add hole cards to the CPU
    ml_cpu.add_hole_card([parse_card_str(card) for card in dummy_hole_cards])
    
    # Get the action from the CPU
    action, amount = ml_cpu.declare_action(dummy_valid_actions, dummy_hole_cards, dummy_round_state)
    
    # Verify that the action is valid
    assert action in ["fold", "call", "raise"]
    assert amount >= 0


def test_ml_cpu_model_creation():
    """Test that MLCPU creates and saves a model after playing multiple rounds."""
    # Use the project's models directory
    model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "models", "ml_cpu_model.pkl")
    
    # Create models directory if it doesn't exist
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    # Initialize engine and CPU
    engine = Engine(num_players=2, initial_stack=1000, blind=10)
    cpu = MLCPU(initial_stack=1000, model_path=model_path)
    engine.set_cpu_player(cpu)

    # Play multiple rounds to ensure model is saved
    for _ in range(15):
        # Start a new round
        engine.dealer.set_up_next_round()
        engine.dealer.start_street()

        # Send game start message to CPU
        cpu.receive_game_start_message({
            'rule': {'initial_stack': 1000},
            'seats': [{'name': 'pc', 'stack': 1000}, {'name': 'MLCPU', 'stack': 1000}]
        })

        # Send round start message to CPU
        cpu.receive_round_start_message(1, ['AH', 'KH'], [
            {'name': 'pc', 'stack': 1000},
            {'name': 'MLCPU', 'stack': 1000}
        ])

        # Pre-flop
        engine.dealer.betting_manager.reset_betting_round()
        engine.dealer.betting_manager.apply_player_action(engine.dealer.table.players[0], Action.SMALL_BLIND)
        engine.dealer.betting_manager.apply_player_action(engine.dealer.table.players[1], Action.BIG_BLIND)

        # Let CPU make its decision
        round_state = engine.build_round_state()
        valid_actions = [
            {'action': 'fold', 'amount': 0},
            {'action': 'call', 'amount': 10},
            {'action': 'raise', 'amount': {'min': 20, 'max': 1000}}
        ]
        action, amount = cpu.declare_action(valid_actions, ['AH', 'KH'], round_state)
        
        # Make sure the player is in the pending_betters list before applying action
        if engine.dealer.table.players[1] not in engine.dealer.betting_manager.pending_betters:
            engine.dealer.betting_manager.pending_betters.append(engine.dealer.table.players[1])
            
        engine.dealer.betting_manager.apply_player_action(engine.dealer.table.players[1], Action(action), amount)

        # Send street start message to CPU
        cpu.receive_street_start_message('flop', round_state)

        # Flop
        engine.dealer.next_street()
        engine.dealer.start_street()
        engine.dealer.betting_manager.reset_betting_round()

        # Let CPU make its decision
        round_state = engine.build_round_state()
        valid_actions = [
            {'action': 'check', 'amount': 0},
            {'action': 'raise', 'amount': {'min': 10, 'max': 1000}}
        ]
        action, amount = cpu.declare_action(valid_actions, ['AH', 'KH'], round_state)
        
        # Make sure the player is in the pending_betters list before applying action
        if engine.dealer.table.players[1] not in engine.dealer.betting_manager.pending_betters:
            engine.dealer.betting_manager.pending_betters.append(engine.dealer.table.players[1])
            
        engine.dealer.betting_manager.apply_player_action(engine.dealer.table.players[1], Action(action), amount)

        # Send round result message to CPU
        cpu.receive_round_result_message(
            [{'name': 'MLCPU', 'stack': 1100}],
            {'hand_rank': 2, 'primary_cards_rank': [14, 13], 'kickers': []},
            {'seats': [{'name': 'pc', 'stack': 900}, {'name': 'MLCPU', 'stack': 1100}]}
        )

    # Save the model
    cpu.save_model(model_path)

    # Verify model was created and is not empty
    assert os.path.exists(model_path)
    assert os.path.getsize(model_path) > 0

    # Load the model and verify Q-table
    new_cpu = MLCPU(initial_stack=1000, model_path=model_path)
    assert len(new_cpu.q_table) > 0

def test_ml_cpu_decision_making():
    """
    Test that the MLCPU can make decisions based on the current game state.
    """

    # Create a temporary directory for the model
    with tempfile.TemporaryDirectory() as temp_dir:
        model_path = os.path.join(temp_dir, "ml_cpu_model.pkl")
        
        # Create an MLCPU with the temporary model path
        ml_cpu = MLCPU(initial_stack=1000, model_path=model_path)
        
        # Add some hole cards
        hole_cards = [parse_card_str("AH"), parse_card_str("KH")]
        ml_cpu.add_hole_card(hole_cards)
        
        # Create a round state
        round_state = {
            "street": "preflop",
            "next_player": 1,
            "small_blind_pos": 0,
            "big_blind_pos": 1,
            "community_card": [],
            "pot": {
                "main": 30,
                "side": []
            },
            "seats": [
                {
                    "name": "Player1",
                    "stack": 970,
                    "state": "participating"
                },
                {
                    "name": "ml_cpu",
                    "stack": 1000,
                    "state": "participating"
                }
            ],
            "action_histories": {
                "preflop": [
                    {"name": "Player1", "action": "small_blind", "amount": 10},
                    {"name": "ml_cpu", "action": "big_blind", "amount": 20},
                    {"name": "Player1", "action": "raise", "amount": 30}
                ],
                "flop": [],
                "turn": [],
                "river": []
            }
        }
        
        # Create valid actions
        valid_actions = [
            {"action": "fold", "amount": 0},
            {"action": "call", "amount": 30},
            {"action": "raise", "amount": {"min": 60, "max": 1000}},
            {"action": "check", "amount": 0},
        ]
        
        # Get the action from the MLCPU
        action, amount = ml_cpu.declare_action(valid_actions, ["AH", "KH"], round_state)
        
        # Verify that the action is valid
        assert action in ["fold", "call", "raise", "check"], f"Invalid action: {action}"
        
        # Verify that the amount is valid
        if action == "fold":
            assert amount == 0, "Fold action should have amount 0"
        elif action == "call":
            assert amount == 30, "Call action should have amount 30"
        elif action == "raise":
            assert amount >= 60 and amount <= 1000, f"Raise amount {amount} is out of range"
        elif action == "check":
            assert amount == 0, "Check action should have amount 0"

def test_ml_cpu_load_model():
    """Test that MLCPU can load a model from the models directory and it contains data."""
    # Path to the model file
    model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "models", "ml_cpu_model.pkl")
    
    # Check if the model file exists
    if not os.path.exists(model_path):
        pytest.skip("Model file does not exist. Run test_ml_cpu_model_creation first.")
    
    # Load the model
    cpu = MLCPU(initial_stack=1000, model_path=model_path)
    
    # Verify the Q-table is loaded and contains data
    assert len(cpu.q_table) > 0, "Q-table is empty"
    
    # Verify the Q-table has some non-zero values
    has_non_zero_values = False
    for state_action, q_value in cpu.q_table.items():
        if q_value != 0:
            has_non_zero_values = True
            break
    
    assert has_non_zero_values, "Q-table contains only zero values"
    
    # Verify the model can make decisions
    valid_actions = [
        {'action': 'fold', 'amount': 0},
        {'action': 'call', 'amount': 10},
        {'action': 'raise', 'amount': {'min': 20, 'max': 1000}},
        {'action': 'check', 'amount': 0}
    ]
    
    # Create a simple round state
    round_state = {
        'street': 'preflop',
        'pot': {'main': 30},
        'community_card': [],
        'seats': [
            {'name': 'pc', 'stack': 1000, 'state': 'participating'},
            {'name': 'MLCPU', 'stack': 1000, 'state': 'participating'}
        ]
    }
    
    # Get an action from the model
    action, amount = cpu.declare_action(valid_actions, ['AH', 'KH'], round_state)
    
    # Verify the action is valid
    assert action in ['fold', 'call', 'raise', 'check'], f"Invalid action: {action}"
    assert amount >= 0, f"Invalid amount: {amount}"
