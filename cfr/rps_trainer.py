import numpy as np
from timeit import default_timer as timer

class RPS_trainer:
    def __init__(self):
        # 0 Rock, 1 Paper, 2 Scissors
        self.action_len = 3
        self.actions = np.arange(3)
        self.player_action_pr_sum = np.zeros(3)
        self.opp_action_pr_sum = np.zeros(3)
        self.player_regret_sum = np.zeros(3)
        self.opp_regret_sum = np.zeros(3)
        self.rewards = np.array([[0,-1,1],[1,0,-1],[-1,1,0]])

    def get_strategy(self,regret_sum):
        regret_sum[regret_sum<0.001]=0
        normalizing_sum = sum(regret_sum)
        if normalizing_sum==0:
            return np.repeat(1/self.action_len,self.action_len)
        else:
            return regret_sum/normalizing_sum
        
    def get_reward(self,player_action,opp_action):
        return self.rewards[player_action,opp_action]

    def get_action(self,p):
        return np.random.choice(self.actions,p=p)
    
    def get_average_strategy(self,action_pr_sum):
        action_pr_sum = np.clip(action_pr_sum,0,None)
        normalizing_sum = sum(action_pr_sum)
        if normalizing_sum==0:
            return np.repeat(1/self.action_len,self.action_len)
        else:
            return action_pr_sum/normalizing_sum
        
    def train(self,n_iterations=50):
        for i in range(n_iterations):
            # Compute regret-matching strategy profile
            player_strategy = self.get_strategy(self.player_regret_sum)
            opp_strategy = self.get_strategy(self.opp_regret_sum)
            # Add strategy profile to strategy profile sum
            self.player_action_pr_sum+=player_strategy
            self.opp_action_pr_sum+=opp_strategy
            # Select each player action profile according to strategy profile
            player_action = self.get_action(player_strategy)
            opp_action = self.get_action(opp_strategy)
            #Compute Player regrets
            player_reward = self.get_reward(player_action,opp_action)
            opp_reward = self.get_reward(opp_action,player_action)

            player_regret = np.zeros(3)
            opp_regret = np.zeros(3)
            
            for i in range(self.action_len):
                player_regret[i] = player_reward  - self.get_reward(i,opp_action)
                opp_regret[i] = opp_reward - self.get_reward(i,player_action)
            #Add player regrets to cummulative regrets
            self.player_regret_sum+=player_regret
            self.opp_regret_sum+=opp_regret
        print(f'Player strategy {self.get_average_strategy(self.player_action_pr_sum)}')
        print(f'Opp strategy {self.get_average_strategy(self.opp_action_pr_sum)}')

rps = RPS_trainer()
start = timer()
rps.train(10000)
end = timer()
print(f'time: {end-start}')