# Poker Showdown: GUI + Game Engine Project

> A full-featured Texas Hold’em Poker game featuring custom betting logic, AI opponent, and pixel-art GUI — built as part of a Software Engineering course at the University of Vermont.

---

##  Table of Contents
- [About the Project](#about-the-project)
- [Gameplay Features](#gameplay-features)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Game Images](#game-images)
- [Team Members](#team-members)

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

Starting Board: <img width="398" alt="image" src="https://github.com/user-attachments/assets/a9d95b67-a283-4407-b56c-6637c3ab70c1" />
---

##  Getting Started
Poker Showdown is a game that runs on Python: a high-level, object-oriented, general-purpose programming language. The following instructions will get a copy of the project up and running on your local machine.

###  Requirements needed to begin 
```bash
Python 3.10+
Pygame
pip
```
### Steps to run game on local machine
1. Clone the Repository on local machine
git clone https://github.com/sgmalik/software_engineering_final.git
2. Install Dependencies listed above (use pip)
pip install pygame
3. Run Poker Showdown
python main.py

Notes on Foulder Structure
* main.py is the entry point to the game
* All assets (images, spritesheets) must remain in the /assets folder to run game
* All game logic lives in the game_engine/ directory
* All GUI components live in the gui/ directory

## Project Structure 
The high-level project structure for Poker Showdown can be seen below. Critical components are highlighted. To properly run the game, the user must have this structure.
```
software_engineering_final/
├── assets/               # Spritesheet and image assets

├── src/                  # Source code: Holds Gui and Game logic code 

  ├── main.py             # Main python file to run program
  
  ├── game_engine/        # Core game logic (engine, betting, player, pot)
  
  ├── gui/                # GUI classes: buttons, sliders, numtext, etc.
  
  ├── model/              # .pkl file for CPU AI model
  
└── README.md             # You're here!
```
## Technologies Used 
* Python 3.10
* Pygame for graphics and event handling
* Object-oriented design
* State-based GUI architecture
* PyPokerEngine for inspiration of betting model 

## Game Images 
<img width="399" alt="image" src="https://github.com/user-attachments/assets/0e587389-6df2-4ba6-a715-43e59485436b" />
<img width="597" alt="image" src="https://github.com/user-attachments/assets/6bcdbc78-2587-45fb-8c11-8f45e2e03f02" />
<img width="398" alt="image" src="https://github.com/user-attachments/assets/a9d95b67-a283-4407-b56c-6637c3ab70c1" />

## Team Members 

| Name    | Role & Contributions |
|---------|----------------------|
| **Surya Malik**   | Developed the CPU logic and core betting engine. Played a key role in implementing the AI opponent and internal game mechanics. |
| **Conor McDevitt**  | Focused heavily on the game engine and connection with the GUI. Helped architect game flow, connect user actions to game logic, and ensure consistent game state transitions. |
| **James Bouchat**   | Created the visual assets and spritesheet used in the GUI. Designed the look and feel of the interface and built the foundational and advanced structure of the graphical user interface. |
| **Nathan Fritz**  | Contributed to GUI development and maintained overall project coordination through bug fixes and deliverable submissions. |

