# Blackjack

Applying RL methods to approximate Blackjack strategies in Beat The Dealer by Edward Thorp

## Rules

Number Of Players: 1-7 (the fewer the number of players the better)
Most games, card dealt face down for all players, one card face up, one card face down for dealer
If blackjack, player receives 1.5 original bet
If player choose hit, card dealt face up, if bust turns hole cards

After each player draws, dealer turns up hole card, if total 16 or less draw, and continue until 17 or more. If ace brings total to 17 or more, stands
Some alter to draw on soft 17 or less

If player hole cards are numerically identical, may choose to turn cards face up and split. Equal amount of bet is placed on the second card. If split aces and get 10 not treated as blackjack but 21, same if split 10s and get aces.

Double down
After looking at whole cards, can choose to double bets and draw one and only one more card. Double down on split pairs allowed, except for split aces
Some restrict double downs to 10 and 11

Insurance
If dealer up card is ace, player may after checking his hole cards choose to place an additional bet equal AT MOST to half his bet
If dealer does has natural, side bet wins twice the amount

Actions
After getting hole cards, determine whether to hit,split, double down

## Basic Strategy

Edge of 0.12% over the house
In some casinos, narrow advantage as much as 0.6%
Hard Standing Numbers:
| You have | Dealer Shows | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | A |
| -------- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 17 | | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| 16 | | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | $\beta$ | 0 |
| 15 | | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 14 | | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | $\alpha$ | 0 |
| 13 | | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 12 | | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |

Draw on all hard totals of 11 or less, stand on hard totals of 18 or more
$\beta$ stand if (10,6) or (9,7)
$\alpha$ stand if (7,7)

Soft standing numbers:
| You have | Dealer Shows | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | A |
| -------- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 19 | | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| 18 | | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 |

Without doubling down, splitting pairs and insure: casino edge 2%

Soft Doubling:
| You have | Dealer Shows | 2 | 3 | 4 | 5 | 6 |
| -------- | ------------ | --- | --- | --- | --- | --- |
| A,7 | | 0 | 1 | 1 | 1 | 1 |
| A,6 | | 1 | 1 | 1 | 1 | 1 |
| A,5 | | 0 | 0 | 1 | 1 | 1 |
| A,4 | | 0 | 0 | 1 | 1 | 1 |
| A,3 | | 0 | 0 | 1 | 1 | 1 |
| A,2 | | 0 | 0 | 1 | 1 | 1 |
| A,A* | | 0 | 0 | 0 | 1 | 1 |
*Double down if can't be split

Hard Doubling:
| You have | Dealer Shows | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | A |
| -------- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 10 | | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| 9 | | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| 8 | | 0 | 0 | 0 | \* | \* | 0 | 0 | 0 | 0 | 0 |

Double down except with 6,2

Pair Splitting:
| You have | Dealer Shows | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | A |
| -------- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A,A | | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 10,10 | | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 9,9 | | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 8,8 | | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 7,7 | | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| 6,6 | | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| 5,5 | | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 4,4 | | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| 3,3 | | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| 2,2 | | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
