# pylint: disable-all
import gymnasium as gym
from gymnasium import spaces
import pygame


import numpy as np
import sys, os
import random
from controllers.oop import OOPController
from visualization.vis import Vis
from agents.boid import Boid, RavenoidWithSteeringWheel


class RavenChasingBoids(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(
        self, n_boids, render_mode=None, controller=OOPController, window_size=256,
        observation_type="visual"
    ):
        self.controller_class = controller
        self.n_boids = n_boids
        self.render_mode = render_mode
        self.window_size = window_size
        self.setup_simulation()
        self.history = []
        self.observation_type = observation_type
        self.previous_action = None

    def setup_simulation(self):
        self.controller = self.controller_class()
        self.n_steps = 0
        # add n_walkers boids to the simulation
        for _ in range(self.n_boids):
            self.controller.report_position(Boid(controller=self.controller))
        # add a ravenoid
        self.ravenoid = RavenoidWithSteeringWheel(controller=self.controller)
        self.controller.report_position(self.ravenoid)

        # Unused? self.image_size = self.controller.world.width, self.controller.world.height

        # Use a discrete observation space broken into 8 directions, where
        # we'll count the number of boids in each direction

        # TODO: do we need float64 here? Can we use float32?
        self.observation_space = spaces.Box(
            low=0, high=100, shape=(8,), dtype=np.float64
        )

        # Define the action space
        self.action_space = spaces.Discrete(9)
        self._action_to_direction = {
            0: [1.0, 0.0],  # Right
            1: [1.0, 1.0],  # Down-Right
            2: [0.0, 1.0],  # Down
            3: [-1.0, 1.0],  # Down-Left
            4: [-1.0, 0.0],  # Left
            5: [-1.0, -1.0],  # Up-Left
            6: [0.0, -1.0],  # Up
            7: [1.0, -1.0],  # Up-Right
            8: [0.0, 0.0],  # No movement
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

    def get_visual_observation(self):
        human_mode = self.render_mode == "human"
        agents = self.controller.get_agents()
        # make the center the round position of the ravenoid
        center = np.round(self.ravenoid.position).astype(int)
        color_map = {
            "boid": (255, 255, 255),
            "ravenoid": (0, 0, 255),
            "dead": (
                0,
                0,
                0,
            ),  # make the dead boids black as they are invisible to the Ravenoid
        }
        frame = self.vis.draw_agents(
            agents,
            human_mode=human_mode,
            recenter_position=center,
            crop_size=80,
            color_map=color_map,
        )
        return frame

    def get_array_observation(self):
        # TODO: this won't have the ability to see over to the next boundary
        nearby_agents = self.ravenoid.nearby_agents
        sight_distance = 40
        distances = []
        angles = []
        for agent in nearby_agents:
            if agent.id == self.ravenoid.id or agent.agent_type != "boid":
                continue
            distance = np.linalg.norm(agent.position - self.ravenoid.position)
            if distance > sight_distance:
                continue
            angle = np.arctan2(
                agent.position[1] - self.ravenoid.position[1],
                agent.position[0] - self.ravenoid.position[0],
            )
            if angle < 0:
                angle += 2 * np.pi
            distances.append(distance)
            angles.append(angle)
        # for each direction, count the number of agents in that direction
        counts = np.zeros(8)
        for distance, angle in zip(distances, angles):
            direction = int(np.round(angle / (2 * np.pi) * 8)) % 8
            counts[direction] += 1
        return counts

    def _get_obs(self):
        if self.observation_type == "visual":
            return self.get_visual_observation()
        elif self.observation_type == "array":
            return self.get_array_observation()

    def _get_info(self):
        return {}

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        print(
            f"{self.n_steps} steps taken. Average steps per episode: {np.mean(self.history)}"
        )
        super().reset(seed=seed)
        self.setup_simulation()
        info = self._get_info()
        observation = self._get_obs()

        return observation, info

    def take_action(self, action):
        steering = self._action_to_direction[action]
        self.ravenoid.update_steering(steering)
        
        self.ravenoid.steer()

    def step(self, action: int) -> tuple:
        self.take_action(action)
        self.n_steps += 1
        for agent in self.controller.get_agents():
            agent.update()

        if self.render_mode == "human":
            self._render_frame()

        observation = self._get_obs()
        reward = 10*self.ravenoid.kill_count
        if self.previous_action != action:
            reward += 0.01
        self.previous_action = action
        terminated = False

        # count the number of boids that are alive
        n_boids_alive = 0
        for agent in self.controller.get_agents():
            if agent.agent_type == "boid":
                n_boids_alive += 1

        # if the raven has killed 5 boids over the course of the episode, terminate
        if self.n_boids - n_boids_alive >= 10:
            terminated = True
            self.history.append(self.n_steps)

        if self.n_steps > 10000:
            terminated = True
            self.history.append(self.n_steps)

        info = self._get_info()
        truncated = False

        return observation, reward, terminated, truncated, info

    def render(self):
        if self.render_mode == "rgb_array":
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
