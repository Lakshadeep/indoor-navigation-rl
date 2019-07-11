import ai2thor.controller
from .env import Env
import math


class Ai2ThorEnv(Env):

    def __init__(self, *args, **kwargs):
        self._map = kwargs.get("map", 'FloorPlan201')
        self._task = kwargs.get("task", 'Television')
        self.controller = ai2thor.controller.Controller()
        self.controller.start()
        self.controller.reset(self._map)
        self.controller.step(dict(action='Initialize', gridSize=0.25))
        self.actions = [0, 1, 2, 3, 4]
        self.agent_pos = [0, 0]

    def reset(self):
        self.controller.reset('FloorPlan201')
        self.controller.step(dict(action='Initialize', gridSize=0.25))

    # take action
    def step(self, action):
        nextState = [0, 0, 0]
        reward = None
        done = None
        event = None
        if action == 0:  # left
            event = self.controller.step(dict(action='RotateLeft'))
            event = self.controller.step(dict(action='MoveAhead'))
        if action == 1:  # right
            event = self.controller.step(dict(action='RotateRight'))
            event = self.controller.step(dict(action='MoveAhead'))
        if action == 2:  # ahead
            event = self.controller.step(dict(action='MoveAhead'))
        if action == 3:  # back same direction
            event = self.controller.step(dict(action='MoveBack'))
        if action == 4:  # back with view
            event = self.controller.step(dict(action='RotateLeft'))
            event = self.controller.step(dict(action='RotateLeft'))
            event = self.controller.step(dict(action='MoveBack'))

        new_agent_pos = [event.metadata['agent']['position']
                         ['y'], event.metadata['agent']['position']['z']]
        print(new_agent_pos)

        if self.__get_distance(new_agent_pos[0], new_agent_pos[1], self.agent_pos[0], self.agent_pos[1]) < 0.01:
            nextState[1] = 1

        self.agent_pos = new_agent_pos

        for obj in event.metadata['objects']:
            if obj['visible'] and obj['objectType'] == self._task:
                print(self._task , "visible")
                nextState[0] = 1

        return nextState, reward, done

    def __get_distance(self, x1, y1, x2, y2):
        print(math.sqrt(((x1 - x2)**2) + ((y1 - y2)**2)))
        return math.sqrt(((x1 - x2)**2) + ((y1 - y2)**2))
