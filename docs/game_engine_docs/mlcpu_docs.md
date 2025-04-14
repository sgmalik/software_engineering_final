# 🤖 MLCPU: Machine Learning-Based Poker Agent

This document provides a comprehensive overview of the Machine Learning CPU (MLCPU) implementation, which uses Q-learning to develop and improve its poker strategy through gameplay experience.

---

## 🧠 Overview

The MLCPU is an advanced poker agent that uses reinforcement learning to develop its strategy. Unlike rule-based CPUs that follow predefined rules, the MLCPU learns from experience and adapts its play style based on the outcomes of previous hands.

**Key Features:**
- Q-learning based decision making
- State-action value tracking
- Adaptive strategy development
- Persistent learning through model saving/loading
- Exploration vs exploitation balance

Think of the MLCPU as a player who starts with no poker knowledge but gradually learns which actions lead to winning more chips over time.

---

## 🎓 Core Concepts

### 1. Q-Learning Explained Simply

Q-learning is a reinforcement learning algorithm that learns to make decisions by learning the value (Q-value) of taking actions in different situations. It's like a player who keeps a mental notebook of what worked and what didn't.

**In Simple Terms:**
- The agent observes the current situation (state)
- It chooses an action (fold, call, or raise)
- It receives a reward (winning or losing chips)
- It updates its "mental notebook" (Q-table) based on the outcome

**Q-Learning Update Rule:**
```python
Q(s,a) = Q(s,a) + α * (r + γ * max(Q(s',a')) - Q(s,a))
```

Where:
- α (alpha) is the learning rate - how quickly the agent learns from new experiences
- r is the immediate reward - how many chips were won or lost
- γ (gamma) is the discount factor - how much the agent values future rewards vs. immediate rewards
- max(Q(s',a')) is the maximum Q-value for the next state - the best possible outcome from the next situation

**Real-World Analogy:**
Imagine you're learning to play chess. After each move, you note whether it led to a good or bad position. Over time, you build a mental map of which moves tend to lead to winning positions. Q-learning works similarly - it builds a map of which actions in which situations tend to lead to winning outcomes.

### 2. State Representation

The MLCPU represents game states using a tuple of numerical features:
```python
(outs_bucket, pot_odds_bucket, position, street, stack_to_pot_bucket, aggression_bucket)
```

This compact representation allows the agent to:
- Track hand strength through the number of outs (potential winning cards)
- Consider pot odds for decision making (risk vs. reward)
- Account for position (small blind or big blind)
- Track which street we're on (preflop, flop, turn, river)
- Consider stack size relative to pot
- Track opponent aggression

**Why Discretization?**
Instead of using continuous values (like exact pot odds of 0.37), the MLCPU uses "buckets" (like pot odds between 0.3 and 0.4). This reduces the number of unique states the agent needs to learn, making learning more efficient.

### 3. Action Space

The agent considers three possible actions:
- Fold (giving up the hand)
- Call (matching the current bet)
- Raise (increasing the bet)
- Check (if the action is not a bet)

