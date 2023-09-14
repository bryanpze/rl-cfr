import numpy as np
player_hold = [8,2]
dealer_hold = [1]
cards = [i if i<10 else 10 for i in range (1,14)] * 4
cards.remove(8)
cards.remove(2)
cards.remove(1)

def draw():
    a = np.random.choice(cards_left)
    cards_left.remove(a)
    return a
#Double down strategy
double_wins_ls = []
for i in range(10000):
    double_wins = 0
    double_draws = 0
    double_loss = 0
    rounds = 400
    while rounds!=0:
        cards_left = cards.copy()
        player = player_hold.copy()
        dealer = dealer_hold.copy()
        dealer_down = np.random.choice(cards_left)
        if dealer_down==10:
            continue
        cards_left.remove(dealer_down)
        dealer.append(dealer_down)
        dealer_sum = sum(dealer)
        player_draw = np.random.choice(cards_left)
        if player_draw==1 and sum(player)+11<=21:
            player_sum = sum(player)+11
            player.append(1)
        else:
            player.append(player_draw)        
            player_sum = sum(player)
        cards_left.remove(player_draw)

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
            double_loss+=1
        elif (player_sum>dealer_sum and player_sum<=21) or (dealer_sum>21):
            double_wins+=1
        elif player_sum==dealer_sum:
            double_draws+=1
    double_wins_ls.append(double_wins-double_loss)
print(f'average excess of wins over losses: {sum(double_wins_ls)/len(double_wins_ls)}')
#Should print 5,same as book



#Correct drawing strategy
correct_drawing_wins_ls = []
for i in range(10000):
    hard_standing = {
            17:[7,8,9,10,1],
            16:[],
            15:[],
            14:[],
            13:[2,3],
            12:[4,5,6]
    }
    correct_drawing_wins = 0
    correct_drawing_draws = 0
    correct_drawing_loss = 0
    rounds = 200
    while rounds!=0:
        cards_left = cards.copy()
        player = player_hold.copy()
        dealer = dealer_hold.copy()
        round_hard_standing = hard_standing.copy()
        dealer_down = np.random.choice(cards_left)
        
        if dealer_down==10:
            continue
        cards_left.remove(dealer_down)
        dealer.append(dealer_down)
        dealer_sum = sum(dealer)
        player_sum = 10
        while player_sum<17:
            a = draw()
            if a==1 and len(player)==2:
                player.append(1)
                player_sum = 21
            else: 
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
        if player_sum>21 or (dealer_sum<=21 and player_sum<dealer_sum):
            correct_drawing_loss+=1
        elif (player_sum>dealer_sum and player_sum<=21) or (dealer_sum>21):
            correct_drawing_wins+=1
        elif player_sum==dealer_sum:
            correct_drawing_draws+=1
    correct_drawing_wins_ls.append(correct_drawing_wins-correct_drawing_loss)
print(f'average excess of wins over losses: {sum(correct_drawing_wins_ls)/len(correct_drawing_wins_ls)}')
#prints 17.2 in 200 hands, book says excess of wins over losses of 17.2 hands in 400 hands



