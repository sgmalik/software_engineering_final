# General Thoughts:

## GUI:

- Start screen: prompt the user for difficulty, starting stack, and blind structure (preset options for all of these)
- Game screen:
  - Show just green background with button that says 'start game'
  - When button is clicked, show screen that James sent in chat, cards showing
  - if user's turn, display buttons for betting actions, otherwise don't
  - timer for cpu to make a move, simulate slower action
  - show pot size in empty space
  - after preflop, if game still active, display button for next street
  - basically repeat the last 4 bullets for each street
  - when showdown occurs, flip cpu cards, simulate a pause, and show the result of the hand evaluation, and update stack amounts visually
  - continue this for each hand (user specifies number of hands most likely, idk)
  - if the game is over, display screen that shows result of the game: user stack amount, cpu stack amount, how many hands were played, button to play again, button to go to start screen (game structure screen), and button to close the game
  **Not sure if this is feasible but this is what I had in mind for the GUI**

## Game Logic:

- Make use of the PyPokerEngine library when we need to, for example:
    - Utilize PyPokerEngine BasePokerPlayer class to create our cpu
        - the reason we are doing this and not adapting the class is because in order to make our cpu better utilizing reinforcement learning, we should make use of the `emulator` module within PyPokerEngine which allows us to simulate games and train our cpu
    - Utilize PyPokerEngine Emulator class to simulate games as previously discussed
    - Make use of game state logic to determine whether game is still active or not, what valid actions are, etc.
    - Reference the code for relevant logic we'd need to implement 
- Setup game engine class:
    - using the `setup_config` function as a baseline, based on the user's input on the gui, we will define a function that sets up the game with the desired structure
    - When the user presses the shuffle and start button, this will trigger a some workflow that runs the game. 
    - This will be responsible for shuffling the deck, dealing the cards, and then simulating the game.
    - Within this, we will need to do the following probably using a lot of helper functions similar to PyPokerEngine:
        - Keep track of the state of the hand, preflop, flop, turn, river, showdown, who's turn it is, what the pot size is, etc.
        - keep track of the state of the player, what their stack is, what their valid actions are, past decisions on previous streets, etc.
        - keep track of the state of the cpu, what their stack is, what their valid actions are, past decisions on previous streets, etc.
        - keep track of the state of the deck, what cards are in it, what cards are dealt, what cards are the community cards, etc.
        - if we are limiting the number of hands, we need to keep track of the number of hands played, etc.
        - if the game is over, we need to display the result of the game
    
    **Luckily, if we make use of the PyPokerEngine BasePokerPlayer class for our cpu, we are <bold>required</bold> to implement the following functions:**
    **need to double check if we can overwrite what exactly each function requires parameter wise**
    - `declare_action`: takes in valid_actions, hold_card, and round_state and returns the cpu's action
        - here is where we implement some sort of logic/strategy for our cpu to make decisions
        - there are some baseline strategies implemented in the source code, but we can do better by implementing GTO strategies:
            - Equity: percentage that your draw hits the board
                - ex. if you have a flush draw on the flop, there are 9 cards that can complete your flush out of the 47 unknown cards (52 - 5 community cards) so your equity is 9/47 = 19.1%
            - Expected Value: Expected Value = (probability of winning) * (amount won) - (probability of losing) * (amount lost)
                - ex. if you have a flush draw and your opponet puts you all in and you call, if you hit your flushyou win $100. If you don't hit your flush, you lose $25. So, your expected value is (19.1%) * ($100) - (80.9%) * ($25) = $19.1 - $20.225 = -$1.125
                - This means that on average, you will lose $1.125 for every $25 you bet
            - Pot Odds: pot odds = (pot size + current bet) / current bet
                - ex. if the pot is $100 and your opponent bets $25, you need to call $25 to win a pot of $125, giving you pot odds of 5:1
            - Implied Odds:  This is a more advanced strategy that takes into account the possibility of future bets and the size of the pot.
                - ex. Say you have a flush draw (9 outs) on the flop. The pot is $100 and your opponent bets $25. You need to call $25 to win a pot of $125, giving you pot odds of 5:1.
                - However, if you hit your flush on the turn, your opponent will likely bet again. So, you need to make a decision based on the possibility of hitting your flush on the turn and the size of the pot on the turn.
            - GTO Strategies:
                - GTO strategies are optimal strategies for a given situation, taking into account the pot odds, implied odds, and equity.
                - ex. If you have a flush draw and your opponent puts you all in, you have about 20% equity meaning that the the odds of you winning the hand (assuming a flush will be the best hand) are 5:1 against you. In order for this to be a profitable call, the pot odds need to be better than 5:1 (pot size of $100, opponent bets $25, you need to call $25 to win a pot of $125, giving you pot odds of 5:1).
                - you can also think about this backwards, if the odds for you to win are 5:1 in your favor, then you only need to win 1 out of every 5 times to break even (this is because the reverse pot odds, amount lost if you call the bet, is 1:5).
            - However, in order to truly be a profitable poker player, you need to know when to deviate from theory and make optimal decisions based on the situation, which is where I imagine we will need to implement some sort of reinforcement learning model to help the cpu make decisions.

    - `receive_game_start_message`: takes in game_info and updates the game state
        - This function will signal that the game has started, should set the game structure based on the configurations by the user in the GUI, update state of the game, and should be called when the user clicks the start game button
    - `receive_round_start_message`: takes in round_count, hole_card, and seats
        - This function will signal that a new round has started, should update state of the game and the number of hands played (if applicable)
        - Signal a function or shuffle the deck and deal cards, get initial state of the players, update the state of the game, set the pot for the hand,and then call the `receive_street_start_message` function to start the first street
        - if there are still hands to play, this should be called to signal the start of the next hand, otherwise the game is over and the result of the game should be displayed
        - if we do not limit the number of hands that are played, I imagine we implement some sort of timer/quit button that allows the user to end the game at any time
    - `receive_street_start_message`: takes in street and round_state and updates the ga
        - This function will signal that a new street has started, should update state of the game, and should be called when the user clicks the next street button
        - Signal a function or verify the state of the game/players, get the action from the user (GUI) and the cpu (`declare_action`) and then update the state of the game by sending the action to the `receive_game_update_message` function 
    - `receive_game_update_message`: takes in new_action and round_state and updates the game state
        - This function will signal that a new action has been made, should update state of the game, and should be called when the user makes a bet/call/raise/fold
        - Signal a function or update everything as needed, if a player folds move on to the next hand, if all in handle as needed, etc.
    - `receive_round_result_message`: takes in winners, hand_info, and round_state and updates the game state
        - This function will signal that a hand has ended, should update state of the game, and should be called when the showdown occurs or people fold out, etc.
        - update the number of hands played if applicable, update the stacks, update the blinds, etc.
    
    **I imagine the logic for a lot of these functions will be necessary for both our actual player and the cpu, so what we could do is create a user player similar to the `console_player` class in the source code, and then just have the cpu inherit from the `BasePokerPlayer` class**

