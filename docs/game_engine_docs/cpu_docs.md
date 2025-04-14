# 🧠 CPU Player Strategies Documentation

This document outlines the different CPU opponents implemented for the poker engine, explaining their internal logic, strategic basis, and the framework they operate within using the PyPokerEngine architecture.

---

## 🧹 Architecture: `BasePokerPlayer` Interface

Each CPU player inherits from `BasePokerPlayer` and must implement the following key methods:

- `declare_action(valid_actions, hole_card, round_state)`
- `receive_game_start_message(game_info)`
- `receive_round_start_message(round_count, hole_card, seats)`
- `receive_street_start_message(street, round_state)`
- `receive_game_update_message(new_action, round_state)`
- `receive_round_result_message(winners, hand_info, round_state)`

These methods provide the hooks necessary for the CPU to interact with the game engine and make decisions during each phase of the game.

---

## 🧠 Implemented CPU Types

### 1. `baselineCPU`

**Goal**: Skeleton implementation with placeholder methods.

- Does **not** currently contain any decision-making logic.
- Serves as a starting point or scaffolding for new strategies.
- Can be extended or copied to begin building smarter opponents.

---

### 2. `equityCPU`

**Strategy**: Uses a simplified equity estimation based on "outs" to determine how strong its hand is.

**Core Concepts:**

- Outs: Number of cards that improve the hand significantly.
- Equity Estimate: `equity = outs * 4`, capped at 100%.

**Decision Thresholds:**

- If `equity` > 50% → Raise
- If 25% < `equity` ≤ 50% → Call
- If `equity` ≤ 25% → Fold

**Highlights:**

- Implements flush draw, straight draw, and overcard detection heuristics.
- Assumes maximum 9 outs for flush and up to 8 for straight draws.
- Great starting point for basic probabilistic play.

---

### 3. `expectedValueCPU`

**Strategy**: Makes decisions based on Expected Value (EV).

**Core Formula:**

```python
EV = (equity * pot_size) - ((1 - equity) * amount_to_call)
```

**Decision Logic:**

- If `EV` > 0 → Raise or Call
- Else → Fold

**Highlights:**

- Equity is computed the same way as in `equityCPU`.
- This CPU integrates pot size and call amount to assess profitability.
- Demonstrates a step toward `GTO (Game Theory Optimal)` behavior.

---

### 4. `potOddsCPU`

**Strategy**: Makes decisions based on Pot Odds vs Equity.

**Core Formula:**

```python
pot_odds = amount_to_call / (pot_size + amount_to_call)
```

**Decision Logic:**

- If `equity` ≥ `pot_odds` → Call or Raise
- Else → Fold

**Highlights:**

- Combines calculated pot odds with estimated equity.
- Models real-world betting decisions based on expected returns.

---

### mlCPU

The `mlCPU` class implements a reinforcement learning-based poker player using Q-learning. This CPU player learns from experience and adapts its strategy over time, making it potentially the most sophisticated CPU player in the system.

#### Architecture

The `mlCPU` class inherits from `BasePokerPlayer` and implements the following key components:

1. **Q-Learning Parameters**:
   - `learning_rate`: Controls how quickly the CPU learns from new experiences (default: 0.1)
   - `discount_factor`: Determines the importance of future rewards (default: 0.9)
   - `epsilon`: Controls the exploration-exploitation trade-off (default: 0.1)
   - `q_table`: Stores Q-values for state-action pairs using a nested defaultdict structure

2. **State Management**:
   - Tracks game state, round state, and player state
   - Maintains history of actions and game outcomes
   - Manages hole cards, community cards, and opponent actions

3. **Feature Extraction**:
   The CPU extracts the following features from the game state:
   - Number of outs (potential winning cards)
   - Pot odds
   - Position (small blind or big blind)
   - Current street (preflop, flop, turn, river)
   - Stack to pot ratio
   - Opponent aggression level

4. **Action Selection**:
   Uses an epsilon-greedy strategy:
   - With probability ε: explores by choosing a random action
   - With probability 1-ε: exploits by choosing the action with highest Q-value

#### Learning Mechanism

1. **Q-Value Updates**:
   - Updates Q-values using the Q-learning update rule:
     Q(s,a) = Q(s,a) + α[r + γ max Q(s',a') - Q(s,a)]
   - α is the learning rate
   - γ is the discount factor
   - r is the immediate reward
   - max Q(s',a') is the maximum Q-value for the next state

2. **Reward Calculation**:
   Rewards are based on:
   - Stack changes (primary reward)
   - Winning bonus (+10)
   - Penalty for folding with strong hands (-5)
   - Small negative rewards for intermediate actions (-0.1)

3. **Model Persistence**:
   - Saves the Q-table to disk every 10 rounds
   - Can load a previously saved model to continue learning
   - Uses pickle for serialization

#### State Space Discretization

To manage the large state space, the CPU discretizes continuous features:
- Outs: Bucketed into 11 categories (0-20 outs)
- Pot odds: Bucketed into 10 categories (0-1)
- Stack to pot ratio: Bucketed into 11 categories (0-10+)
- Opponent aggression: Bucketed into 6 categories (0-2.5+)

#### Message Handling

The CPU responds to various game events through message handlers:
1. `receive_game_start_message`: Initializes game settings
2. `receive_round_start_message`: Prepares for a new round
3. `receive_street_start_message`: Updates street-specific information
4. `receive_game_update_message`: Tracks opponent actions and updates Q-values
5. `receive_round_result_message`: Processes round outcomes and updates learning

#### Usage Example

```python
# Create an MLCPU instance
ml_cpu = mlCPU(
    initial_stack=1000,
    model_path="models/ml_cpu_model.pkl",
    learning_rate=0.1,
    discount_factor=0.9,
    epsilon=0.1
)

# The CPU will learn and improve its strategy over time
# The model is automatically saved every 10 rounds
```

