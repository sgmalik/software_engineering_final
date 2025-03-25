from game_engine.engine import Engine
from game_engine.constants import PlayerState
from game_engine.constants import Street

class TestEngine: 
    def test_start_game(self):
        """
        start game is expected to initialize players
        and start the game with the preflop street
        """
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
        
       
