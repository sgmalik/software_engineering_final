---
marp: true
title: "Heads Up Poker"
paginate: true
theme: gaia
---

# Heads Up Poker

## Software Engineering Final Project

---

```
src/
├── main.py
├── models/
│   └── ml_cpu_model.pkl
├── game_engine/
│   ├── engine.py
│   ├── cpu/
│   │   ├── mlCPU.py
│   │   ├── potOddsCPU.py
│   │   ├── expectedValueCPU.py
│   │   ├── equityCPU.py
│   │   └── baselineCPU.py
│   ├── hand_evaluator.py
│   ├── dealer.py
│   ├── betting_manager.py
│   ├── player.py
│   ├── game_evaluator.py
│   ├── table.py
│   ├── card.py
│   ├── pot.py
│   ├── deck.py
│   └── constants.py
└── gui/
    ├── button.py
    ├── util.py
    ├── spritetext.py
    ├── gui_card.py
    ├── slider.py
    ├── numtext.py
    └── chip.py
```

---

# Core Game Engine

- **Core Game Engine**
  - Python-based poker implementation
  - Supports Texas Hold'em rules
  - Multiple CPU difficulty levels
  - Hand evaluation and game state management

---

# GUI Implementation

- **GUI Implementation**
  - Pygame-based interface
  - Visual card and chip representations
  - Interactive betting controls
  - Real-time game state updates

---

# Code Overview

- **Game Engine Components**
  - `Engine`: Core game logic and state management
  - `Dealer`: Handles card dealing and round progression
  - `BettingManager`: Handles betting logic
  - `Player`: Base player class with action handling
  - `GameEvaluator`: Handles game evaluation and winner determination
  - `HandEvaluator`: Handles hand evaluation
  - `CPU`: Multiple AI implementations (Baseline, Equity, Pot Odds, ML)
  - `Deck`: Handles card deck management
  - `Pot`: Handles pot management
  - `Table`: Handles table management
  - `Card`: Handles card management

---

# GUI Implementation

- **GUI Components**
  - `Button`: Interactive UI elements
  - `GUI_Card`: Visual card representation
  - `Chip`: Visual chip stack representation
  - `Slider`: Betting amount control
  - `NumText`: Number display
  - `SpriteText`: Text rendering
  - `Util`: Utility functions

---

# Live Demo

- **Game Flow**
  1. Start new game
  2. Place blinds
  3. Deal cards
  4. Betting rounds
  5. Showdown
  6. Winner determination

- **Features to Show**
  - Different CPU difficulties
  - Betting mechanics
  - Hand evaluation
  - Visual feedback

---

# Work Division

- **GUI**
  - Game engine core implementation
  - CPU AI development
  - Testing framework

- **Engine**
  - Game engine core implementation
  - CPU AI development
  - Testing framework

---

# Shared Responsibilities

- **Shared Responsibilities**
  - Code review
  - Documentation
  - Bug fixing
  - Testing

---

# Git Usage

- **Branch Strategy**
  - `main`: Production-ready code
  - Feature branches for new implementations

- **Commit Practices**
  - Small, frequent commits
  - Update documentation/tests with new features
  - Regular pushes
  - Pull request reviews

---

# Collaboration

- **Collaboration**
  - Code review process
  - Feature discussions

---

# What Worked Well

- **Technical Successes**
  - Clean architecture separation
  - Modular CPU implementations
  - Efficient hand evaluation
  - Responsive GUI

- **Process Successes**
  - Regular communication
  - Clear task division
  - Comprehensive testing

---

# Challenges Faced

- **Technical Challenges**
  - ML CPU training stability
  - GUI performance optimization
  - State management complexity
  - Edge case handling

- **Process Challenges**
  - Documentation maintenance
  - Feature prioritization

---

# Lessons Learned

- **Technical Improvements**
  - Better error handling
  - More comprehensive testing
  - Performance optimization

- **Process Improvements**
  - More frequent reviews
  - Better task estimation
  - Enhanced communication

---

# Future Enhancements

- **Technical Features**
  - Multiplayer support
  - Tournament mode
  - Advanced AI strategies

- **Process Improvements**
  - Automated testing
  - Performance monitoring
  - User feedback system

---

# Questions?

Thank you for your attention!
