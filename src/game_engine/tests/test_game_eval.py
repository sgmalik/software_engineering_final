from game_engine.game_evaluator import GameEvaluator
from game_engine.engine import Engine
from game_engine.constants import Street
from game_engine.card import Card
from game_engine.dealer import Dealer

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

        #NOTE: can't really assert stacks because can tie, or 1 player wins

        #can't assert stacks because pc or cpu1 could win
    def test_determine_winners(self):
        """
        basic test, going to manually change Table and players to check if winners are correct
        """
        dealer = Dealer(1000, 1)
        table = dealer.table

        #with these cards you would expect pc to win (high card)
        pc_hole_cards = [
            Card('H', '2'),
            Card('D', '5'),
        ]

        cpu1_hole_cards = [
            Card('H', '8'),
            Card('D', '4'),
        ]

        community_cards = [
            Card('S', '9'),
            Card('C', 'J'),
            Card('H', 'Q'),
            Card('S', '3'),
            Card('D', '7'),
        ]

        table.players[0].hole_cards = pc_hole_cards
        table.players[1].hole_cards = cpu1_hole_cards
        table.community_cards = community_cards

        #will just say pot is 20 (even though no bets were made)
        table.pot.value = 20
        winners = GameEvaluator.determine_winners(table)

        #should be pc with high card 
        assert winners == [table.players[0]]

        #and then pot should be added to pc stack
        GameEvaluator.add_money_to_winners(table, winners)
        assert table.players[0].stack == 1020
        assert table.players[1].stack == 1000

    def test_determine_winners_tie(self):
            """
            test if we have a tie between two players
            """
            dealer = Dealer(1000, 1)
            table = dealer.table

            #with these cards you would expect pc to win (high card)
            pc_hole_cards = [
                Card('H', '2'),
                Card('D', '5'),
            ]

            cpu1_hole_cards = [
                Card('S', '2'),
                Card('C', '5'),
            ]

            community_cards = [
                Card('S', '9'),
                Card('C', 'J'),
                Card('H', 'Q'),
                Card('S', '3'),
                Card('D', '7'),
            ]

            table.players[0].hole_cards = pc_hole_cards
            table.players[1].hole_cards = cpu1_hole_cards
            table.community_cards = community_cards

            #will just say pot is 20 (even though no bets were made)
            table.pot.value = 20
            winners = GameEvaluator.determine_winners(table)

            #should be a tie so both players in winner array 
            assert winners == [table.players[0], table.players[1]]

            GameEvaluator.add_money_to_winners(table, winners)
            assert table.players[0].stack == 1010
            assert table.players[1].stack == 1010



       
        




