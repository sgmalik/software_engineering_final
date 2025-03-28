## hand_evaluator 
the HandEvaluator class provides information on the strength of a poker hand. 

To use HandEvaluator you would call the hand_eval function like so: 
```
hand_info = HandEvaluator.hand_eval(hole_cards, community_cards)
```
You would then get an object like this: 
```
{
    "strength": {
        "hand_rank": Int,
        "primary_cards_rank": []
    },
        "kickers": []
}
```
**hand_rank**: the rank of the hand given (Ex. high_card, pair, two pair, etc). This is on a 1-10 scale (high_card being 1, royal_flush being a 10)

**primary_cards_rank**: these are used for tie breaking the same hand_rank, Ex. the hand is a pair of 2's.
```
hand_info["strength"]["primary_cards_rank"] = [2]
```

**kickers**: the kickers are also used for tie-breaking, these are the highest ranked individual cards (2-14) that aren't used in hand_rank or primary_cards_rank 
## game_evaluator


## dealer:
dealer manages the state of streets, keeps tracks of bets using BettingManager. 

**apply_action**: this function is a wrapper for bettingManager's apply_action and has two paramaters
    * action: the action to apply (raise,,fold, call)
    * raise_amount: optional parameter, only used when increasing the bet 

**is_round_over**: returns True if the round has concluded (if all but one player has folded, or river street has concluded). This will be called in game_engine to pass information to the GUI

### Street management: 
*untested* 
**start_street** this function starts the current street (preflop, flop, turn, river). This should be called in game_engine when the betting round is over.
**next_street** change street state to the next street. 

the reason these two are seperate functions is because we need to check if the street is over (betting is over) before going onto the next street.


## BettingManager
the purpose of betting manager, is to track pending_betters (who is still in the hand) as well as update table information based on player action.

**apply_action**: function that calls the player action, and applys it to player and table information.
    Ex. big blind you would update, the pot, player contribuition, current_bet 

**pending_betters**: this is an array which incombination with helper functions keeps track of who is still in the round.
    * if a player raises, all other players need to respond to the bet so they are added to this array 
    * if a player calls they are taken out of the array (they have responded to the bet)
    * only active players can be in the array, if a player folds they are taken out

**is_betting_over**: returns a boolean value. If true the betting round is over. This is used in game_engine to check if we should move onto a new street. 


## Table
table keeps track of players, deck, and holds the pot. It has methods to deal cards as well. 

**init__players** player's need to be initialized. 
**next_player** set's tables current player to the next player (currently only working for 1v1)
**players_turn**: to be used in game_engine so the GUI knows when its the players turn 
**active_players**: returns an array of all the players that are active in a hand 


## Engine
**currently unimplemented** 

the Engine class works as an inbetween between the GUI and our game logic. Ideally, the only functions that will be called from the GameEngine will
be current_state_of_the_game which will use (dealer,player,game_eval,hand_eval, etc) to return an object containing all the information the GUI needs. A start street wrapper 
function and a next_street wrapper. As well as functions to start a round, and start game. 

Most of the information that GUI gets should be from current_state_of_the_game, and this object shouldn't contain any classes that we use in game_engine. It should 
be a string representation of the state of the game. 


