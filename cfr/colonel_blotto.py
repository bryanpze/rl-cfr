import numpy as np
import itertools
from collections import defaultdict
class Cblotto:
    def __init__(self):
        self.pure_actions = self.gen_pure(S=5,N=3)
        self.num_actions = len(self.pure_actions)
        self.payoffs = self.gen_payoffs()
        self.player_regret_sum = np.zeros(self.num_actions)
        self.opp_regret_sum = np.zeros(self.num_actions)
        self.player_strategy_sum =  np.zeros(self.num_actions)
        self.opp_strategy_sum =  np.zeros(self.num_actions)

    def gen_pure(self,S,N):
        key = 0
        pure_actions = set()
        pure_actions_dict = {}
        for i in itertools.combinations(list(range(S+1))*N,N):
            for j in itertools.permutations(list(i)):
                if sum(j)==S:
                    pure_actions.add(j)
        for index,value in enumerate(pure_actions):
            pure_actions_dict[index] = value
        return pure_actions_dict
    def gen_payoffs(self):
        payoffs = np.zeros([self.num_actions,self.num_actions])
        for i in range(self.num_actions):
            player_action = self.pure_actions[i]
            for j in range(self.num_actions):
                enemy_action = self.pure_actions[j]
                controlled = 0
                loss = 0
                for position in range(len(enemy_action)):
                    if (player_action[position] - enemy_action[position])>0:
                        controlled += 1
                    elif (player_action[position] - enemy_action[position])<0:
                        loss +=1
                if controlled>loss:
                    payoffs[i,j]=1
                elif loss>controlled:
                    payoffs[i,j] = -1
        return payoffs
    
    def get_strategy(self,regret_sum):
        regret_sum = np.clip(regret_sum,0,None)
        normalizing_sum = sum(regret_sum)
        if normalizing_sum==0:
            return np.repeat(1/self.num_actions,self.num_actions)
        else:
            return regret_sum/normalizing_sum

    def get_action(self,strategy):
        return np.random.choice(list(range(self.num_actions)),p=strategy)
    
    def get_reward(self,player_action,opp_action):
        return self.payoffs[player_action,opp_action]
    
    def get_average_strategy(self,action_pr_sum):
        action_pr_sum = np.clip(action_pr_sum,0,None)
        normalizing_sum = sum(action_pr_sum)
        if normalizing_sum==0:
            np.repeat(1/self.action_len,self.action_len)
        else:
            return action_pr_sum/normalizing_sum

    
    def train(self,num_iterations=1000):
        for i in range(num_iterations):
            player_strategy = self.get_strategy(self.player_regret_sum)
            opp_strategy = self.get_strategy(self.opp_regret_sum)
            
            self.player_strategy_sum+=player_strategy
            self.opp_strategy_sum+=opp_strategy
            
            player_action = self.get_action(player_strategy)
            opp_action = self.get_action(opp_strategy)

            player_reward = self.get_reward(player_action,opp_action)
            opp_reward = self.get_reward(opp_action,player_action)

            player_regret = np.zeros(self.num_actions)
            opp_regret = np.zeros(self.num_actions)
            
            for i in range(self.num_actions):
                player_regret[i] = player_reward  - self.get_reward(i,opp_action)
                opp_regret[i] = opp_reward - self.get_reward(i,player_action)
            #Add player regrets to cummulative regrets
            self.player_regret_sum+=player_regret
            self.opp_regret_sum+=opp_regret
        print(f'Player strategy {self.get_average_strategy(self.player_strategy_sum)}')
        print(f'Opp strategy {self.get_average_strategy(self.opp_strategy_sum)}')
        print(f'Pure_actions {self.pure_actions}')




model = Cblotto()
model.train(num_iterations=2000000)