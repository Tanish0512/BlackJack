import argparse

def read_game_config(file_path):

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    threshold = int(lines[1])
    bonus = int(lines[2])
    sequence = list(map(int, lines[3].split()))

    return threshold, bonus, sequence

def valid_hands(cards, threshold):
    all_valid_states = []
    def backtrack(start, current_sum, subset):
        if current_sum >= threshold:
            return
        
        all_valid_states.append(sort_hand(subset[:]))

        for i in range(start, len(cards)):
            if current_sum + int(cards[i][:-1]) >= threshold:
                break

            subset.append(cards[i])
            backtrack(i+1, current_sum + int(cards[i][:-1]), subset)
            subset.pop()
    
    backtrack(0, 0, [])
    return all_valid_states

def sum_card_values(hand):
    return sum(int(card[:-1]) for card in hand)


def has_bonus(hand, sequence):
    numbers_in_hand = set([int(card[:-1]) for card in hand])
    return all(num in numbers_in_hand for num in sequence)


def valid_actions(valid_hands):
    possible_actions = []
    for hand in valid_hands:
        actions = [0, 27]
        for hand_card in hand:
            if hand_card[-1] == "H":
                actions.append(int(hand_card[:-1]))
            else:
                actions.append(int(hand_card[:-1]) + 13)
        possible_actions.append(sorted(actions))
    return possible_actions


def sort_hand(hand):
    # Sorts first by number, then by suit ('H' comes before 'D')
    suit_order = "HD"
    return sorted(hand, key=lambda c: (int(c[:-1]), suit_order.index(c[-1])))


def build_mdp_from_game(threshold, bonus, special_seq):

    cards = [f"{i}{s}" for s in ["H", "D"] for i in range(1, 14)]
    all_valid_hands = valid_hands(sorted(cards, key=lambda c: int(c[:-1])), threshold)
    all_valid_actions = valid_actions(all_valid_hands)
    state_id_map = {tuple(s):idx for idx,s in enumerate(all_valid_hands)}

    print("numStates",len(all_valid_hands)+1)      
    print("numActions", 28)     
    print("end", len(all_valid_hands))      

    for hand in all_valid_hands:
        state = state_id_map[tuple(hand)]
        remaining_deck = [card for card in cards if card not in hand]
        
        valid_action = all_valid_actions[state]
        # print(hand, state)

        for action in valid_action:
            if action == 0: # Add
                ter_prob = 1
                for card in remaining_deck:
                    new_hand = sort_hand(hand + [card])
                    new_state = state_id_map.get(tuple(new_hand))
                    if new_state is not None:
                        prob = 1/len(remaining_deck)
                        ter_prob -= prob
                        reward = 0
                        print("transition", state, action, new_state, reward, prob)
                
                if ter_prob > 0:
                    print("transition", state, action, len(all_valid_hands), 0, ter_prob)
                    

            elif action == 27: # Stop
                reward = sum_card_values(hand)
                if has_bonus(hand, special_seq):
                    reward += bonus
                print("transition", state, action, len(all_valid_hands), reward, 1.0)


            else: # Swap
                ter_prob = 1
                for card in remaining_deck:
                    new_hand = hand.copy()
                    if action <= 13 and action >=1:
                        new_hand.remove(cards[action-1])
                    elif action <= 26 and action >=14:
                        new_hand.remove(cards[action-1])
                    new_hand.append(card)
                    new_hand = sort_hand(new_hand)
                    new_state = state_id_map.get(tuple(new_hand))
                    if new_state is not None:
                        prob = 1/len(remaining_deck)
                        ter_prob -= prob
                        reward = 0
                        print("transition", state, action, new_state, reward, prob)
                
                if ter_prob > 0:
                    print("transition", state, action, len(all_valid_hands), 0, ter_prob)


    print("mdptype episodic")
    print("discount 1.0")



def main():
    parser = argparse.ArgumentParser(description="Encode card game into MDP format.")
    parser.add_argument("--game_config", required=True, help="Path to game specification file.")
    args = parser.parse_args()

    threshold, bonus, sequence = read_game_config(args.game_config)
    build_mdp_from_game(threshold, bonus, sequence)



if __name__ == "__main__":
    main()
