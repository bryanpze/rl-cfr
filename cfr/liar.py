import numpy as np
import random
from timeit import default_timer as timer

class LiarDieTrainer:
    def __init__(self,sides):
        self.DOUBT = 0
        self.ACCEPT = 1
        self.sides = sides
        # 2D array of response nodes indexed by claim before current claim and current claim
        # 0 is used when initial claim does not exist
        # E.g response node for initial claim of c would be response_nodes[0][c]
        self.response_nodes = np.ndarray((self.sides,self.sides+1),dtype=object)
        # 2D array of claim nodes indexed by accepted prior claim before the current claim and current die roll claim decision concerns
        # E.g claim node for initial claim of a game with roll r would be claim_nodes[0][r]
        self.claim_nodes = np.ndarray((self.sides,self.sides+1),dtype=object)
        # only one action when no prior claim (ACCEPT) and only one action when opponent claims highest rank (DOUBT)
        for i in range(self.sides+1):
            for j in range(i+1,self.sides+1):
                self.response_nodes[i,j] = LiarDieNode(1) if ((j==0) or (j==self.sides)) else LiarDieNode(2)
        # number of legal claims remaining are number of sides minus previous opponent claim
        for i in range(self.sides):
            for j in range(1,self.sides+1):
                self.claim_nodes[i,j] = LiarDieNode(self.sides-i)

    def train(self,num_iterations):
        regret = np.zeros(self.sides)
        roll_after_accepting_claim = np.zeros(self.sides,dtype=int)
        for iter in range(num_iterations):
            # Precompute initial rolls and set initial reach probabilities
            for i in range(len(roll_after_accepting_claim)):
                roll_after_accepting_claim[i] = random.randint(1,self.sides)
            
            self.claim_nodes[0, roll_after_accepting_claim[0]].pPlayer = 1
            self.claim_nodes[0, roll_after_accepting_claim[0]].pOpponent = 1

            # Accumulate realization weights forward
            for opp_claim in range(self.sides+1):
                # Visit response nodes forward
                if opp_claim>0:
                    for my_claim in range(0,opp_claim):
                        node = self.response_nodes[my_claim][opp_claim]
                        action_prob = node.get_strategy()
                        if opp_claim<self.sides:
                            next_node = self.claim_nodes[opp_claim,roll_after_accepting_claim[opp_claim]]
                            next_node.pPlayer +=action_prob[1]*node.pPlayer
                            next_node.pOpponent +=node.pOpponent
                # Visit claim nodes forward
                if opp_claim<self.sides:
                    node = self.claim_nodes[opp_claim,roll_after_accepting_claim[opp_claim]]
                    action_prob = node.get_strategy()
                    for my_claim in range(opp_claim+1,self.sides+1):
                        next_claim_prob = action_prob[my_claim-opp_claim-1] 
                        if next_claim_prob>0:
                            next_node = self.response_nodes[opp_claim,my_claim]
                            next_node.pPlayer += node.pOpponent
                            next_node.pOpponent += node.pPlayer*next_claim_prob
            # Backpropogate utilities, adjusting regrets and strategies
            for opp_claim in range(self.sides,-1,-1):
                # Visit claim nodes backwards
                if opp_claim<self.sides:
                    node = self.claim_nodes[opp_claim,roll_after_accepting_claim[opp_claim]]
                    action_prob = node.strategy
                    node.u = 0
                    for my_claim in range(opp_claim+1,self.sides+1):
                        action_index = my_claim - opp_claim -1
                        next_node = self.response_nodes[opp_claim][my_claim]
                        child_util = -next_node.u
                        regret[action_index] = child_util
                        node.u += action_prob[action_index] * child_util
                    for a in range(len(action_prob)):
                        regret[a] -= node.u
                        node.regret_sum[a]+=node.pOpponent *regret[a]
                    node.pPlayer = 0
                    node.pOpponent = 0
                # Visit response nodes backwards
                if opp_claim>0:
                    for my_claim in range(0,opp_claim):
                        node = self.response_nodes[my_claim,opp_claim]
                        action_prob = node.strategy
                        node.u = 0
                        doubt_util = 1 if opp_claim>roll_after_accepting_claim[my_claim] else -1
                        regret[self.DOUBT] = doubt_util
                        node.u += action_prob[self.DOUBT]*doubt_util
                        if opp_claim<self.sides:
                            next_node = self.claim_nodes[opp_claim,roll_after_accepting_claim[opp_claim]]
                            regret[self.ACCEPT] = next_node.u
                            node.u+=action_prob[self.ACCEPT]*next_node.u
                        for i in range(len(action_prob)):
                            regret[i]-=node.u
                            node.regret_sum[i] += node.pOpponent *regret[i]
                        node.pPlayer = 0
                        node.pOpponent = 0

            # Reset strategy sums after half of training
            if iter==int(num_iterations/2):
                for (x,y), value in np.ndenumerate(self.response_nodes):
                    if self.response_nodes[x,y] != None:
                        self.response_nodes[x,y].strategy_sum = 0
                for (x,y), value in np.ndenumerate(self.claim_nodes):
                    if self.claim_nodes[x,y] != None:
                        self.claim_nodes[x,y].strategy_sum = 0            
        # Print resulting strategy
        for initialRoll in range(1,self.sides+1):
            print(f'Initial claim policy with roll {initialRoll}')
            for prob in self.claim_nodes[0,initialRoll].get_average_strategy():
                print(prob)
        print(f'\n Old Claim \t New Claim \t Action Probabilities')
        for my_claim in range(0,self.sides):
            for opp_claim in range(my_claim+1,self.sides+1):
                print(f'{my_claim} {opp_claim} {str(self.response_nodes[my_claim,opp_claim].get_average_strategy())}')
        print(f'\n Old Claim \t Roll \t Action Probabilities')
        for opp_claim in range(0,self.sides):
            for roll in range(1,self.sides+1):
                print(f'{opp_claim} {roll} {str(self.claim_nodes[opp_claim,roll].get_average_strategy())}')
class LiarDieNode:
    def __init__(self,num_actions):
        self.num_actions = num_actions
        self.regret_sum = np.zeros(num_actions)
        self.strategy_sum = np.zeros(num_actions)
        self.strategy = np.zeros(num_actions)
        # Holds utility value in order to allow for backpropogation of utility to all predecessors
        self.u = 0
        # Sum of probabilities, represent average probabilities if we divide by the number of node_visits
        self.pPlayer = 0
        self.pOpponent = 0
    
    def get_strategy(self):
        self.regret_sum[self.regret_sum<0] = 0 
        normalizing_sum = sum(self.regret_sum)
        if normalizing_sum==0:
            self.strategy = np.repeat(1/self.num_actions,self.num_actions)
        else:
            self.strategy = self.regret_sum/normalizing_sum
        self.strategy_sum += self.strategy *self.pPlayer
        return self.strategy
    def get_average_strategy(self):
        self.strategy_sum[self.strategy_sum<0] = 0
        normalizing_sum = sum(self.strategy_sum)
        if normalizing_sum == 0:
            return np.repeat(1/self.num_actions,self.num_actions)
        else:
            return self.strategy_sum/normalizing_sum

trainer = LiarDieTrainer(6)
start = timer()
trainer.train(1000)
end = timer()
print(f'time: {end-start}')