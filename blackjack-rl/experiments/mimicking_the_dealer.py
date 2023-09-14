import numpy as np
cards = [i if i<10 else 10 for i in range (1,14)] * 4
def draw():
    a = np.random.choice(cards_left)
    cards_left.remove(a)
    return a
wins_ls = []
for i in range(10000):
    wins = 0
    draws = 0
    loss = 0
    rounds = 100
    while rounds!=0:
        cards_left = cards.copy()
        round = np.random.choice(cards_left,size = 4,replace=False)
        for i in round:
            cards_left.remove(i)
        dealer = [round[0],round[1]]
        player = [round[2],round[3]]
        player_sum = sum(player)
        dealer_sum = sum(dealer)
        while player_sum<17:
            if 1 in player:
                player_1_copy = player.copy()
                player_1_copy.remove(1)
                if len(player_1_copy)>1:
                    if sum(player_1_copy)<6:
                        a = draw()
                        player.append(a)
                        player_sum = sum(player)
                    elif sum(player_1_copy)<=10:
                        player_sum=11+sum(player_1_copy)
                    else:
                        if player_sum<17:
                            a = draw()
                            player.append(a)
                            player_sum = sum(player)
                else:
                    if (player_1_copy[0])<6 :
                        a = draw()
                        player.append(a)
                        player_sum = sum(player)
                    elif (player_1_copy[0])<=10:
                        player_sum=11+player_1_copy[0]
                    else:
                        if player_sum<17:
                            a = draw()
                            player.append(a)
                            player_sum = sum(player)
            else:
                if player_sum<17:
                    a = draw()
                    player.append(a)
                    player_sum = sum(player)
        while dealer_sum<17:
            if 1 in dealer:
                dealer_1_copy = dealer.copy()
                dealer_1_copy.remove(1)
                if len(dealer_1_copy)>1:
                    if sum(dealer_1_copy)<6:
                        a = draw()
                        dealer.append(a)
                        dealer_sum = sum(dealer)
                    elif sum(dealer_1_copy)<=10:
                        dealer_sum=11+sum(dealer_1_copy)
                    else:
                        if dealer_sum<17:
                            a = draw()
                            dealer.append(a)
                            dealer_sum = sum(dealer)
                else:
                    if (dealer_1_copy[0])<6 :
                        a = draw()
                        dealer.append(a)
                        dealer_sum = sum(dealer)
                    elif (dealer_1_copy[0])<=10:
                        dealer_sum=11+dealer_1_copy[0]
                    else:
                        if dealer_sum<17:
                            a = draw()
                            dealer.append(a)
                            dealer_sum = sum(dealer)
            else:
                if dealer_sum<17:
                    a = draw()
                    dealer.append(a)
                    dealer_sum = sum(dealer)
        rounds-=1
        if ((10 in player and 1 in player) and len(player)==2 and (dealer_sum<21 or (dealer_sum==21 and len(dealer)>2) or dealer_sum>21)):
            wins+=1.5
        else:
            if (player_sum>dealer_sum and player_sum<=21) or (player_sum<=21 and dealer_sum>21):
                wins+=1
            elif (player_sum<dealer_sum and dealer_sum<=21) or player_sum>21:
                loss+=1
            elif player_sum==dealer_sum:
                draws+=0
    wins_ls.append(wins-loss)
print(f'average excess of wins over losses: {sum(wins_ls)/len(wins_ls)}')
#5.13 instead of 5.73
