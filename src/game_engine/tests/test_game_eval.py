from game_engine.game_evaluator import GameEvaluator
from game_engine.engine import Engine
from game_engine.constants import Street

class TestGameEval():
    def test_game_eval(self):
        #init game start preflop 
        engine = Engine(num_players=2, initial_stack=1000, blind=1)
        engine.start_next_round()

        #so, pc blind 1, cpu1 blinds 2. this call will be pc 1
        engine.player_action("call")
        assert engine.dealer.table.pot.value == 4
        assert engine.dealer.table.players[0].stack == 998
        assert engine.dealer.table.players[1].stack == 998

        #flop 
        engine.start_next_street()
        engine.player_action("call")
        assert engine.dealer.table.pot.value == 4
        assert engine.dealer.table.players[0].stack == 998
        assert engine.dealer.table.players[1].stack == 998
        assert engine.dealer.current_street == Street.FLOP
        engine.player_action("call")

        #should be on turn now 
        engine.start_next_street()
        assert engine.dealer.current_street == Street.TURN
        assert len(engine.dealer.table.community_cards) == 4

        #everytime we call twice betting should be over
        engine.player_action("call")
        engine.player_action("call")
        assert engine.dealer.betting_manager.is_betting_over() is True

        engine.start_next_street()
        assert engine.dealer.current_street == Street.RIVER
        assert len(engine.dealer.table.community_cards) == 5
        engine.player_action("call")
        #since player_action calls showdown checking here to see if pot and stacks correct
        assert engine.dealer.table.pot.value == 4
        assert engine.dealer.table.players[0].stack == 998
        assert engine.dealer.table.players[1].stack == 998
        
        engine.player_action("call")
        assert engine.dealer.betting_manager.is_betting_over() is True
        assert engine.dealer.is_round_over() is True

        #game_eval is just returning pc wins for now 
        #check if pot is correct after add_winners. pot would be 4
        assert engine.dealer.table.pot.value == 4
        assert engine.dealer.table.players[0].stack == 1002
        assert engine.dealer.table.players[1].stack == 998
       
        