# Poker Showdown: GUI + Game Engine Project

> A full-featured Texas Hold’em Poker game featuring custom betting logic, AI opponent, and pixel-art GUI — built as part of a Software Engineering course at the University of Vermont.

---

##  Table of Contents
- [About the Project](#about-the-project)
- [Gameplay Features](#gameplay-features)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Screenshots](#screenshots)
- [Known Issues](#known-issues)
- [Team Members](#team-members)
- [License](#license)

---

##  About the Project

Poker Showdown is a 1v1 Texas Hold’em poker simulation game with:
- Dynamic chip-based betting
- A working poker engine with full game state transitions
- An AI opponent that reacts intelligently to player moves
- Pixel-style GUI with smooth transitions and spritesheet-based rendering
A user of Poker Showdown will be welcomed to a retro, pixel-styled GUI showing a poker board, $500 in chips, and a CPU with the same amount of money. The goal is to win the opponent's money by creating the strongest possible five-card hand or getting them to fold. Once all money is in the Player or CPU's collection, the game is over.

---

##  Gameplay Features

✅ Clickable betting buttons (`25%`, `50%`, `75%`, `All In`)
- Controls a slider to select bet amount
✅ Raise, Fold, Call, and Check logic and buttons, selectable when appropriate within the game
- Raise: place a bet based on the location of the slider
- Fold: discard one's hand and forfeit interest in the current pot
- Call: match the current bet
- Check: chooses not to bet and remains in the hand if no one has bet before
✅ Slider-based betting
- Slider changes the amount the user will bet
✅ Card reveal at showdown(all betting and card actions completed)  
✅ CPU betting logic
- AI-based betting logic
✅ Pot distribution with edge-case handling (all-in, partial calls)  
✅ Chip graphics update based on actual stack  
✅ Visual state transitions between menu, settings, and gameplay

---

##  Getting Started

###  Requirements
```bash
Python 3.10+
Pygame

Starting Board: <img width="398" alt="image" src="https://github.com/user-attachments/assets/a9d95b67-a283-4407-b56c-6637c3ab70c1" />

