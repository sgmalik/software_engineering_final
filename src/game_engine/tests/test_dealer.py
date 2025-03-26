from game_engine.dealer import Dealer
from game_engine.constants import PlayerState, Action
class TestDealer:
    

    #simple raise test seeing if values are cahnged as expected
    def test_apply_player_action_raise(self):
       dealer = Dealer(small_blind=1, initial_stack=1000)
       table = dealer.table

       table.init_players(initial_stack=1000, num_players=2)

       #raise 10 
       dealer.apply_player_action(Action.RAISE, 10)
        
       assert table.players[0].stack == 990
       
       assert dealer.current_bet == 10
       assert dealer.pot == 10
    
    def test_multiple_raises(self):
        dealer = Dealer(small_blind=1, initial_stack=1000)
        table = dealer.table

        table.init_players(initial_stack=1000, num_players=2)

        #pc raises 10
        assert dealer.current_bet == 0
        dealer.apply_player_action(Action.RAISE, 10)
        assert dealer.current_bet == 10
        dealer.table.next_player()

        assert table.current_player.name == "cpu1"
        
        #cpu1 calls 10, and raises 20 so should be -30
        dealer.apply_player_action(Action.RAISE, 20)
        
        assert table.players[0].stack == 990
        assert table.players[1].stack == 970
        assert dealer.current_bet == 30
        assert dealer.pot == 40

