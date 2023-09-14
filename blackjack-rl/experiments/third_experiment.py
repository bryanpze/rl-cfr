import numpy as np
cards = [i if i<10 else 10 for i in range (1,14)] * 4
cards.remove(6)
cards.remove(6)
cards.remove(5)
player_hold = [6,6]
dealer_hold = [5]

def draw():
    a = np.random.choice(cards_left)
    cards_left.remove(a)
    return a
stand_wins_ls = []
for i in range(10000):
    stand_wins = 0
    stand_draws = 0
    stand_loss = 0
    rounds = 100
    while rounds!=0:
        cards_left = cards.copy()
        player = player_hold.copy()
        dealer = dealer_hold.copy()
        player_sum =12
        dealer_down = np.random.choice(cards_left)
        dealer.append(dealer_down)
        dealer_sum = sum(dealer)
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
        if player_sum>21 or (dealer_sum<=21 and player_sum<dealer_sum):
            stand_loss+=1
        elif (player_sum>dealer_sum and player_sum<=21) or (dealer_sum>21):
            stand_wins+=1
        elif player_sum==dealer_sum:
            stand_draws+=1
    stand_wins_ls.append(stand_wins-stand_loss)
print(f'average excess of wins over losses: {sum(stand_wins_ls)/len(stand_wins_ls)}')
#Should print -10.2, same as book

