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
    
    def test_next_player(self):
        table = Table()
        table.init_players(1000, 2)

        print("Initially:", table.current_player.name)  # → pc
        table.next_player()
        print("After next_player:", table.current_player.name)  # → cpu1
        table.next_player()
        print("After next_player again:", table.current_player.name)  # → pc
