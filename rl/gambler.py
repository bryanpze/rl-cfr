import numpy as np
import matplotlib.pyplot as plt
class State:
    def __init__(self,n):
        self.n = n
        self.value = np.random.rand()
        self.actions = list(range(1,min(n,100-n)+1))
        self.highest_action = 0

states = [State(x) for x in range(101)]
states[0].value = 0
states[-1].value = 0
for i in range(10000):
    for j in states[1:100]:
        # print(f'Current State {j.n}')
        #choose an action, 0.4 u get to state + action , 0.6 u get to state-action
        highest_value = 0
        for m in j.actions:
            value=0
            if j.n+m==100:
                value=0.4+0.6*(states[j.n-m].value)
            elif j.n+m<100:
                value=0.4*(states[j.n+m].value)+0.6*(states[j.n-m].value)
            if value>highest_value:
                highest_value=value
                j.highest_action = m
        # print(f'Highest Value {highest_value}')
        j.value = highest_value
state_values = []
state_actions = []
for i in states:
    state_values.append(i.value)
    state_actions.append(i.highest_action)
# plt.plot(state_values)
plt.plot(state_actions)