#### Advantages and Limitations

Advantages:
- Adapts to opponent strategies
- Learns from experience
- Can develop sophisticated playing patterns
- Persists learning across sessions

Limitations:
- Requires significant training to become effective
- May make suboptimal decisions during early learning
- Memory usage grows with the number of unique states encountered
- Performance depends on the quality of feature extraction

#### Best Practices

1. **Training**:
   - Allow sufficient rounds for learning (100+ rounds recommended)
   - Start with higher epsilon (0.3-0.5) for more exploration
   - Gradually decrease epsilon as the CPU improves

2. **Model Management**:
   - Regularly backup model files
   - Consider using different models for different game types
   - Monitor model size and performance

3. **Feature Engineering**:
   - Consider adding more sophisticated features
   - Fine-tune discretization buckets
   - Add position-based features

4. **Performance Optimization**:
   - Monitor memory usage
   - Consider periodic Q-table pruning
   - Optimize feature extraction for speed

---

## 🎓 Design Philosophy

- These CPUs are intentionally designed to showcase progressively deeper poker logic.
- Use the `emulator` module from PyPokerEngine to simulate thousands of hands for training smarter strategies.
- Future enhancements may include:
  - Bluff detection
  - Opponent modeling
  - Reinforcement Learning (RL) or Deep Q-Learning agents

---

## 🔧 Useful Heuristics Implemented

| Concept        | Description                                                             |
| -------------- | ----------------------------------------------------------------------- |
| Equity         | % chance to win/improve hand using outs                                 |
| Expected Value | Weighs possible gain vs loss based on probabilities and bet size        |
| Pot Odds       | Determines whether a call is justified based on bet vs pot ratio        |
| Implied Odds   | Takes future rounds into account; can be used for deeper strategic play |

---

## 📌 Recommendations for Further Development

- Convert current `count_outs()` logic into a shared utility module.
- Use the PyPokerEngine emulator to simulate full games and collect training data.
- Use a decision tree, rule engine, or ML model for more nuanced behavior.

---

## 🔄 Method Implementation Details

### Common Methods Across All CPUs

All CPU implementations share these core methods:

#### `declare_action(valid_actions, hole_card, round_state)`
- **Purpose**: Determines the next action to take based on the current game state
- **Parameters**:
  - `valid_actions`: List of dictionaries containing possible actions (fold, call, raise)
  - `hole_card`: List of strings representing the player's hole cards
  - `round_state`: Dictionary containing the current state of the game
- **Returns**: Tuple of (action, amount) where action is a string and amount is an integer

#### `receive_game_start_message(game_info)`
- **Purpose**: Initializes the CPU when a new game begins
- **Parameters**:
  - `game_info`: Dictionary containing game settings and player information
- **Implementation**: Stores initial game settings and sets the player's name to "cpu"

#### `receive_round_start_message(round_count, hole_card, seats)`
- **Purpose**: Handles the start of a new round
- **Parameters**:
  - `round_count`: Integer indicating the current round number
  - `hole_card`: List of strings representing the player's hole cards
  - `seats`: List of dictionaries containing information about all players
- **Implementation**: Updates the player's state with new hole cards and seat information

#### `receive_street_start_message(street, round_state)`
- **Purpose**: Handles the start of a new street (preflop, flop, turn, river)
- **Parameters**:
  - `street`: String indicating the current street
  - `round_state`: Dictionary containing the current state of the game
- **Implementation**: Updates the player's state with new community cards and street information

#### `receive_game_update_message(new_action, round_state)`
- **Purpose**: Processes an action taken by another player
- **Parameters**:
  - `new_action`: Dictionary containing information about the action taken
  - `round_state`: Dictionary containing the updated state of the game
- **Implementation**: Tracks opponent actions and updates the player's state

#### `receive_round_result_message(winners, hand_info, round_state)`
- **Purpose**: Processes the results of a completed round
- **Parameters**:
  - `winners`: List of dictionaries containing information about the winners
  - `hand_info`: Dictionary containing information about the hands played
  - `round_state`: Dictionary containing the final state of the round
- **Implementation**: Updates the player's state to WINNER if they won and updates their stack

### CPU-Specific Methods

#### `count_outs(hole_cards, community_cards)` (equityCPU, potOddsCPU, expectedValueCPU)
- **Purpose**: Calculates the number of "outs" (cards that improve the hand)
- **Parameters**:
  - `hole_cards`: List of Card objects representing the player's hole cards
  - `community_cards`: List of Card objects representing the community cards
- **Returns**: Integer representing the number of outs
- **Implementation**: Checks for flush draws, straight draws, and overcards

#### `calculate_ev(equity, pot, call_amount)` (expectedValueCPU)
- **Purpose**: Calculates the expected value of a call
- **Parameters**:
  - `equity`: Float representing the player's equity
  - `pot`: Integer representing the current pot size
  - `call_amount`: Integer representing the amount needed to call
- **Returns**: Float representing the expected value
- **Implementation**: Uses the formula `EV = (equity * pot) - ((1 - equity) * call_amount)`

---

## 🔍 Testing

The CPU implementations are tested using pytest with fixtures that simulate various game states:

- `dummy_round_state`: Simulates the current state of a round
- `dummy_valid_actions`: Simulates the valid actions a player can take
- `dummy_hole_cards`: Simulates the player's hole cards
- `dummy_game_info`: Simulates game initialization data
- `dummy_round_start`: Simulates round start data
- `dummy_street_start`: Simulates street start data
- `dummy_game_update`: Simulates game update data
- `dummy_round_result`: Simulates round result data

Each CPU class has tests for all its methods to ensure they behave as expected.
