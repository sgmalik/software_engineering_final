from game_engine.table import Table
class testTable:
    def test_init_players(self):
        
       
       table = Table()

       table.init_players(initial_stack=1000, num_players=2)
       
       assert len(table.players) == 2
       assert table.players[0].stack == 1000
       assert table.players[1].stack == 1000

       assert table.players[0].name == "pc"
       assert table.players[1].name == "cpu1"