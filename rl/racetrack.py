import numpy as np
from itertools import product
import matplotlib.pyplot as plt

#Create environment
track = np.zeros((32,17))
track[0,0:3] = 1
track[1:3, 0:2] = 1
track[3, 0] = 1
track[14:,0] = 1
track[22:,1] = 1
track[29:,2] = 1
track[29:,2] = 1
track[6:,10:] = 1
track[7:,9:] = 1

#Initialization
action_comb = list(product([0,1,-1],[0,1,-1]))
#states rows, columns, velocity row (0-4)  velocity column (0-4) , actions 
state_action_values = np.random.random((32,17,5,5,9))*400-500
cum_weights = np.zeros((32,17,5,5,9))
policy = state_action_values.argmax(axis=4)
#valid actions for each velocity combination: velocity ranges from 0-4, resulting velocity can never be (0,0)
velocity_combinations = [list(product([i],list(range(0,5)))) for i in range(0,5)]
def check_valid(comb):
    valid = []
    for i,j in enumerate(action_comb):
        if comb[0]+j[0]!=0 or comb[1]+j[1]!=0:
            if comb[0]+j[0]>=0 and comb[0]+j[0]<=4 and comb[1]+j[1]>=0 and comb[1]+j[1]<=4:
                valid.append(i)
    return valid
velocity_combinations = [list(map(check_valid,j)) for j in velocity_combinations]

states=[]
actions =[]
probs =[]

#Generate episodes
def gen_episode(epsilon = 0.1):
    #initial state
    global states 
    states = []
    global actions 
    actions = []
    global probs
    probs = []
    states.append([31,np.random.randint(3,9),0,0])
    t = 0
    while True:
        s = states[t]
        valid_actions = velocity_combinations[s[2]][s[3]]
        greedy = policy[tuple(s)]
        greedy_is_valid = greedy in valid_actions
        if np.random.random()>=epsilon:
            if greedy_is_valid:
                action = greedy
                prob_action = 1-epsilon+epsilon/len(valid_actions)
            else:
                action = np.random.choice(valid_actions)
                prob_action = 1/len(valid_actions)
        else:
            if greedy_is_valid:
                tmp = [x for x in valid_actions if x!=greedy]
                action = np.random.choice(tmp)
                prob_action = epsilon/len(valid_actions)
            else:
                action = np.random.choice(valid_actions)
                prob_action = 1/len(valid_actions)
        actions.append(action)
        probs.append(prob_action)
        next_state = [s[0] - (s[3]+action_comb[action][1]),s[1] + (s[2]+action_comb[action][0]),s[2]+action_comb[action][0],s[3]+action_comb[action][1]]
        # Check if hit finish line
        if (next_state[0]>=0 and next_state[0]<=5) and (next_state[1]>=16):
            return t
        if next_state[0] >31 or next_state[0]<0 or next_state[1]<0 or next_state[1]>16 or track[next_state[0],next_state[1]]==1:
            next_state[0] = 31
            next_state[1] = np.random.randint(3,9)
            next_state[2] = 0
            next_state[3] = 0
        
        t+=1
        states.append(next_state)
        
#Simulate 1000 episodes

def loop_episode(t):
    G = 0
    W = 1
    R = -1
    for step in range(t,0,-1):
        step_state = states[step]
        step_action = actions[step]
        step_prob = probs[step]
        G = G + R
        cum_weights[tuple(step_state)+tuple([step_action])] = cum_weights[tuple(step_state)+tuple([step_action])]+W
        state_action_values[tuple(step_state)+tuple([step_action])] = state_action_values[tuple(step_state)+tuple([step_action])] + ((W/(cum_weights[tuple(step_state)+tuple([step_action])]))*(G-state_action_values[tuple(step_state)+tuple([step_action])]))
        valid_actions = velocity_combinations[step_state[2]][step_state[3]]
        greedy_policy = valid_actions[state_action_values[tuple(step_state)][valid_actions].argmax()]
        policy[tuple(step_state)] = greedy_policy
        if greedy_policy != step_action:
            return
        W = W/step_prob



def simulate():
    for i in range(10000):
        t = gen_episode()
        loop_episode(t)
        print(-1*t)
    t = gen_episode(0)
    print(-1*t)
simulate()