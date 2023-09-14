#%%
import numpy as np
import random
import math
import functools
import struct

"""
Info Sets

Stages:
player places ante

first two cards and three community cards delt, dealer bets twice the size of the ante
player action is to call or fold 


"""
class Evaluator:
    def __init__(self):
        self.card_vals = ['2', '3', '4', '5', '6', '7', '8', '9', 't', 'j', 'q', 'k', 'a'],
        self.cards = {
        "2c": 1,
        "2d": 2,
        "2h": 3,
        "2s": 4,
        "3c": 5,
        "3d": 6,
        "3h": 7,
        "3s": 8,
        "4c": 9,
        "4d": 10,
        "4h": 11,
        "4s": 12,
        "5c": 13,
        "5d": 14,
        "5h": 15,
        "5s": 16,
        "6c": 17,
        "6d": 18,
        "6h": 19,
        "6s": 20,
        "7c": 21,
        "7d": 22,
        "7h": 23,
        "7s": 24,
        "8c": 25,
        "8d": 26,
        "8h": 27,
        "8s": 28,
        "9c": 29,
        "9d": 30,
        "9h": 31,
        "9s": 32,
        "tc": 33,
        "td": 34,
        "th": 35,
        "ts": 36,
        "jc": 37,
        "jd": 38,
        "jh": 39,
        "js": 40,
        "qc": 41,
        "qd": 42,
        "qh": 43,
        "qs": 44,
        "kc": 45,
        "kd": 46,
        "kh": 47,
        "ks": 48,
        "ac": 49,
        "ad": 50,
        "ah": 51,
        "as": 52
        }
        self.handtypes = [
        "invalid hand",
        "high card",
        "one pair",
        "two pairs",
        "three of a kind",
        "straight",
        "flush",
        "full house",
        "four of a kind",
        "straight flush"
        ]
        with open('./HandRanks.dat','rb') as file:
            self.ranks_data = file.read()
    def fill_hand(self,cards):
        cards_used =  [0,0,0,0,0,0,0,0,0,0,0,0,0]
        for card in cards:
            i = math.floor((self.cards[card.lower()]-1)/4)
            cards_used[i] = 1
        to_fill = 2
        for i in range(13):
            if to_fill==0:
                break
            if cards_used[i]==0 and not self.make_straight(cards_used,i):
                cards_used[i]==2
                to_fill-=1
        suit = ['s','d']
        for i in range(14):
            if cards_used[i]==2:
                card = self.card_vals[i]+suit[0]
                suit.pop(0)
                cards.append(card)
        return cards
    
    @staticmethod
    def reducing_function(prev,next):
        if prev==5:
            return 5
        else:
            return prev+1 if next else 0
    def make_straight(self,cards_used,rank):
        new_cards = [cards_used[12]]+cards_used
        new_cards[rank+1]=2
        tmp = functools.reduce(self.reducing_function,new_cards)
        return 5==tmp
    def eval_hand(self,cards):
        if len(cards)==3:
            cards =  self.fill_hand(cards)
        if type(cards[0])==str:
            cards = list(map(lambda card: self.cards[card.lower()],cards))
        return self.evaluate(cards)
    
    def evaluate(self,cards):
        p=53
        for i in range(len(cards)):
            p=self.eval_card(p+cards[i])
        if len(cards)==5 or len(cards)==6:
            p = self.eval_card(p)
        return {
            'handType': p >> 12,
            'handRank': p & 0x00000fff,
            'value': p,
            'handName': self.handtypes[p >> 12]
        }
    def eval_card(self,card):
        offset = card * 4
        return struct.unpack('<I', self.ranks_data[offset:offset+4])[0] 

