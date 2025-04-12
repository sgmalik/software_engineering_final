from game_engine.engine import Engine
from game_engine.constants import PlayerState, Action, Street
from game_engine.cpu.baselineCPU import baselineCPU
from game_engine.card import Card
class TestEngine: 
    def test_start_game(self):
        """
        start game is expected to initialize players
        and start the game with the preflop street
        """
        #init game start preflop 
        engine = Engine(num_players=2, initial_stack=1000, blind=1)

        # initialize the cpu player
        cpu = baselineCPU(initial_stack=1000)
        engine.set_cpu_player(cpu)
        # make sure cpu player overrides the default player
        assert engine.cpu_player is not None
        assert engine.cpu_player == cpu
        assert engine.dealer.table.players[1].name == "baselineCPU"
        assert engine.cpu_player.stack == 1000
        assert engine.cpu_player.state == PlayerState.ACTIVE
        
        engine.start_next_round()

        #make sure dealer is correct
        assert engine.dealer.blind == 1
        assert engine.dealer.initial_stack == 1000
        assert engine.dealer.current_street == Street.PREFLOP

        #betting manager
        assert engine.dealer.betting_manager.blind == 1

        
        #testing blinds adjust players stack correctly
        pc_stack = engine.dealer.table.players[0].stack
        cpu1_stack = engine.dealer.table.players[1].stack
        assert pc_stack == 999
        assert cpu1_stack == 998
        assert engine.dealer.table.pot.value == 3

        #testing if players are initialized correctly
        pc_name = engine.dealer.table.players[0].name
        cpu1_name = engine.dealer.table.players[1].name
        assert pc_name == "pc"
        assert cpu1_name == "baselineCPU"

        #it should be pc's turn after blinds
        assert engine.dealer.table.current_player is not None
        assert engine.dealer.table.current_player.name == "pc"

        #testing if hole cards are dealt correctly
        pc_hole_cards = engine.dealer.table.players[0].hole_cards
        cpu1_hole_cards = engine.dealer.table.players[1].hole_cards

        assert len(pc_hole_cards) == 2
        assert len(cpu1_hole_cards) == 2
    
    def test_current_state_of_game_at_preflop(self):
        """
        current state of game is expected to return a dictionary
        containing the current state of the game
        """
        engine = Engine(num_players=2,initial_stack=1000, blind=1)
        cpu = baselineCPU(initial_stack=1000)
        engine.set_cpu_player(cpu)
        engine.start_next_round()

        state = engine.current_state_of_game()
        
        #test if state is expected at start of preflop (after we started round)
        assert state["players_turn"] is True
        assert state["community_cards"] == []
        assert len(state["players"]) == 2
        assert state["pot"] == 3
        assert state["betting_over"] is False
        assert state["round_over"] is False

        pc = state["players"][0]
        cpu1 = state["players"][1]

        assert pc["name"] == "pc"
        assert pc["stack"] == 999
        assert PlayerState(pc["state"]) == PlayerState.ACTIVE

        assert cpu1["name"] == "baselineCPU"
        assert cpu1["stack"] == 998
        assert PlayerState(cpu1["state"]) == PlayerState.ACTIVE

        
    def test_preflop_betting_round_raises(self):
        """
        test the preflop round of bets
        """
        engine = Engine(num_players=2,initial_stack=1000, blind=1)
        cpu = baselineCPU(initial_stack=1000)
        engine.set_cpu_player(cpu)
        engine.start_next_round()

        # update cpu hole cards to be 2 high cards to force raise behavior
        engine.dealer.table.players[1].hole_cards = [Card("H", "K"), Card("H", "A")]
       

        #pc raises 10
        engine.player_action("raise", 10)
        state = engine.current_state_of_game()

        assert state["players_turn"] is False
        assert state["community_cards"] == []
        assert state["pot"] == 14
        assert state["betting_over"] is False
        assert state["round_over"] is False
        assert state["players"][0]["stack"] == 988

        #cpu1 raises 10
        engine.cpu_action()
        state = engine.current_state_of_game()

        #player turn will be true because cpu1 just did an action
        assert state["players_turn"] is True
        assert state["community_cards"] == []
        assert state["pot"] == 34
        assert state["betting_over"] is False
        assert state["round_over"] is False
        assert state["players"][0]["stack"] == 988
        assert state["players"][1]["stack"] == 978

        #pc calls this 
        engine.player_action("call")
        state = engine.current_state_of_game()

        assert state["players_turn"] is False
        assert state["community_cards"] == []
        assert state["pot"] == 44
        assert state["betting_over"] is True
        assert state["round_over"] is False
        assert state["players"][0]["stack"] == 978
        assert state["players"][1]["stack"] == 978
        
        round_state = engine.build_round_state()

    def test_set_cpu_player(self):
        """
        Test setting a CPU player in the engine
        """
        engine = Engine(num_players=2, initial_stack=1000, blind=1)
        cpu = baselineCPU(initial_stack=1000)
        
        # Set the CPU player
        engine.set_cpu_player(cpu)
        
        # Check that the CPU player was set correctly
        assert engine.cpu_player is not None
        assert engine.cpu_player == cpu
        
        # Check that the CPU player's name was updated in the table
        assert engine.dealer.table.players[1].name == "baselineCPU"
        
        # Check that the CPU player's stack was initialized
        assert cpu.stack == 1000
        assert cpu.state == PlayerState.ACTIVE
        # 2 players in table
        assert len(engine.dealer.table.players) == 2

    def test_build_round_state(self):
        """
        Test building the round state for CPU players
        """
        engine = Engine(num_players=2, initial_stack=1000, blind=1)
        engine.start_next_round()
        
        # Build the round state
        round_state = engine.build_round_state()
        
        # Check the structure of the round state
        assert "street" in round_state
        assert round_state["street"] == "preflop"
        assert "next_player" in round_state
        assert "blind_pos" in round_state
        assert "community_card" in round_state
        assert round_state["community_card"] == []
        assert "pot" in round_state
        assert "main" in round_state["pot"]
        assert round_state["pot"]["main"] == 3
        assert "seats" in round_state
        assert len(round_state["seats"]) == 2
        assert "action_histories" in round_state
        assert "preflop" in round_state["action_histories"]
        assert "flop" in round_state["action_histories"]
        assert "turn" in round_state["action_histories"]
        assert "river" in round_state["action_histories"]

    def test_cpu_action(self):
        """
        Test that the CPU player can make an action
        """
        engine = Engine(num_players=2, initial_stack=1000, blind=1)
        cpu = baselineCPU(initial_stack=1000)
        engine.set_cpu_player(cpu)
        engine.start_next_round()

        # update cpu hole cards to be 1 high card to force call behavior
        engine.dealer.table.players[1].hole_cards = [Card("H", "K"), Card("H", "2")]
        
        # Player raises, so it's CPU's turn
        engine.player_action("raise", 10)
        
        # CPU should make an action
        engine.cpu_action()
        
        # Check that the CPU made an action
        state = engine.current_state_of_game()
        assert state["players_turn"] is True  # It should be player's turn again
        assert state["pot"] > 14  # Pot should have increased
        assert state["players"][1]["stack"] < 998  # CPU's stack should have decreased

    def test_action_histories_in_round_state(self):
        """
        Test that action histories are properly added to the round state
        """
        # Initialize game
        engine = Engine(num_players=2, initial_stack=1000, blind=1)
        engine.start_next_round()
        
        # Perform some actions in preflop
        engine.player_action("raise", 10)
        engine.cpu_action()  # CPU should call or raise
        
        # Get the round state
        round_state = engine.build_round_state()
        
        # Check that action histories are included in the round state
        assert "action_histories" in round_state
        assert "preflop" in round_state["action_histories"]
        
        # Check that the preflop actions are recorded
        preflop_actions = round_state["action_histories"]["preflop"]
        assert len(preflop_actions) >= 2  # At least the blinds and our raise
        
        # Check that the actions have the correct structure
        for action in preflop_actions:
            assert "name" in action
            assert "action" in action
            assert "amount" in action
        
        # Move to the next street (flop)
        engine.start_next_street()
        
        # Get the round state again
        round_state = engine.build_round_state()
        
        # Check that preflop actions are still in the round state
        assert "preflop" in round_state["action_histories"]
        assert len(round_state["action_histories"]["preflop"]) >= 2
        
        # Check that flop actions are empty (since we just started flop)
        assert "flop" in round_state["action_histories"]
        assert len(round_state["action_histories"]["flop"]) == 0
