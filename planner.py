import argparse
import numpy as np
from pulp import *

def read_mdp(file_path):
    mdp = {}
    mdp["transitions"] = {}

    with open(file_path, "r") as f:
        for line in f:
            # print(line)
            parts = line.strip().split()
            if not parts:
                continue

            if parts[0] == "numStates":
                mdp["num_states"] = int(parts[1])

            elif parts[0] == "numActions":
                mdp["num_actions"] = int(parts[1])

            elif parts[0] == "end":
                if len(parts) == 2 and parts[1] == "-1":
                    mdp["end_states"] = []  # continuing MDP
                elif len(parts) > 1:
                    mdp["end_states"] = list(map(int, parts[1:]))
                else:
                    mdp["end_states"] = []

            elif parts[0] == "transition":
                s1 = int(parts[1])
                a = int(parts[2])
                s2 = int(parts[3])
                r = float(parts[4])
                p = float(parts[5])

                if (s1, a) not in mdp["transitions"]:
                    mdp["transitions"][(s1, a)] = []
                mdp["transitions"][(s1, a)].append((s2, r, p))

            elif parts[0] == "mdptype":
                mdp["mdptype"] = parts[1]

            elif parts[0] == "discount":
                mdp["discount"] = float(parts[1])
    return mdp
   
def policy_evaluation(mdp, policy):
    n_states = mdp["num_states"]
    gamma = mdp["discount"]
    R = np.zeros(n_states)
    P = np.zeros((n_states, n_states))

    for s1, ac in enumerate(policy):
        if (s1, ac) not in mdp["transitions"]:
            continue
        for s2, r, p in mdp["transitions"][(s1, ac)]:
             R[s1] += p*r
             P[s1][s2] += p

    I = np.identity(n_states)
    V = np.linalg.solve(I - gamma * P, R)
    return V

import numpy as np

def howards_policy_iteration(mdp):

    n_states = mdp["num_states"]
    n_actions = mdp["num_actions"]
    gamma = mdp["discount"]

    policy = np.zeros(n_states)
    stable = False
    iter = 0
    while not stable:
        if iter >= 10 : break
        iter += 1
        V = policy_evaluation(mdp, policy)

        stable = True
        for s in range(n_states):
            if s in mdp["end_states"]: 
                continue

            old_action = policy[s]

            action_values = []
            for a in range(n_actions):
                q_val = 0
                if (s, a) in mdp["transitions"]:
                    for s2, r, p in mdp["transitions"][(s, a)]:
                        q_val += p * (r + gamma * V[s2])
                action_values.append(q_val)

            best_action = int(np.argmax(action_values))

            if best_action != old_action:
                stable = False
                policy[s] = best_action

    return V, policy



def linear_programming(mdp):
    """
    Linear Programming method.
    Returns (V*, π*).
    """
    n_states = mdp["num_states"]
    n_actions = mdp["num_actions"]
    gamma = mdp["discount"]

    prob = LpProblem("Bellman_Optimality_Problem", LpMinimize)
    V = LpVariable.dict("V", range(n_states))
    
    prob += lpSum([V[s] for s in range(n_states)])
    pi_star = []

    for s in range(n_states):
        if s in mdp["end_states"]:
            prob += V[s] == 0  
            continue

        for a in range(n_actions):
            if (s,a) not in mdp["transitions"]:
                continue
            rhs = lpSum(p * (r + gamma * V[s2]) for s2, r, p in mdp["transitions"][(s, a)])
            prob += V[s] >= rhs

    prob.solve(PULP_CBC_CMD(msg=False))
    V_star = np.array([V[s].varValue for s in range(n_states)])

    pi_star = np.zeros(n_states, dtype=int)

    for s in range(n_states):
        if s in mdp["end_states"]:
            continue  # terminal states
        best_a = None
        best_val = -float('inf')
        for a in range(n_actions):
            if (s,a) not in mdp["transitions"]:
                continue
            val = sum(p * (r + gamma * V_star[s2]) for s2, r, p in mdp["transitions"][(s,a)])
            if val > best_val:
                best_val = val
                best_a = a
        pi_star[s] = best_a

    return V_star, pi_star
            
            

def read_policy_file(file_path):
    with open(file_path, "r") as f:
        policy = [int(line.strip()) for line in f.readlines()]
    return np.array(policy)

def main():
    parser = argparse.ArgumentParser(description="MDP Planner")
    parser.add_argument("--mdp", type=str, required=True,
                        help="Path to MDP input file")
    parser.add_argument("--algorithm", type=str, choices=["hpi", "lp"], default="lp",
                        help="Algorithm to use: hpi or lp (default: hpi)")
    parser.add_argument("--policy", type=str,
                        help="Path to policy file to evaluate")

    args = parser.parse_args()
    mdp = read_mdp(args.mdp)
    # print(mdp)
    if args.policy:
        policy = read_policy_file(args.policy)
        V_pi = policy_evaluation(mdp, policy)
        for s, v in enumerate(V_pi):
            print(f"{v:.6f}\t{policy[s]}")
    else:
        if args.algorithm == "hpi":
            V_star, pi_star = howards_policy_iteration(mdp)
        else: 
            V_star, pi_star = linear_programming(mdp)

        for v, pi in zip(V_star, pi_star):
            print(f"{v:.6f}\t{int(pi)}")

if __name__ == "__main__":
    main()