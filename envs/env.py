import numpy as np


class Env():

    def __init__(self, *args, **kwargs):
        self.posX = 0
        self.posY = 0
        self.actions = [0, 1, 2, 3]

    def reset(self):
        self.posX = 0
        self.posY = 0

    def step(self, action):
        nextState = None
        reward = None
        done = False
        '''
        Logic goes here
        '''
        return nextState, reward, done

    def randomAction(self):
        return np.random.choice(self.actions)

    # display environment
    def render(self):
        pass