split_wins_ls = []
for i in range(10000):
    split_wins = 0
    split_draws = 0
    split_loss = 0
    rounds = 100
    soft_standing = {
            19: [1,2,3,4,5,6,7,8,9,10],
            18:[1,2,3,4,5,6,7,8]
        }
    hard_standing = {
            17:[2,3,4,5,6,7,8,9,10,1],
            16:[2,3,4,5,6],
            15:[2,3,4,5,6],
            14:[2,3,4,5,6],
            13:[2,3,4,5,6],
            12:[4,5,6]
    }
    while rounds!=0:
        cards_left = cards.copy()
        round_hard_standing_1 = hard_standing.copy()
        round_hard_standing_2 = hard_standing.copy()
        two_add = np.random.choice(cards_left,size = 2,replace=False)
        player_1 = [6,two_add[0]]
        player_2 = [6,two_add[1]]
        dealer = dealer_hold.copy()
        player_1_sum =sum(player_1)
        player_2_sum = sum(player_2)
        dealer_down = np.random.choice(cards_left)
        dealer.append(dealer_down)
        dealer_sum = sum(dealer)
        while player_1_sum<12:
            if 1 in player_1:
                player_1_copy = player_1.copy()
                player_1_copy.remove(1)
                if len(player_1_copy)>1:
                    if sum(player_1_copy)==7 or sum(player_1_copy)==8 or sum(player_1_copy)==9 or sum(player_1_copy)==10:
                        if sum(player_1_copy)==9:
                            player_1_sum = 20
                        elif sum(player_1_copy)==10:
                            player_1_sum = 21
                        elif sum(player_1_copy)==7:
                            if dealer[0] not in soft_standing[18]:
                                a = draw()
                                player_1.append(a)
                                player_1_sum = sum(player_1)
                            else:
                                player_1_sum = 18
                        elif sum(player_1_copy)==8:
                            if dealer[0] not in soft_standing[19]:
                                a = draw()
                                player_1.append(a)
                                player_1_sum = sum(player_1)
                            else:
                                player_1_sum = 19
                    else:
                        a = draw()
                        player_1.append(a)
                        player_1_sum = sum(player_1)
                else:
                    if (player_1_copy[0])==7 or (player_1_copy[0])==8 or (player_1_copy[0])==9 or (player_1_copy[0])==10:
                        if (player_1_copy[0])==9:
                            player_1_sum = 20
                        elif (player_1_copy[0])==10:
                            player_1_sum = 21
                        elif (player_1_copy[0])==7:
                            if dealer[0] not in soft_standing[18]:
                                a = draw()
                                player_1.append(a)
                                player_1_sum = sum(player_1)
                            else:
                                player_1_sum = 18
                        elif (player_1_copy[0])==8:
                            if dealer[0] not in soft_standing[19]:
                                a = draw()
                                player_1.append(a)
                                player_1_sum = sum(player_1)
                            else:
                                player_1_sum = 19
                    else:
                                a = draw()
                                player_1.append(a)
                                player_1_sum = sum(player_1)                    
            else:
                a = draw()
                player_1.append(a)
                player_1_sum = sum(player_1)
        if  player_1_sum==16 and not (10 in player_1 and 6 in player_1) and not (9 in player_1 and 7 in player_1):
            round_hard_standing_1[16] = [2,3,4,5,6,10]
        if  player_1[0]==7 and player_1[1]==7:
            round_hard_standing_1[14] = [2,3,4,5,6,10]
        while player_1_sum in round_hard_standing_1 and (dealer[0] not in round_hard_standing_1[player_1_sum]):
            a = draw()
            player_1.append(a)
            player_1_sum = sum(player_1)
        
        while player_2_sum<12:
            if 1 in player_2:
                player_2_copy = player_2.copy()
                player_2_copy.remove(1)
                if len(player_2_copy)>1:
                    if sum(player_2_copy)==7 or sum(player_2_copy)==8 or sum(player_2_copy)==9 or sum(player_2_copy)==10:
                        if sum(player_2_copy)==9:
                            player_2_sum = 20
                        elif sum(player_2_copy)==10:
                            player_2_sum = 21
                        elif sum(player_2_copy)==7:
                            if dealer[0] not in soft_standing[18]:
                                a = draw()
                                player_2.append(a)
                                player_2_sum = sum(player_2)
                            else:
                                player_2_sum = 18
                        elif sum(player_2_copy)==8:
                            if dealer[0] not in soft_standing[19]:
                                a = draw()
                                player_2.append(a)
                                player_2_sum = sum(player_2)
                            else:
                                player_2_sum = 19
                    else:
                        a = draw()
                        player_2.append(a)
                        player_2_sum = sum(player_2)
                else:
                    if (player_2_copy[0])==7 or (player_2_copy[0])==8 or (player_2_copy[0])==9 or (player_2_copy[0])==10:
                        if (player_2_copy[0])==9:
                            player_2_sum = 20
                        elif (player_2_copy[0])==10:
                            player_2_sum = 21
                        elif (player_2_copy[0])==7:
                            if dealer[0] not in soft_standing[18]:
                                a = draw()
                                player_2.append(a)
                                player_2_sum = sum(player_2)
                            else:
                                player_2_sum = 18
                        elif (player_2_copy[0])==8:
                            if dealer[0] not in soft_standing[19]:
                                a = draw()
                                player_2.append(a)
                                player_2_sum = sum(player_2)
                            else:
                                player_2_sum = 19
                    else:
                                a = draw()
                                player_2.append(a)
                                player_2_sum = sum(player_2)                    
            else:
                a = draw()
                player_2.append(a)
                player_2_sum = sum(player_2)
        if  player_2_sum==16 and not (10 in player_2 and 6 in player_2) and not (9 in player_2 and 7 in player_2):
            round_hard_standing_2[16] = [2,3,4,5,6,10]
        if  player_2[0]==7 and player_2[1]==7:
            round_hard_standing_2[14] = [2,3,4,5,6,10]
        while player_2_sum in round_hard_standing_2 and (dealer[0] not in round_hard_standing_2[player_2_sum]):
            a = draw()
            player_2.append(a)
            player_2_sum = sum(player_2)

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
        
        if player_1_sum>21 or (dealer_sum<=21 and player_1_sum<dealer_sum):
            split_loss+=1
        elif (player_1_sum>dealer_sum and player_1_sum<=21) or (dealer_sum>21):
            split_wins+=1
        elif player_1_sum==dealer_sum:
            split_draws+=1
        if player_2_sum>21 or (dealer_sum<=21 and player_2_sum<dealer_sum):
            split_loss+=1
        elif (player_2_sum>dealer_sum and player_2_sum<=21) or (dealer_sum>21):
            split_wins+=1
        elif player_2_sum==dealer_sum:
            split_draws+=1
    split_wins_ls.append(split_wins-split_loss)
print(f'average excess of wins over losses: {sum(split_wins_ls)/len(split_wins_ls)}')
#Gets 7.83 instead of 27.4

