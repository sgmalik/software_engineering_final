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
        engine = Engine(num_players=2, initial_stack=1000, blind=1)
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
        assert cpu1_name == "cpu1"

        #it should be pc's turn after blinds
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
        assert pc["state"] == PlayerState.ACTIVE

        assert cpu1["name"] == "cpu1"
        assert cpu1["stack"] == 998
        assert cpu1["state"] == PlayerState.ACTIVE

        
    def test_preflop_betting_round_raises(self):
        """
        test the preflop round of bets
        """
        engine = Engine(num_players=2,initial_stack=1000, blind=1)
        engine.start_next_round()
       

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
        engine.player_action("raise", 10)
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

        
        
