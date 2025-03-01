import pypokerengine.utils.visualize_utils as U
from pypokerengine.players import BasePokerPlayer
from Engine import Engine
from time import sleep

class GUIPlayer(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
        #print(U.visualize_declare_action(valid_actions, hole_card, round_state, self.uuid))

        #declare_action is going to be based on the GUI 
        #TODO: get input from GUI and return action and amount
        action = Engine.get_action()
        print(action)
        action, amount = self._receive_action_from_GUI(valid_actions)
        return action, amount

    def receive_game_start_message(self, game_info):
        #print(U.visualize_game_start(game_info, self.uuid))
        sleep(2)


    def receive_round_start_message(self, round_count, hole_card, seats):
        #print(U.visualize_round_start(round_count, hole_card, seats, self.uuid))
        sleep(2)

    def receive_street_start_message(self, street, round_state):
        #print(U.visualize_street_start(street, round_state, self.uuid))
        sleep(2)


    def receive_game_update_message(self, new_action, round_state):
        #print(U.visualize_game_update(new_action, round_state, self.uuid))
        sleep(2)


    def receive_round_result_message(self, winners, hand_info, round_state):
        #print(U.visualize_round_result(winners, hand_info, round_state, self.uuid))
        sleep(2)

    def _wait_until_event(self):
        input("Enter some key to continue ...")
    


    # FIXME: This code would be crash if receives invalid input.
    #        So you should add error handling properly.
    def _receive_action_from_GUI(self, valid_actions):
        action = Engine.get_action()
        if action == 'fold': 
            amount = 0
        if action == 'call':  
            amount = valid_actions[1]['amount']
        if action == 'raise':  
            amount = int(input("Enter raise amount >> "))
        return action, amount
