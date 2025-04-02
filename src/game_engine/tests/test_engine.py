from game_engine.engine import Engine
from game_engine.constants import PlayerState
from game_engine.constants import Street

class TestEngine: 
    def test_start_game(self):
        """
        start game is expected to initialize players
        and start the game with the preflop street
        """
        #init game start preflop
        engine = Engine(num_players=2,initial_stack=1000, blind=1)
        engine.start_game()

        
        #testing blinds adjust players stack correctly
        pc_stack = engine.dealer.table.players[0].stack
        cpu1_stack = engine.dealer.table.players[1].stack
        assert pc_stack == 999
        assert cpu1_stack == 998

        #testing if players are initialized correctly
        pc_name = engine.dealer.table.players[0].name
        cpu1_name = engine.dealer.table.players[1].name
        assert pc_name == "pc"
        assert cpu1_name == "cpu1"
        
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
        engine.start_game()

        state = engine.current_state_of_game()
        
        #test if state is expected at start of preflop (after we started round)
        assert state["players_turn"] is True
        assert state["community_cards"] == []
        assert len(state["players"]) == 2

        pc = state["players"][0]
        cpu1 = state["players"][1]

        assert pc["name"] == "pc"
        assert pc["stack"] == 999
        assert pc["hole_cards"] == engine.dealer.table.players[0].hole_cards
        assert pc["state"] == PlayerState.ACTIVE

        assert cpu1["name"] == "cpu1"
        assert cpu1["stack"] == 998
        assert cpu1["hole_cards"] == engine.dealer.table.players[1].hole_cards
        assert cpu1["state"] == PlayerState.ACTIVE

        
    def test_preflop_betting_round(self):
        """
        test the preflop round of bets
        """
        engine = Engine(num_players=2,initial_stack=1000, blind=1)
        engine.start_game()

        #after blinds current player should be pc (index 0)
        assert engine.dealer.table.current_player == 0

        engine.player_action("check")
