from game_engine.engine import Engine
from game_engine.constants import PlayerState
from game_engine.constants import Street

class TestEngine: 
    def test_start_game(self):
        engine = Engine(num_players=2,initial_stack=1000, blind=1)
        engine.start_game()

        #
        expected_state = {
            "street": Street.PREFLOP,
            "community_cards": [],
            "players": [
                {
                    "name": "pc",
                    "stack": 1000,
                    "hole_cards": [],
                    "state": PlayerState.ACTIVE
                },
                {
                    "name": "cpu1",
                    "stack": 1000,
                    "hole_cards": [],
                    "state": PlayerState.ACTIVE
                }
            ]
         }
        
        assert engine.current_state_of_game() == expected_state
       
