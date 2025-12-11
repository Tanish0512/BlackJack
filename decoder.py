import argparse
from encoder import *
import os

def read_testcases(filepath):
    with open(filepath) as f:
        lines = [line.rstrip("\n") for line in f]

    idx = lines.index("Testcase:")
    hand_lines = [line for line in lines[idx+1:]]
    hands = [tuple(sort_hand(line.split())) if line.split() else tuple() for line in hand_lines]
    threshold, bonus, sequence = read_game_config(filepath)
    return threshold, bonus, sequence, hands

def read_value_policy(filepath):
    policy = {}
    with open(filepath) as f:
        for state, line in enumerate(f):
            # print(line)
            parts = line.strip().split()
            if len(parts) == 2:
                _, a = parts
                policy[state] = int(a)
    return policy

def state_mapping(deck, limit):
    all_valid_hands = valid_hands(deck, limit)
    return {tuple(hand): idx for idx, hand in enumerate(all_valid_hands)}


def run_normal_mode(value_policy_path, testcase_path):
    threshold, bonus, sequence, test_hands = read_testcases(testcase_path)
    
    # 1. Create the deck in the SAME order as the encoder script.
    # This uses: for i in range(1, 14) for s in ["H", "D"]
    deck = [f"{i}{s}" for i in range(1, 14) for s in ["H", "D"]]

    # Now, the state_map will be generated identically to the encoder's.
    state_map = state_mapping(deck, threshold)

    policy = read_value_policy(value_policy_path)

    for hand in test_hands:
        # print(hand)
        state_id = state_map.get(tuple(hand))
        
        # This check prevents crashing if any unexpected hand appears.
        if state_id is not None:
            print(policy[state_id])
        else:
            # If a hand isn't found, it's a terminal state. Default action is Stop.
            print(-1)


def run_automate_mode(config_path):
    threshold, _, _ = read_game_config(config_path)
    deck = [f"{i}{s}" for i in range(1, 14) for s in ["H", "D"]]

    value_policy_path = os.path.join(os.getcwd(), "tmp_planner_output.txt")
    policy = read_value_policy(value_policy_path)

    all_valid_hands = valid_hands(deck, threshold)
    state_map = {tuple(hand): idx for idx, hand in enumerate(all_valid_hands)}
    
    for hand in all_valid_hands:
        sid = state_map.get(tuple(hand))
        if sid is not None and sid in policy:
            action = policy[sid]
        else:
            action = 27  # Stop by default
        print((" ".join(hand) if hand else "") + " -> " + str(action))


def main():
    parser = argparse.ArgumentParser(description="Decoder for card game MDP")
    parser.add_argument("--value_policy", help="Planner output file with values and actions")
    parser.add_argument("--testcase", help="Testcase file path")
    parser.add_argument("--automate", help="Game configuration file for full policy output")

    args = parser.parse_args()

    # --- Mode selection ---
    if args.automate:
        run_automate_mode(args.automate)

    elif args.value_policy and args.testcase:
        run_normal_mode(args.value_policy, args.testcase)


if __name__ == "__main__":
    main()