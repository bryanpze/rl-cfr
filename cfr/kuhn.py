import numpy as np
from random import shuffle
import numpy as np
from timeit import default_timer as timer

"""
Info Sets
K
Q
J
Bet K
Bet Q
Bet J
Pass K
Pass Q
pass J
K Pass Bet
Q Pass Bet
J Pass Bet
"""

class KuhnPoker:
    def __init__(self):
        self.num_actions = 2
        # Pass Bet
        self.actions = np.arange(self.num_actions)
        self.node_map = {}
        self.cards = np.array([0,1,2])
    def train(self,iterations):
        util = 0
        for i in range(iterations):
            np.random.shuffle(self.cards)
            util+=self.cfr("",1,1,i)
        print(f'Average game value: {util/iterations}')
        for node in self.node_map:
            print(self.node_map[node])

    def cfr(self,history,p0,p1,iter):
        plays = len(history)
        player = plays%2
        opponent = 1- player
        # Checks to see if both players have at least one action
        if plays>1:
            if self.check_terminal(history):
                return self.get_payoff(history,player,opponent)
        infoset = str(self.cards[player])+history
        
        # Retrieve node associated with infoset or create if not exist
        if infoset in self.node_map:
            node = self.node_map[infoset]
        else:
            node = KuhnNode(infoset)
            self.node_map[infoset]=node

        # For each action recursively call cfr with additional history and updated probability of playing to that infoset in current training iteration
        strat_prob = p0 if player==0 else p1
        node_strategy = node.get_strategy(strat_prob,iter)
        util = np.zeros(self.num_actions)
        node_util = 0
        for i in range(self.num_actions):
            next_action = 'p' if i==0 else 'b'
            next_history = history+next_action
            util[i] = -self.cfr(next_history,p0*node_strategy[i],p1,iter) if player==0 else -self.cfr(next_history,p0,p1*node_strategy[i],iter)
            # Each action probability is multiplied by the corresponding returned action utility is accumulated to the utility of the player playing this node
            node_util+=util[i]*node_strategy[i]
        # For each action, compute and accumulate counterfactual regrets
        # Cumulative regrets are cumulative counterfactual regrets, weighted by prob that opponet plays to the current infoset
        for i in range(self.num_actions):
            regret = util[i]-node_util
            node.regret_sum[i]+=(regret*p1 if player==0 else regret*p0)
        return node_util

    def check_terminal(self,history):
        terminal_pass = history[-1:]=='p'
        double_bet = history[-2:]=='bb'
        if terminal_pass or double_bet:
            return True
        else:
            return False

    def get_payoff(self,history,player,opponent):
        terminal_pass = history[-1:]=='p'
        double_bet = history[-2:]=='bb'
        is_player_card_higher = self.cards[player]>self.cards[opponent]
        if terminal_pass:
            if history[-2:]=='pp':
                return 1 if is_player_card_higher else -1
            else:
                return 1
        elif double_bet:
            return 2 if is_player_card_higher else -2

class KuhnNode:
    def __init__(self,info_set):
        self.info_set = info_set
        self.num_actions = 2
        self.regret_sum = np.zeros(self.num_actions)
        self.strategy_sum = np.zeros(self.num_actions)
        self.strategy = np.repeat(1/self.num_actions,self.num_actions)
    
    def get_strategy(self,realization_weight,iteration):
        # Thresholding using 0.001 instead of 0 prevents unecessary traversals
        # Using the regret[regret<0] is faster than the np.clip method
        self.regret_sum[self.regret_sum<0.001] = 0
        normalizing_sum = sum(self.regret_sum)
        if normalizing_sum==0:
            self.strategy = np.repeat(1/self.num_actions,self.num_actions)
        else:
            self.strategy =  self.regret_sum/normalizing_sum
        # Resetting strategy sums
        # By not including strategies of early iterations, it helps improves convergence
        # Leads to faster convergence as well
        if iteration>10000:
            self.strategy_sum+=realization_weight*self.strategy
        return self.strategy
    def get_average_strategy(self):
        self.strategy_sum[self.strategy_sum<0.001] = 0
        normalizing_sum = sum(self.strategy_sum)
        if normalizing_sum==0:
            return np.repeat(1/self.num_actions,self.num_actions)
        else:
            return self.strategy_sum/normalizing_sum

    def __str__(self):
        return f'{self.info_set}: {str(self.get_average_strategy())}'

trainer = KuhnPoker()
start = timer()
trainer.train(1000000)
end = timer()
print(f'time: {end-start}')