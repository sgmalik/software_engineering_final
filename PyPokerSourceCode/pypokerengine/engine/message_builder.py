from pypokerengine.engine.data_encoder import DataEncoder
from pypokerengine.engine.action_checker import ActionChecker

class MessageBuilder:

  GAME_START_MESSAGE = "game_start_message"
  ROUND_START_MESSAGE = "round_start_message"
  STREET_START_MESSAGE = "street_start_message"
  ASK_MESSAGE = "ask_message"
  GAME_UPDATE_MESSAGE = "game_update_message"
  ROUND_RESULT_MESSAGE = "round_result_message"
  GAME_RESULT_MESSAGE = "game_result_message"

  @classmethod
  def build_game_start_message(cls, config, seats):
    message = {
        "message_type": cls.GAME_START_MESSAGE,
        "game_information": DataEncoder.encode_game_information(config, seats)
    }
    return cls.__build_notification_message(message)

  @classmethod
  def build_round_start_message(cls, round_count, player_pos, seats):
    player = seats.players[player_pos]
    hole_card = DataEncoder.encode_player(player, holecard=True)["hole_card"]
    message = {
        "message_type": cls.ROUND_START_MESSAGE,
        "round_count": round_count,
        "hole_card": hole_card
    }
    message.update(DataEncoder.encode_seats(seats))
    return cls.__build_notification_message(message)

  @classmethod
  def build_street_start_message(cls, state):
    message = {
        "message_type": cls.STREET_START_MESSAGE,
        "round_state": DataEncoder.encode_round_state(state)
        }
    message.update(DataEncoder.encode_street(state["street"]))
    return cls.__build_notification_message(message)

  @classmethod
  def build_ask_message(cls, player_pos, state):
    players = state["table"].seats.players
    player = players[player_pos]
    hole_card = DataEncoder.encode_player(player, holecard=True)["hole_card"]
    valid_actions = ActionChecker.legal_actions(players, player_pos, state["small_blind_amount"])
    message = {
        "message_type" : cls.ASK_MESSAGE,
        "hole_card": hole_card,
        "valid_actions": valid_actions,
        "round_state": DataEncoder.encode_round_state(state),
        "action_histories": DataEncoder.encode_action_histories(state["table"])
    }
    return cls.__build_ask_message(message)

  @classmethod
  def build_game_update_message(cls, player_pos, action, amount, state):
    player = state["table"].seats.players[player_pos]
    message = {
        "message_type": cls.GAME_UPDATE_MESSAGE,
        "action": DataEncoder.encode_action(player, action, amount),
        "round_state": DataEncoder.encode_round_state(state),
        "action_histories": DataEncoder.encode_action_histories(state["table"])
    }
    return cls.__build_notification_message(message)

  @classmethod
  def build_round_result_message(cls, round_count, winners, hand_info, state):
    message = {
        "message_type": cls.ROUND_RESULT_MESSAGE,
        "round_count": round_count,
        "hand_info"  : hand_info,
        "round_state": DataEncoder.encode_round_state(state)
    }
    message.update(DataEncoder.encode_winners(winners))
    return cls.__build_notification_message(message)

  @classmethod
  def build_game_result_message(cls, config, seats):
    message = {
      "message_type": cls.GAME_RESULT_MESSAGE,
      "game_information": DataEncoder.encode_game_information(config, seats)
    }
    return cls.__build_notification_message(message)


  @classmethod
  def __build_ask_message(cls, message):
    return {
        "type": "ask",
        "message": message
    }

  @classmethod
  def __build_notification_message(cls, message):
    return {
        "type": "notification",
        "message": message
    }