class CasinoHold:
    def __init__(self,bet_size):
        self.deck = ['2c',
        '2d',
        '2h',
        '2s',
        '3c',
        '3d',
        '3h',
        '3s',
        '4c',
        '4d',
        '4h',
        '4s',
        '5c',
        '5d',
        '5h',
        '5s',
        '6c',
        '6d',
        '6h',
        '6s',
        '7c',
        '7d',
        '7h',
        '7s',
        '8c',
        '8d',
        '8h',
        '8s',
        '9c',
        '9d',
        '9h',
        '9s',
        'tc',
        'td',
        'th',
        'ts',
        'jc',
        'jd',
        'jh',
        'js',
        'qc',
        'qd',
        'qh',
        'qs',
        'kc',
        'kd',
        'kh',
        'ks',
        'ac',
        'ad',
        'ah',
        'as']
        self.num_actions = 2
        self.actions = np.arange(self.num_actions)
        self.node_map = {}
        self.util = 0
        self.iter = 0
        self.bet_size = bet_size
        self.evaluator = Evaluator()

    def train(self,n_iterations = 50):
        for j in range(10):
            for i in range(n_iterations):
                # First two cards are player cards (part of infoset)
                # Next three is community cards (part of infoset)
                # Next two cards are opponent cards
                # Last two are final cards used only in reward
                cards = random.sample(self.deck,9)
                infoset = str(sorted(cards[:2])+sorted(cards[2:5]))
                if infoset in self.node_map:
                    node = self.node_map[infoset]
                else:
                    node = CasinoHoldNode(infoset)
                    self.node_map[infoset]=node
                player_strategy = node.get_strategy()
                player_action = self.get_action(player_strategy)
                counterfactual_action = 1-player_action
                player_reward = self.get_reward(player_action,cards)
                counterfactual_reward = self.get_reward(counterfactual_action,cards)
                
                player_regret = np.zeros(self.num_actions)
                player_regret[counterfactual_action] = counterfactual_reward - player_reward
                if self.iter<1000000:
                    player_regret*=self.iter
                node.regret_sum+=player_regret
                self.util+=player_reward
                self.iter+=1
                if i%500000==0:
                    print(f'Iteration {self.iter} Average game value: {self.util/(self.iter)}')
            self.util = 0
            self.iter = 0
            # for x in self.node_map:
            #     average = self.node_map[x].get_average_strategy()
            #     print(f'{x} {average}')

    def get_action(self,player_strategy):
        return self.actions[0] if player_strategy[0]>random.random() else self.actions[1]
        
    def get_reward(self,player_action,cards):
        if player_action==0:
            return -self.bet_size
        player_hand = self.evaluator.eval_hand(cards[:5]+cards[-2:])
        opp_han = self.evaluator.eval_hand(cards[2:])
        if opp_han['value']<8780:
            # Call bet is a push, Ante bet pays according to pay table
            if player_hand['value']==36874:
                return self.bet_size*100
            elif player_hand['handName']=='straight flush':
                return self.bet_size*20
            elif player_hand['handName']=='four of a kind':
                return self.bet_size*10
            elif player_hand['handName']=='full house':
                return self.bet_size*3
            elif player_hand['handName']=='flush':
                return self.bet_size*2
            else:
                return self.bet_size
        else:
            if opp_han['value']>player_hand['value']:
                return -(3*self.bet_size)
            elif opp_han['value']==player_hand['value']:
                return 0
            else:
                call_bet = self.bet_size*2
                if player_hand['value']==36874:
                    ante_bet = self.bet_size*100
                    return ante_bet+call_bet
                elif player_hand['handName']=='straight flush':
                    ante_bet = self.bet_size*20
                    return ante_bet+call_bet
                elif player_hand['handName']=='four of a kind':
                    ante_bet = self.bet_size*10
                    return ante_bet+call_bet
                elif player_hand['handName']=='full house':
                    ante_bet = self.bet_size*3
                    return ante_bet+call_bet
                elif player_hand['handName']=='flush':
                    ante_bet = self.bet_size*2
                    return ante_bet+call_bet
                else:
                    ante_bet = self.bet_size
                    return ante_bet+call_bet
   
class CasinoHoldNode:
    def __init__(self,info_set):
        self.info_set = info_set
        self.num_actions = 2
        self.regret_sum = np.zeros(self.num_actions)
        self.strategy_sum = np.zeros(self.num_actions)
        self.strategy = np.repeat(1/self.num_actions,self.num_actions)
    
    def get_strategy(self):
        # Thresholding using 0.001 instead of 0 prevents unecessary traversals
        # Using the regret[regret<0] is faster than the np.clip method
        regret_sum = self.regret_sum
        regret_sum[regret_sum<0.001] = 0
        normalizing_sum = sum(regret_sum)
        if normalizing_sum==0:
            self.strategy = [1/self.num_actions,self.num_actions]
        else:
            self.strategy =  regret_sum/normalizing_sum
        # Resetting strategy sums
        # By not including strategies of early iterations, it helps improves convergence
        # Leads to faster convergence as well
        self.strategy_sum+=self.strategy
        return self.strategy

    def get_average_strategy(self):
        strategy_sum = self.strategy_sum
        strategy_sum[strategy_sum<0.001] = 0
        normalizing_sum = sum(strategy_sum)
        if normalizing_sum==0:
            return [1/self.num_actions,self.num_actions]
        else:
            return strategy_sum/normalizing_sum
    
    def reset_regret(self):
        self.strategy_sum = np.zeros(self.num_actions)
        self.regret_sum = np.zeros(self.num_actions)

trainer = CasinoHold(1)

# %%
trainer.train(50000000)
#%%
import pickle
with open('casino_model.pkl','wb') as f:
    pickle.dump(trainer.node_map,f)
# %%
for i in (trainer.node_map):
    trainer.node_map[i].strategy = [round(x,2) for x in trainer.node_map[i].strategy]