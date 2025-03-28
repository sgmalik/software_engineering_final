"""
tests for dealer class: most of these tests are assuming only two players
"""
from game_engine.dealer import Dealer
from game_engine.constants import PlayerState, Action


class TestDealer:
    """
    methods are tests for dealer
    """

    def test_apply_player_action_raise(self):
        """
        simple raise test seeing if values are changed as expected
        """

        dealer = Dealer(small_blind=1, initial_stack=1000)
        table = dealer.table

        table.init_players(initial_stack=1000, num_players=2)

        # raise 10
        dealer.apply_action(Action.RAISE, 10)

        assert table.players[0].stack == 990

        assert dealer.betting_manager.current_bet == 10
        assert dealer.table.pot.value == 10

    def test_two_raises(self):
        """
        raising twice to test current_bet is working as expected
        """
        dealer = Dealer(small_blind=1, initial_stack=1000)
        table = dealer.table

        table.init_players(initial_stack=1000, num_players=2)

        # pc raises 10
        assert dealer.betting_manager.current_bet == 0
        dealer.apply_action(Action.RAISE, 10)
        assert dealer.betting_manager.current_bet == 10

        # make next player does its job
        assert table.current_player.name == "cpu1"

        # cpu1 calls 10, and raises 20 so should be -30
        dealer.apply_action(Action.RAISE, 20)

        assert table.players[0].stack == 990
        assert table.players[1].stack == 970
        assert dealer.betting_manager.current_bet == 30
        assert dealer.table.pot.value == 40

    def test_check(self):
        """
        test checking when initial blinds are done
        """
        dealer = Dealer(small_blind=1, initial_stack=1000)
        table = dealer.table

        table.init_players(initial_stack=1000, num_players=2)

        # start preflop
        dealer.start_street()
        # after blinds current_bet should be 2
        assert dealer.betting_manager.current_bet == 2
        assert dealer.betting_manager.pending_betters == table.active_players()

        # after blinds its pc's turn
        assert dealer.table.current_player.name == "pc"

        dealer.apply_action(Action.CALL)
        dealer.apply_action(Action.CALL)

        # stacks and pot are after two blinds (blind_pos starts with p1)
        # so p1 pays 1, p2 pays 2, they both call 2
        assert table.players[0].stack == 998
        assert table.players[1].stack == 998
        assert dealer.table.pot.value == 4

    def test_contribution(self):
        """
        test raising when a player has already raised 
        in the current betting round (meaning they shouldn't pay
        all of current_bet) based on contribuition on the current street
        """
        dealer = Dealer(small_blind=1, initial_stack=1000)
        table = dealer.table

        table.init_players(initial_stack=1000, num_players=2)

        dealer.apply_action(Action.RAISE, 10)
        dealer.apply_action(Action.RAISE, 20)
        dealer.apply_action(Action.CALL)

        pc = dealer.table.players[0]
        cpu1 = dealer.table.players[1]

        assert pc.stack == 970
        assert cpu1.stack == 970

        assert pc.contribuition == 30
        assert cpu1.contribuition == 30
        assert dealer.table.pot.value == 60

    def test_is_betting_over(self):
        """
        check if betting is over works as expected at multiple points in a round
        """
        dealer = Dealer(small_blind=1, initial_stack=1000)
        table = dealer.table
        table.init_players(initial_stack=1000, num_players=2)

        dealer.start_street()
        assert dealer.betting_manager.is_betting_over() is False

        # if player 1 raises, and then p2 calls then betting for the street is over
        dealer.apply_action(Action.RAISE, 100)
        dealer.apply_action(Action.CALL)
        assert dealer.betting_manager.is_betting_over() is True

        # go to next street betting should begin
        dealer.next_street()
        dealer.start_street()
        assert dealer.betting_manager.is_betting_over() is False

        dealer.apply_action(Action.CALL)
        dealer.apply_action(Action.CALL)
        assert dealer.betting_manager.is_betting_over() is True

        # if both players raise betting should not be over
        dealer.next_street()
        dealer.start_street()
        dealer.apply_action(Action.RAISE, 10)
        dealer.apply_action(Action.RAISE, 10)
        assert dealer.betting_manager.is_betting_over() is False

        # if player raise's again we are still betting
        dealer.apply_action(Action.RAISE, 30)
        assert dealer.betting_manager.is_betting_over() is False

        # if player calls after the raise we are done betting
        dealer.apply_action(Action.CALL)
        assert dealer.betting_manager.is_betting_over() is True

    def test_is_betting_over_fold(self):
        """
        this fails but I think I dont want is_betting_over
        to check if all but one has folded, that will be something 
        like is_round_over
        """

        dealer = Dealer(small_blind=1, initial_stack=1000)
        table = dealer.table

        table.init_players(initial_stack=1000, num_players=2)
        dealer.start_street()

        # if one player folds betting is over, and the round is over
        dealer.apply_action(Action.FOLD)
        assert dealer.betting_manager.is_betting_over() is True

    def test_is_round_over_fold(self):
        """
        test if round is over when 1 player folds 
        """
        dealer = Dealer(small_blind=1, initial_stack=1000)
        table = dealer.table

        table.init_players(initial_stack=1000, num_players=2)
        dealer.start_street()

        dealer.apply_action(Action.FOLD)
        assert dealer.is_round_over() is True

    def test_round_over_river(self):
        """
        go through all the streets and call is round_over at the end
        """
        dealer = Dealer(small_blind=1, initial_stack=1000)
        table = dealer.table

        table.init_players(initial_stack=1000, num_players=2)

        # start preflop
        dealer.start_street()

        # preflop betting
        dealer.apply_action(Action.RAISE, 10)
        dealer.apply_action(Action.CALL)

        assert table.players[0].stack == 988
        assert dealer.table.pot.value == 24
        assert dealer.is_round_over() is False

        # flop
        dealer.next_street()
        dealer.start_street()
        dealer.apply_action(Action.RAISE, 10)
        dealer.apply_action(Action.CALL)

        assert dealer.table.pot.value == 44
        assert dealer.is_round_over() is False
        # turn
        dealer.next_street()
        dealer.start_street()
        dealer.apply_action(Action.RAISE, 10)
        dealer.apply_action(Action.CALL)

        assert dealer.is_round_over() is False

        # river
        dealer.next_street()
        dealer.start_street()
        dealer.apply_action(Action.RAISE, 10)
        dealer.apply_action(Action.CALL)

        assert dealer.is_round_over() is True
        assert dealer.table.pot.value == 84
