import numpy as np
from itertools import product
import matplotlib.pyplot as plt


class Off_Policy_MC:
    def __init__(self,ndecks=1,nrounds=100):
        self.nrounds = nrounds
        self.cards = [i if i<10 else 10 for i in range (1,14)] * 4 * ndecks
        #hit,stand,double,split
        self.actions = [0,1,2,3]
        #Player sum, dealer hole card, ace is still soft,current_num_cards_player (max 4 aces 4 twos 3 threes), actions
        self.state_action_values = np.random.random((21,10,2,11,4))
        self.cum_weights = np.zeros((21,10,2,11,4))
        self.policy = self.state_action_values.argmax(axis=4)
        self.states = []
        self.actions = []
        self.probs = []
        self.rewards = []

    def gen_episode(self, epsilon = 0.1):
        self.states = []
        self.actions = []
        self.probs = []
        self.cards_left =self.cards.copy()
        round = np.random.choice(self.cards_left,size = 3,replace=False)
        for i in round:
            self.cards_left.remove(i)
        dealer = [round[0]]
        player = [round[1],round[2]]
        player_sum = sum(player)
        dealer_hole = dealer[0]
        ace_is_still_soft = 0
        num_cards = 2
        if 1 in player:
            ace_is_still_soft = 1
        states.append([player_sum,dealer_hole,ace_is_still_soft,num_cards])
        t = 0
        while True:
            s = self.states[t]
            valid_actions = [0,1]
            if s[3]==2:
                valid_actions.append(2)
                if player[0]==player[1]:
                    valid_actions.append(3)
            greedy = self.policy[tuple(s)]
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
            next_state = [player_sum,dealer_hole,ace_is_still_soft,num_cards]

            #Check if stand
            if action==1:
                return t
            elif action==4:
                #draw one more card update state return t
            next_state = [,dealer_hole,,,]

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