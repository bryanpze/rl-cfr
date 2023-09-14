import numpy as np
class State:
    def __init__(self,n):
        self.state = n
        self.val = 0
        self.left_state = max(n//4*4,n-1) 
        self.right_state = min(n//4*4+3,n+1) if n+1!=15 else 0
        self.up_state = n-4 if n//4!=0 else n
        if (n//4!=3):
            if n!=11:
                self.down_state = n+4
            else: self.down_state = 0  
        else: 
            self.down_state = n
        
    def update(self):
        print('current_state',self.state)
        V = 0
        if self.left_state!=0:
            print('left_state',self.left_state,states[self.left_state-1].state,'val',states[self.left_state-1].val)
            V+=0.25*states[self.left_state-1].val
        if self.right_state!=0:
            print('right_state',self.right_state,states[self.right_state-1].state,'val',states[self.right_state-1].val)
            V+=0.25*states[self.right_state-1].val
        if self.up_state!=0:
            print('up_state',self.up_state,states[self.up_state-1].state,'val',states[self.up_state-1].val)
            V+=0.25*states[self.up_state-1].val
        if self.down_state!=0:
            print('down_state',self.down_state,states[self.down_state-1].state,'val',states[self.down_state-1].val)
            V+=0.25*states[self.down_state-1].val
        
        self.val=V-1

states = []
for i in range(1,15):
    states.append(State(i))
print('currrrrr',len(states))
for i in range(0,1000):
    if np.random.rand()<0.5:
        for i in range(0,14):
            states[i].update()
    else:
        for i in range(13,-1,-1):
            states[i].update()
for i in states:
    print(i.val)