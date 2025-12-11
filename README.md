Strategic Card Play using MDPs

A two-part journey through decision-making, optimal control, and a sprinkle of card-driven drama.

This repository contains my complete implementation for an IIT Bombay course assignment on Markov Decision Processes. It consists of:

A general-purpose MDP planner supporting policy iteration and LP methods.

A full MDP modeling pipeline for a strategic card game (Blackjack-with-a-twist), including encoder, decoder, and automated policy generation.

The project blends mathematical precision with algorithmic craft, transforming uncertainty into optimal action.

📌 Project Overview
Task 1: MDP Planning

The goal is to compute:

The optimal value function 
𝑉
\*
V
\*

An optimal policy 
𝜋
\*
π
\*

Given an input MDP, the file planner.py implements:

✔ Howard’s Policy Iteration (HPI)

Custom implementation:

Exact policy evaluation using linear equation solving

Improvement based on switching all improvable states

✔ Linear Programming (LP)

Using the PuLP library to solve the Bellman optimality constraints.

✔ Policy Evaluation Mode

If a policy file is given, the planner evaluates its value function.

✔ Clean Output

Prints S lines containing:
value_of_state optimal_action
(min. 6 decimal precision)

This component is fully compatible with the provided autograder.py.

Task 2: Card Game as an MDP

A strategic card game with:

26 cards: numbers 1–13 in ♥ and ♦

Actions: Add, Swap (for specific cards), Stop

Bust threshold

Bonus for containing a 3-card consecutive sequence

Each draw is from a reshuffled remaining deck, so transitions are stochastic and uniform.

Key Components
encoder.py — Game → MDP

Given a game configuration (limit, bonus, sequence), this script generates a corresponding MDP in the same format used by planner.py.
It defines states, actions, transitions, and rewards so that solving the MDP yields the optimal game strategy.

decoder.py — Planner Output → Game Actions

Given:

The computed value-policy file

The encoded MDP

Testcases representing different initial hands

The decoder returns the optimal action for each instance.

--automate Mode

Generates an action for every possible valid hand (sum < threshold).

Outputs lines like:

1H -> 1
1D -> 14
1H 1D -> 0
2H -> 2
...


Used directly by the GUI for automated gameplay.

🗂 File Structure
planner.py      # MDP solver (HPI & LP)
encoder.py      # Card game → MDP converter
decoder.py      # Policy-to-action for hands; also supports --automate
generateMDP.py  # Provided random MDP generator
autograder.py   # Test runner
gui.py          # Provided visual gameplay interface
game_setup.py   # Full pipeline runner for GUI automation
data/
  mdp/          # 8 base MDP tasks + reference solutions
  gamespec/     # Card game configuration examples
  test/         # Testcases with initial hands

🚀 How to Run
1. Solve an MDP
python3 planner.py --mdp path/to/mdp.txt --algorithm hpi
python3 planner.py --mdp path/to/mdp.txt --algorithm lp
python3 planner.py --mdp path/to/mdp.txt
python3 planner.py --mdp path/to/mdp.txt --policy policy.txt

2. Encode a Card Game
python3 encoder.py --game_config data/gamespec/game1.txt > mdp.txt

3. Decode Actions
python3 decoder.py --value_policy vp.txt --testcase data/test/test1.txt

4. Generate Full Hand→Action Policy
python3 decoder.py --automate game_config.txt

5. Launch GUI in Automated Mode
python3 game_setup.py --limit 20 --bonus 10 --sequence 3 4 5 --initial_state 3H 4D 7H

🧠 Design Highlights
Policy Iteration

Full synchronous improvement

Deterministic tie-breaking where needed

Handles terminal states cleanly

Linear Programming

Uses standard Bellman inequalities

Extracts optimal actions from LP values

Card Game MDP

State represents:

Hand composition

Remaining deck

Actions correspond to all legal Add/Swap/Stop moves

Rewards given only on termination

The formulation ensures the optimal policy truly maximizes expected final score.
