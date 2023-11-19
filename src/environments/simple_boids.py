# pylint: disable-all
import gymnasium as gym
from gymnasium import spaces
import pygame


import numpy as np
import sys, os
import random
from controllers.oop import OOPController
from visualization.vis import Vis
from agents.boid import Boid, Ravenoid


class PureBoinds(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, n_walkers, render_mode=None, controller=OOPController, window_size=256):
        self.controller = controller()

        # add n_walkers random walkers to the simulation
        for _ in range(n_walkers):
            self.controller.report_position(Boid(controller=self.controller))

        self.window_size = window_size  # Size of the PyGame window
        self.image_size = self.controller.world.width, self.controller.world.height
        self.render_mode = render_mode
        self.setup_simulation()

    def setup_simulation(self):
        # Define the observation space as an image
        self.observation_space = spaces.Box(
            low=0,
            high=255,
            shape=(self.image_size[0], self.image_size[1], 3),
            dtype=np.uint8,
        )

        # Define the action space
        self.action_space = spaces.Discrete(5)
        self._action_to_direction = {
            0: [1.0, 0.0],  # Right
            1: [0.0, 1.0],  # Up
            2: [-1.0, 0.0],  # Left
            3: [0.0, -1.0],  # Down
            4: [0.0, 0.0],  # Don't change velocity
        }

        assert (
            self.render_mode is None
            or self.render_mode in self.metadata["render_modes"]
        )

        """
        If human-rendering is used, `self.window` will be a reference
        to the window that we draw to. `self.clock` will be a clock that is used
        to ensure that the environment is rendered at the correct framerate in
        human-mode. They will remain `None` until human-mode is used for the
        first time.
        """
        self.window = None
        self.clock = None

        # init the visualization state
        self.vis = Vis(screen_height=self.window_size, screen_width=self.window_size)

    def _get_obs(self):
        pass

    def _get_info(self):
        pass

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)
        self.setup_simulation()
        info = self._get_info()
        observation = self._get_obs()

        return (observation, info)

    def take_action(self, action):
        # no action is taken for random walkers
        pass

    def step(self, action: int) -> tuple:
        action  # ignoring the action
        for agent in self.controller.get_agents():
            agent.update()

        if self.render_mode == "human":
            self._render_frame()

        observation = self._get_obs()
        reward = 0
        terminated = False

        return observation, reward, terminated, False

    def render(self):
        if self.render_mode == "human":
            return self._render_frame()

    def _render_frame(self):
        human_mode = self.render_mode == "human"
        agents = self.controller.get_agents()
        frame = self.vis.draw_agents(agents, human_mode=human_mode)
        return frame

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

class BoidsWithRavenoid(PureBoinds):
    def __init__(self, n_walkers, render_mode=None, controller=OOPController, window_size=256):
        self.controller = controller()

        # add n_walkers random walkers to the simulation
        for _ in range(n_walkers):
            self.controller.report_position(Boid(controller=self.controller))

        # add a ravenoid
        self.controller.report_position(Ravenoid(controller=self.controller))
        self.controller.report_position(Ravenoid(controller=self.controller))
        self.controller.report_position(Ravenoid(controller=self.controller))

        self.window_size = window_size  # Size of the PyGame window
        self.image_size = self.controller.world.width, self.controller.world.height
        self.render_mode = render_mode
        self.setup_simulation()