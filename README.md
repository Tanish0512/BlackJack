## Optimal Strategy for a Card Game using Markov Decision Processes (MDPs)

This project finds the optimal strategy for a specific strategic card game by modeling it as a Markov Decision Process (MDP). It includes an MDP solver with two planning algorithms and an encoder/decoder system to interface with the game.

## Card Game Rules

The game's objective is to achieve the highest score possible without exceeding a fixed Threshold. Exceeding the threshold results in a Bust (score 0).
  
- Deck: 26 cards (1-13, each in Heart/Diamond).  
- Scoring: Final Score = Sum of Hand Values + Bonus (if a specified Special Sequence of 3 consecutive numbers is present).
- Actions (28 total):  
  0: Add (Draw a new card).  
  1-13: Swap a Heart card (e.g., 1 for ♥1).  
  14-26: Swap a Diamond card (e.g., 14 for ♦1).  
  27: Stop (End the game).
- Uncertainty: The next card drawn is always uniformly random from the remaining deck.

## Project Components

**1. MDP Planner (`planner.py`):**  Solves a general MDP to find the optimal value function (V*) and policy (π*).

**Algorithms Implemented:**
   - Howard's Policy Iteration (hpi)
   - Linear Programming (lp) (uses the PuLP library)

**Usage:**
```
# Compute optimal policy using HPI
python planner.py --mdp path/to/mdp-file.txt --algorithm hpi
```

```
# Evaluate a specific policy
python planner.py --mdp path/to/mdp-file.txt --policy path/to/policy-file.txt
```

**Output Format:**
```
V*(0) π*(0)
V*(1) π*(1)
...v
```

**2. MDP Encoder (encoder.py) :** Translates the card game's configuration (Threshold, Bonus, Sequence) into the MDP file format required by `planner.py`. The state is defined by the agent's current hand.

**Usage:**
```
# Encodes the game configuration into an MDP file
python encoder.py --game_config path/to/game_config.txt > game_mdp.txt
```
**3. Policy Decoder (decoder.py) :**
Determines the optimal action(s) for the card game based on the policy computed by the planner.

**Modes of Operation:**

- Evaluate Testcase: Finds the optimal action for a specific initial hand(s).
```
python decoder.py --value_policy path/to/Vpi.txt --testcase path/to/testcase.txt
```
- Automated Policy Generation: Generates the complete optimal action for every possible valid hand in the game. This runs the full pipeline (encoding, planning, and decoding).
```
python decoder.py --automate path/to/game_config.txt
```
**Output Format for `--automate` (Standard Output):**
```
1H -> 1
1D -> 14
1H 1D -> 0
...
HandState -> OptimalAction
```
## Setup and Running
**Prerequisites**
- Python 3.x
- See requirements.txt
- The PuLP library:
```
pip install pulp
```
**Full Strategy Generation Example**
To generate the optimal strategy for a game defined in `config.txt`:

- Make sure `planner.py`, `encoder.py`, and `decoder.py` are in the same directory.

- Run the decoder in automated mode, pointing to your game configuration:

```
python decoder.py --automate config.txt
```
The resulting output on the standard output is the comprehensive optimal policy for that specific card game instance.
