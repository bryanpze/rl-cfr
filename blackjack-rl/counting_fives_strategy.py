import numpy as np
import matplotlib.pyplot as plt
class Basic_Strategy:
    def __init__(self,ndecks=1,nrounds = 100,dd = False,ps = False):
        self.nrounds = nrounds
        self.dd = dd
        self.ps = ps
        self.payoff = 0
        self.cards = [i if i<10 else 10 for i in range (1,14)] * 4 * ndecks
        while 5 in self.cards:
            self.cards.remove(5)
        self.soft_standing = {
            19: [1,2,3,4,5,6,7,8,9,10],
            18:[1,2,3,4,5,6,7,8]
        }
        self.hard_standing = {
            17:[2,3,4,5,6,7,8,9,10,1],
            16:[2,3,4,5,6,7,8,9,10],
            15:[2,3,4,5,6,9,10],
            14:[2,3,4,5,6],
            13:[2,3,4,5,6],
            12:[2,3,4,5,6]
        }
        self.pair_splitting = {
            1:[1,2,3,4,5,6,7,8,9,10],
            2:[2,3,4,5,6,7,8],
            3:[2,3,4,5,6,7,8],
            4:[],
            5:[],
            6:[2,3,4,5,6],
            7:[2,3,4,5,6,7,8,9],
            8:[1,2,3,4,5,6,7,8,9,10],
            9:[2,3,4,5,6,7,8,9],
            10:[6]
        }
        if self.dd:
            self.pair_splitting[4] = [4]
        self.soft_doubling = {
            9:[6],
            8:[3,4,5,6],
            7:[2,3,4,5,6,],
            6:[2,3,4,5,6,7],
            5:[3,4,5,6],
            4: [3,4,5,6],
            3:[3,4,5,6],
            2:[3,4,5,6],
            1:[]
        }
        self.hard_doubling = {
            11:[1,2,3,4,5,6,7,8,9,10],
            10:[1,2,3,4,5,6,7,8,9,10],
            9:[2,3,4,5,6,7],
            8:[4,5,6]
        }
    def draw(self):
        a = np.random.choice(self.cards_left)
        self.cards_left.remove(a)
        return a
    def run_match(self,player,dealer,player_sum,dealer_sum,split):
        round_hard_standing = self.hard_standing.copy()
        round_hard_doubling = self.hard_doubling.copy()
        round_soft_doubling = self.soft_doubling.copy()
        if ((10 in player and 1 in player)  and (dealer_sum<21 or (dealer_sum==21 and len(dealer)>2) or dealer_sum>21)):
            if split:
                self.payoff+=1
            else:
                self.payoff+=1.5
        if 1 in player:
            if player[0]==1 and self.dd==True:
                if player[1] in round_soft_doubling and dealer[0] in round_soft_doubling[player[1]]:
                    a = self.draw()
                    player.append(a)
                    player_sum = sum(player)
                    if (player_sum>dealer_sum and player_sum<=21) or (player_sum<=21 and dealer_sum>21):
                        self.payoff+=2
                    elif (player_sum<dealer_sum and dealer_sum<=21) or player_sum>21:
                        self.payoff-=2
                    elif player_sum==dealer_sum:
                        self.payoff+=0
                    else:
                        print('error')
                    # print("DOUBLED")
                    # print(f'player {player} sum {player_sum} dealer {dealer} sum {dealer_sum}')
                    # print(self.payoff)
                    return
            elif player[1]==1 and self.dd==True:
                if player[0] in round_soft_doubling and dealer[0] in round_soft_doubling[player[0]]:
                    a = self.draw()
                    player.append(a)
                    player_sum = sum(player)
                    if (player_sum>dealer_sum and player_sum<=21) or (player_sum<=21 and dealer_sum>21):
                        self.payoff+=2
                    elif (player_sum<dealer_sum and dealer_sum<=21) or player_sum>21:
                        self.payoff-=2
                    elif player_sum==dealer_sum:
                        self.payoff+=0
                    else:
                        print('error')
                    # print("DOUBLED")
                    # print(f'player {player} sum {player_sum} dealer {dealer} sum {dealer_sum}')
                    # print(self.payoff)

                    return
        elif player_sum>=8 and player_sum<=11 and self.dd==True:
            if dealer[0] in round_hard_doubling[player_sum]:
                a = self.draw()
                player.append(a)
                player_sum = sum(player)
                if (player_sum>dealer_sum and player_sum<=21) or (player_sum<=21 and dealer_sum>21):
                    self.payoff+=2
                elif (player_sum<dealer_sum and dealer_sum<=21) or player_sum>21:
                    self.payoff-=2
                elif player_sum==dealer_sum:
                    self.payoff+=0
                else:
                    print('error')
                # print("DOUBLED")
                # print(f'player {player} sum {player_sum} dealer {dealer} sum {dealer_sum}')
                # print(self.payoff)
                return
        while player_sum<12:
            if 1 in player:
                player_1_copy = player.copy()
                player_1_copy.remove(1)
                if len(player_1_copy)>1:
                    if sum(player_1_copy)==7 or sum(player_1_copy)==8 or sum(player_1_copy)==9 or sum(player_1_copy)==10:
                        if sum(player_1_copy)==9:
                            player_sum = 20
                        elif sum(player_1_copy)==10:
                            player_sum = 21
                        elif sum(player_1_copy)==7:
                            if dealer[0] not in self.soft_standing[18]:
                                a = self.draw()
                                player.append(a)
                                player_sum = sum(player)
                            else:
                                player_sum = 18
                        elif sum(player_1_copy)==8:
                            if dealer[0] not in self.soft_standing[19]:
                                a = self.draw()
                                player.append(a)
                                player_sum = sum(player)
                            else:
                                player_sum = 19
                    else:
                        a = self.draw()
                        player.append(a)
                        player_sum = sum(player)
                else:
                    if (player_1_copy[0])==7 or (player_1_copy[0])==8 or (player_1_copy[0])==9 or (player_1_copy[0])==10:
                        if (player_1_copy[0])==9:
                            player_sum = 20
                        elif (player_1_copy[0])==10:
                            player_sum = 21
                        elif (player_1_copy[0])==7:
                            if dealer[0] not in self.soft_standing[18]:
                                a = self.draw()
                                player.append(a)
                                player_sum = sum(player)
                            else:
                                player_sum = 18
                        elif (player_1_copy[0])==8:
                            if dealer[0] not in self.soft_standing[19]:
                                a = self.draw()
                                player.append(a)
                                player_sum = sum(player)
                            else:
                                player_sum = 19
                    else:
                                a = self.draw()
                                player.append(a)
                                player_sum = sum(player)                    
            else:
                a = self.draw()
                player.append(a)
                player_sum = sum(player)
        if  player_sum==16 and not (10 in player and 6 in player) and not (9 in player and 7 in player):
            round_hard_standing[16] = [2,3,4,5,6,9,10]
        while player_sum in round_hard_standing and (dealer[0] not in round_hard_standing[player_sum]):
            a = self.draw()
            player.append(a)
            player_sum = sum(player)
        # print(f'player {player} sum {player_sum} dealer {dealer} sum {dealer_sum}')
        
        if (player_sum>dealer_sum and player_sum<=21) or (player_sum<=21 and dealer_sum>21):
            self.payoff+=1
        elif (player_sum<dealer_sum and dealer_sum<=21) or player_sum>21:
            self.payoff-=1
        elif player_sum==dealer_sum:
            self.payoff+=0            
        else:
            print('error')
        # print(self.payoff)
    def simulate(self):
        for i in range(self.nrounds):
            self.cards_left = self.cards.copy()
            print(self.cards_left)
            round = np.random.choice(self.cards_left,size = 4,replace=False)
            for i in round:
                self.cards_left.remove(i)
            dealer = [round[0],round[1]]
            player = [round[2],round[3]]
            player_sum = sum(player)
            dealer_sum = sum(dealer)
            while dealer_sum<17:
                if 1 in dealer:
                    dealer_1_copy = dealer.copy()
                    dealer_1_copy.remove(1)
                    if len(dealer_1_copy)>1:
                        if sum(dealer_1_copy)<6:
                            a = self.draw()
                            dealer.append(a)
                            dealer_sum = sum(dealer)
                        elif sum(dealer_1_copy)<=10:
                            dealer_sum=11+sum(dealer_1_copy)
                        else:
                            if dealer_sum<17:
                                a = self.draw()
                                dealer.append(a)
                                dealer_sum = sum(dealer)
                    else:
                        if (dealer_1_copy[0])<6 :
                            a = self.draw()
                            dealer.append(a)
                            dealer_sum = sum(dealer)
                        elif (dealer_1_copy[0])<=10:
                            dealer_sum=11+dealer_1_copy[0]
                        else:
                            if dealer_sum<17:
                                a = self.draw()
                                dealer.append(a)
                                dealer_sum = sum(dealer)
                else:
                    if dealer_sum<17:
                        a = self.draw()
                        dealer.append(a)
                        dealer_sum = sum(dealer)
            if self.ps:
                if player[0]==player[1]:
                    if dealer[0] in self.pair_splitting[player[0]]:
                        # print('SPLITTED')
                        a = self.draw()
                        b = self.draw()
                        hand_1 = [player[0],a]
                        hand_2 = [player[1],b]
                        hand_1_sum = sum(hand_1)
                        hand_2_sum = sum(hand_2)
                        self.run_match(hand_1,dealer,hand_1_sum,dealer_sum,split=True)
                        self.run_match(hand_2,dealer,hand_2_sum,dealer_sum,split=True)
                    else:
                        self.run_match(player,dealer,player_sum,dealer_sum,split=False)
                else:
                    self.run_match(player,dealer,player_sum,dealer_sum,split=False)
            else:
                self.run_match(player,dealer,player_sum,dealer_sum,split=False)
        return self.payoff   
gains = []
for i in range(10000):
    model = Basic_Strategy(ps=True,dd=True,ndecks=3)
    score = model.simulate()
    gains.append(score)
print(sum(gains)/len(gains))
plt.hist(gains,bins=[-np.inf,-39.9,-29.9,-19.9,-9.9,0.1,10.1,20.1,30.1,40.1,np.inf],alpha=0.65)
plt.axvline(sum(gains)/len(gains),linestyle='dashed',linewidth=1)