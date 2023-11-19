# pylint: disable-all

import numpy as np

class JustFollowModel:
    def __init__(self, env):
        self.action_space = env.action_space
        self.env = env

    def predict(self, observation, state=None, episode_start=None, deterministic=None):
        action = np.argmax(observation)
        print(action, observation)
        return action, state

    def get_env(self): return self.env