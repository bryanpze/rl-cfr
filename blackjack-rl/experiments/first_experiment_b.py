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
        cards_left.remove(1)
        dealer = [1]
        player_sum = 16
        dealer_down = np.random.choice(cards_left)
        if dealer_down==10:
            continue
        cards_left.remove(dealer_down)
        dealer.append(dealer_down)
        dealer_sum = sum(dealer)
        player_draw = np.random.choice(cards_left)
        cards_left.remove(player_draw)
        player_sum += player_draw
        if player_sum>21:
            loss+=1
            rounds-=1
            continue
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
        if dealer_sum>21 or player_sum>dealer_sum:
            wins+=1
        elif player_sum==dealer_sum:
            draws+=1
        else:
            loss+=1
    wins_ls.append(wins+0.5*draws)
    
print(sum(wins_ls)/len(wins_ls))
#Gets expected wins of 23.85 instead of 24.3