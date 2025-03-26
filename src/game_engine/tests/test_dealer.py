from game_engine.dealer import Dealer
from game_engine.constants import PlayerState, Action
class TestDealer:
          
    def test_apply_player_action_raise(self):
       dealer = Dealer(small_blind=1, initial_stack=1000)
       table = dealer.table

       table.init_players(initial_stack=1000, num_players=2)

       #raise 10 
       dealer.apply_player_action(Action.RAISE, 10)
        
       assert table.players[0].stack == 990
       
       assert dealer.current_bet == 10
       assert dealer.pot == 10