Each action is associated with a Q-value that represents its expected value in the current state. The agent chooses the action with the highest expected value (unless it's exploring).

---

## 🔧 Implementation Details

### 1. State Feature Extraction

The `extract_features` method converts the current game state into a numerical representation that the agent can use for decision making:

```python
def extract_features(self, hole_cards, community_cards, pot, call_amount, round_state):
    # Count outs as a measure of hand strength
    outs = self.count_outs(hole_cards, community_cards)
    
    # Calculate pot odds
    if isinstance(call_amount, dict) and 'min' in call_amount:
        call_amount = call_amount['min']  # Use minimum call amount for pot odds calculation
    pot_odds = call_amount / (pot + call_amount) if pot + call_amount > 0 else 0
    
    # Calculate position (0 = small blind, 1 = big blind)
    position = 0
    if round_state.get('small_blind_pos') == 1:  # We're small blind
        position = 0
    elif round_state.get('big_blind_pos') == 1:  # We're big blind
        position = 1
        
    # Calculate street (0 = preflop, 1 = flop, 2 = turn, 3 = river)
    street_map = {'preflop': 0, 'flop': 1, 'turn': 2, 'river': 3}
    street = street_map.get(round_state.get('street', 'preflop'), 0)
    
    # Calculate stack to pot ratio
    stack_to_pot = self.stack / (pot + 1)  # Add 1 to avoid division by zero
    
    # Calculate opponent aggression (ratio of raises to calls)
    opponent_aggression = 0
    if self.opponent_actions:
        raises = sum(1 for action in self.opponent_actions if action.get('action') == 'raise')
        calls = sum(1 for action in self.opponent_actions if action.get('action') == 'call')
        opponent_aggression = raises / (calls + 1)  # Add 1 to avoid division by zero
        
    # Discretize continuous values to reduce state space
    outs_bucket = min(outs // 2, 10)  # 0-20 outs, bucketed into 11 categories
    pot_odds_bucket = int(pot_odds * 10)  # 0-1 pot odds, bucketed into 10 categories
    stack_to_pot_bucket = min(int(stack_to_pot), 10)  # 0-10+ stack to pot ratio
    aggression_bucket = min(int(opponent_aggression * 2), 5)  # 0-2.5+ aggression, bucketed into 6 categories
    
    # Return a tuple of discretized features
    return (outs_bucket, pot_odds_bucket, position, street, stack_to_pot_bucket, aggression_bucket)
```

**Understanding the Features:**

1. **Outs**: The number of cards that could improve your hand. For example, if you have four cards to a flush, you have 9 outs (the remaining 9 cards of that suit).

2. **Pot Odds**: The ratio of the call amount to the total pot after calling. For example, if you need to call 10 chips to win a pot of 40 chips, your pot odds are 10/(40+10) = 0.2 or 20%.

3. **Position**: Whether you're in the small blind (0) or big blind (1) position. Position is crucial in poker as it determines who acts first.

4. **Street**: Which stage of the hand you're in - preflop (0), flop (1), turn (2), or river (3).

5. **Stack to Pot Ratio**: How many times your stack size is compared to the current pot. This helps determine how committed you are to the hand.

6. **Opponent Aggression**: How aggressive your opponent has been, measured as the ratio of raises to calls.

### 2. Action Selection

The `get_action_from_q_table` method implements an epsilon-greedy strategy, which balances exploration (trying new actions) and exploitation (using known good actions):

```python
def get_action_from_q_table(self, state, valid_actions):
    # Epsilon-greedy strategy
    if random.random() < self.epsilon:
        # Explore: choose a random action
        action_idx = random.randint(0, len(valid_actions) - 1)
        action = valid_actions[action_idx]['action']
        amount = valid_actions[action_idx].get('amount', 0)
        if isinstance(amount, dict):  # For raise actions
            amount = amount.get('min', 0)
        return action, amount
    
    # Exploit: choose the action with the highest Q-value
    best_action_idx = 0
    best_q_value = float('-inf')
    
    for i, action_dict in enumerate(valid_actions):
        action = action_dict['action']
        amount = action_dict.get('amount', 0)
        if isinstance(amount, dict):  # For raise actions
            amount = amount.get('min', 0)
            
        q_value = self.q_table[state][(action, amount)]
        if q_value > best_q_value:
            best_q_value = q_value
            best_action_idx = i
            
    action = valid_actions[best_action_idx]['action']
    amount = valid_actions[best_action_idx].get('amount', 0)
    if isinstance(amount, dict):  # For raise actions
        amount = amount.get('min', 0)
        
    return action, amount
```

**Understanding Epsilon-Greedy Strategy:**

- With probability ε (epsilon): The agent explores by choosing a random action. This helps it discover new strategies and avoid getting stuck in local optima.
- With probability 1-ε: The agent exploits by choosing the action with the highest Q-value. This is the action that has historically led to the best outcomes.

For example, if ε = 0.1, the agent will:
- Choose a random action 10% of the time
- Choose the best-known action 90% of the time

As training progresses, ε can be gradually decreased to favor exploitation over exploration.

### 3. Q-Value Updates

The `update_q_value` method implements the Q-learning update rule:

```python
def update_q_value(self, state, action, reward, next_state):
    # Get the maximum Q-value for the next state
    next_max_q = max(self.q_table[next_state].values()) if self.q_table[next_state] else 0
    
    # Q-learning update rule
    current_q = self.q_table[state][action]
    new_q = current_q + self.learning_rate * (reward + self.discount_factor * next_max_q - current_q)
    self.q_table[state][action] = new_q
```

**Understanding the Q-Learning Update:**

1. The agent takes an action in a state and receives a reward.
2. It then looks at the next state and finds the best possible action in that state.
3. It updates its estimate of the value of the action it just took based on:
   - The immediate reward it received
   - The discounted value of the best action in the next state
   - Its previous estimate of the action's value

This update helps the agent learn which actions lead to higher rewards over time.

### 4. Reward Calculation

The `calculate_reward` method determines the reward based on the round outcome:

```python
def calculate_reward(self, round_result, hand_info):
    # Check if we won
    won = False
    for winner in round_result:
        if isinstance(winner, dict) and winner.get('name') == self.name:
            won = True
            break
            
    # Calculate reward based on stack change
    initial_stack = self.stack - self.contribuition
    stack_change = self.stack - initial_stack
    
    # Base reward is the stack change
    reward = stack_change
    
    # Add bonus for winning
    if won:
        reward += 10
        
    # Add penalty for folding with a strong hand
    if self.state == PlayerState.FOLDED and self.count_outs(self.hole_cards, self.community_cards) > 10:
        reward -= 5
        
    return reward
```

**Understanding the Reward Structure:**

1. **Base Reward**: The primary reward is the change in stack size. Winning chips is good, losing chips is bad.

2. **Winning Bonus**: A bonus of 10 is added if the agent won the hand. This encourages the agent to play to win rather than just minimize losses.

3. **Folding Penalty**: A penalty of 5 is applied if the agent folded with a strong hand (more than 10 outs). This discourages the agent from folding when it has a good chance of winning.

4. **Intermediate Rewards**: Small negative rewards (-0.1) are given for intermediate actions to encourage efficiency.

This reward structure guides the agent toward making profitable decisions while avoiding common poker mistakes like folding strong hands.

---

## 🧠 Learning Process

### 1. Training Flow

The MLCPU learns through a cycle of observation, action, reward, and update:

1. **State Observation**
   - The agent observes the current game state
   - It extracts features from the state (outs, pot odds, position, etc.)
   - It stores the current state for later Q-value updates

2. **Action Selection**
   - The agent selects an action using the epsilon-greedy strategy
   - It considers only valid actions (e.g., can't check if there's a bet to call)
   - It records the selected action for later Q-value updates

3. **Experience Collection**
   - The agent records its action and the resulting state
   - It tracks opponent actions to build a model of opponent behavior
   - It maintains a history of the current round for later reward calculation

4. **Learning Updates**
   - After each action, the agent updates Q-values based on immediate rewards
   - At the end of the round, it calculates the final reward
   - It updates Q-values for all actions in the round based on the final reward
   - It saves the model periodically (every 10 rounds) to preserve learning

**Visual Representation of the Learning Cycle:**

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Observe State  │────▶│  Select Action  │────▶│  Receive Reward │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Save Model     │◀────│  Update Q-Values│◀────│  Next State     │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### 3. Model Training

The `train_model` method provides a way to train the MLCPU through simulated poker rounds:

```python
def train_model(self, num_rounds=1000, opponent_strategy='random'):
    """
    Train the MLCPU by simulating multiple rounds of poker.
    
    Args:
        num_rounds (int): Number of rounds to simulate (default: 1000)
        opponent_strategy (str): Strategy for the opponent CPU
            - 'random': Makes random decisions
            - 'aggressive': Tends to raise and bet
            - 'passive': Tends to call and check
    """
```

**Training Process:**

1. **Setup**
   - Creates a simulated opponent using the specified strategy
   - Increases exploration (epsilon) to 0.3 during training
   - Saves the original state to restore after training

2. **Round Simulation**
   - Deals hole cards to both players
   - Simulates each street (preflop, flop, turn, river)
   - Handles betting rounds and action selection
   - Determines winners and updates stacks

3. **Learning Updates**
   - Updates Q-values based on round outcomes
   - Saves the model every 10 rounds
   - Prints progress updates
   - Tracks completed rounds

**Example Usage:**

```python
# Train the MLCPU against a random opponent
ml_cpu.train_model(num_rounds=1000, opponent_strategy='random')

# Train against an aggressive opponent
ml_cpu.train_model(num_rounds=2000, opponent_strategy='aggressive')

# Train against a passive opponent
ml_cpu.train_model(num_rounds=1500, opponent_strategy='passive')
```

**Training Progress:**
The method provides feedback on training progress:
- Shows the number of completed rounds
- Indicates when the model is saved
- Reports the final number of rounds completed

**Best Practices:**
1. Start with a higher number of rounds (1000+) for better learning
2. Train against different opponent strategies to develop a balanced approach
3. Save the model periodically to preserve progress
4. Monitor the training progress to ensure learning is occurring

### 2. Model Persistence

The MLCPU can save and load its learned Q-table, allowing it to continue learning across multiple game sessions:

```python
def save_model(self, path):
    with open(path, 'wb') as f:
        pickle.dump(dict(self.q_table), f)
        
def load_model(self, path):
    with open(path, 'rb') as f:
        q_table_dict = pickle.load(f)
        self.q_table = defaultdict(lambda: defaultdict(float), q_table_dict)
```

**Why Model Persistence Matters:**

- Learning in poker is slow - it takes many hands to develop a good strategy
- Saving the model allows the agent to build on previous learning
- Different models can be trained for different opponents or game types

---

## 🎯 Performance Considerations

### 1. Memory Usage

The Q-table can grow large as the agent encounters more unique states:

- Each state is represented by a 6-tuple of features
- Each state-action pair has an associated Q-value
- The number of possible states is the product of the number of possible values for each feature

**Example Calculation:**
- 11 possible outs buckets × 10 possible pot odds buckets × 2 possible positions × 4 possible streets × 11 possible stack-to-pot buckets × 6 possible aggression buckets = 58,080 possible states

To manage memory usage:
- States are discretized into buckets
- The Q-table is saved periodically to disk
- Unused state-action pairs can be pruned

### 2. Learning Parameters

The MLCPU's learning is controlled by three key parameters:

1. **Learning Rate (α)**: 0.1 (default)
   - Controls how quickly the agent learns from new experiences
   - Higher values (e.g., 0.3): Faster learning but more volatile
   - Lower values (e.g., 0.01): More stable but slower learning
   - **Real-world analogy**: How quickly you update your opinion after new evidence

2. **Discount Factor (γ)**: 0.9 (default)
   - Determines how much the agent values future rewards vs. immediate rewards
   - Higher values (e.g., 0.95): More emphasis on long-term outcomes
   - Lower values (e.g., 0.5): More emphasis on immediate outcomes
   - **Real-world analogy**: How much you value immediate gratification vs. long-term benefits

3. **Exploration Rate (ε)**: 0.1 (default)
   - Controls the balance between exploration and exploitation
   - Higher values (e.g., 0.3): More random actions, more exploration
   - Lower values (e.g., 0.01): More best-known actions, more exploitation
   - **Real-world analogy**: How often you try new restaurants vs. going to your favorite

**Parameter Tuning:**
These parameters can be tuned based on:
- The specific poker variant being played
- The desired playing style (aggressive vs. conservative)
- The computational resources available

### 3. Convergence

The MLCPU's learning follows a typical reinforcement learning curve:

1. **Initial Phase (0-1000 hands)**
   - Mostly random actions due to high exploration
   - Rapid improvement as basic patterns are learned
   - Often makes obvious mistakes

2. **Middle Phase (1000-5000 hands)**
   - More consistent play as Q-values stabilize
   - Learns basic poker concepts (position, pot odds)
   - Still vulnerable to advanced strategies

3. **Advanced Phase (5000+ hands)**
   - Sophisticated play with balanced strategies
   - Adapts to opponent tendencies
   - Makes fewer mistakes and exploits opponent weaknesses

**Visual Representation of Learning Progress:**

```
     Performance
         │
         │     Advanced Phase
         │          │
         │          │
         │     Middle Phase
         │          │
         │          │
         │     Initial Phase
         │          │
         │          │
         └──────────┴─────────────────▶
                Hands Played
```

---

## 🔮 Future Enhancements

1. **Deep Q-Learning**
   - Replace the Q-table with a neural network
   - Handle continuous state spaces without discretization
   - Learn more complex patterns and strategies
   - **Example**: A neural network that takes raw card information and outputs Q-values for each action

2. **State Representation**
   - Add position information (early, middle, late)
   - Include opponent modeling (tracking opponent tendencies)
   - Track betting patterns and bet sizing
   - **Example**: Adding features like "opponent_raise_frequency" and "opponent_continuation_bet_percentage"

3. **Reward Structure**
   - Implement multi-objective rewards (e.g., balance chip EV and tournament survival)
   - Consider long-term strategy (e.g., building a table image)

4. **Training Improvements**
   - Implement experience replay (storing and replaying past experiences)
   - Add prioritized experience replay (focusing on the most informative experiences)
   - Use double Q-learning (reducing overestimation of action values)
   - **Example**: Storing the last 10,000 state-action-reward-next_state tuples and randomly sampling from them for updates

---

## 📝 Usage Example

Here's how to create and use an MLCPU in your poker game:

```python
# Create MLCPU instance
ml_cpu = MLCPU(
    initial_stack=1000,
    model_path="models/ml_cpu_model.pkl",
    learning_rate=0.1,
    discount_factor=0.9,
    epsilon=0.1
)

# Load existing model if available
if os.path.exists("models/ml_cpu_model.pkl"):
    ml_cpu.load_model("models/ml_cpu_model.pkl")

# Use in game engine
engine = Engine(num_players=2, initial_stack=1000, blind=10)
engine.set_cpu_difficulty("hard")  # Uses MLCPU
```

**Training the MLCPU:**

To train the MLCPU effectively:

1. Play many hands (1000+) against various opponents
2. Start with a higher epsilon (0.3-0.5) for more exploration
3. Gradually decrease epsilon as the CPU improves
4. Save the model periodically to preserve learning
5. Consider using different models for different game types or opponents

---

## 🔍 Testing

The MLCPU is tested using pytest with fixtures that simulate various game states:

```python
def test_ml_cpu_model_creation():
    # Test model saving and loading
    with tempfile.TemporaryDirectory() as temp_dir:
        model_path = os.path.join(temp_dir, "test_model.pkl")
        
        # Create and train CPU
        cpu = MLCPU(name="test_cpu", stack=1000, model_path=model_path)
        
        # Simulate gameplay
        # ...
        
        # Verify model was saved and loaded correctly
        assert os.path.exists(model_path)
        assert os.path.getsize(model_path) > 0
```

**Key Test Cases:**

1. **Model Creation and Persistence**
   - Verify that the model can be saved and loaded
   - Check that Q-values are preserved between sessions

2. **Decision Making**
   - Test that the CPU makes valid actions
   - Verify that the epsilon-greedy strategy works as expected

3. **Learning**
   - Confirm that Q-values are updated correctly
   - Check that the CPU improves its strategy over time

4. **Feature Extraction**
   - Validate that features are extracted correctly
   - Ensure that discretization works as expected

---

## 📚 References

1. Sutton, R. S., & Barto, A. G. (2018). Reinforcement Learning: An Introduction. MIT Press.
   - The foundational textbook on reinforcement learning, including Q-learning.

2. Mnih, V., et al. (2015). Human-level control through deep reinforcement learning. Nature, 518(7540), 529-533.
   - The paper that introduced Deep Q-Networks (DQN) for playing Atari games.

3. Brown, N., & Sandholm, T. (2019). Superhuman AI for multiplayer poker. Science, 365(6456), 885-890.
   - Details on how AI has achieved superhuman performance in poker.

4. Johanson, M., et al. (2013). Measuring the size of large no-limit poker games. arXiv preprint arXiv:1302.7005.
   - Analysis of the size of the poker game state space.

5. Zinkevich, M., et al. (2008). Monte Carlo sampling for regret minimization in extensive games. Advances in Neural Information Processing Systems, 21.
   - Introduction to counterfactual regret minimization, another approach to poker AI.
