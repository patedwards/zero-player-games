"""
This file contains the base class for all agents.
"""

import random
import uuid
from typing import final, List
from abc import ABC, abstractmethod
import logging
import numpy as np


# @dataclass
class AgentTypes:
    """
    A class containing the agent types.
    """
    boid = "boid"
    ravenoid = "ravenoid"
    agent = "agent"
    dead = "dead"
    food = "food"
    poison = "poison"


class Agent(ABC):
    """
    Todo: add docstring
    """

    def __init__(
        self, x: float, y: float, velocity=None, controller=None, will_log=False
    ):
        """
        Initialize the agent, this can include things like:
         - the controller being used
         - starting position and velocity
         - any other parameters related to the specific simulation
        """
        self.id: str = str(uuid.uuid4())  # unique identifier for each agent
        self.controller = controller
        self.position: np.ndarray = np.array([x, y], dtype=float)
        if velocity is not None:
            self.velocity: np.ndarray = velocity
        else:
            self.velocity: np.ndarray = np.array(
                [random.random() * 2 - 1, random.random() * 2 - 1]
            )
        self.h3_index: str = None
        self.nearby_agents = []
        self.will_log = will_log
        self.agent_type = AgentTypes.agent
        self.report_position()

    def __repr__(self):
        return (
            f"Agent(id={self.id}, position={self.position}, velocity={self.velocity})"
        )

    def add_h3_index(self, h3_index: str) -> None:
        """
        Add an h3 index to the agent.
        """
        self.h3_index = h3_index

    @final
    def report_position(self) -> None:
        """
        Report the agent's position and velocity to the controller.
        """

        self.controller.report_position(self)
        if self.will_log:
            # log the report
            logging.info("%s", self)

    @final
    def get_nearby_agents(self) -> List:
        """
        Get a list of nearby agents.
        """
        nearby_agents = self.controller.find_nearby(self.id)

        if self.will_log:
            # log the report
            logging.info("Nearby agents: %s", nearby_agents)
        return nearby_agents

    @final
    def update(self) -> None:
        """
        Update the agent's position and velocity.
        """
        if self.agent_type == AgentTypes.dead:
            self.report_position()
            return
        self.nearby_agents = self.get_nearby_agents()
        steering = self.steer()
      
        self.perform_step_logic(steering)
        self.handle_boundaries()
        self.report_position()

    @abstractmethod
    def steer(self) -> np.ndarray:
        """
        Calculate steering forces based on agent interactions and environmental factors.
        This might set a desired change in velocity but does not directly update the
        agent's position.
        """

    @abstractmethod
    def perform_step_logic(self, steering: np.ndarray) -> None:
        """
        Based on the current state of the agent, perform the logic required
        to update the agent's position and velocity.

        E.g:
        self.velocity += self.steer()
        # enforce speed limit
        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity /= np.linalg.norm(self.velocity)
            self.velocity *= self.max_speed
        self.position += self.velocity
        """

    @final
    def leave(self) -> None:
        """
        The agent is taking itself out of the simulation.
        """
        self.controller.leave(self.id)

    @final
    def handle_boundaries(self):
        """
        TODO: add docstring
        """
        if self.controller.world.wraparound:
            if self.position[0] > self.controller.world.top:
                overshoot = self.position[0] - self.controller.world.top
                self.position[0] = self.controller.world.bottom + overshoot
            elif self.position[0] < self.controller.world.bottom:
                overshoot = self.controller.world.bottom - self.position[0]
                self.position[0] = self.controller.world.top - overshoot

            if self.position[1] > self.controller.world.right:
                overshoot = self.position[1] - self.controller.world.right
                self.position[1] = self.controller.world.left + overshoot
            elif self.position[1] < self.controller.world.left:
                overshoot = self.controller.world.left - self.position[1]
                self.position[1] = self.controller.world.right - overshoot
        else:
            if self.position[0] > self.controller.world.top:
                overshoot = self.position[0] - self.controller.world.top
                self.position[0] = self.controller.world.top - overshoot
                self.velocity[0] *= -1
            elif self.position[0] < self.controller.world.bottom:
                overshoot = self.controller.world.bottom - self.position[0]
                self.position[0] = self.controller.world.bottom - overshoot
                self.velocity[0] *= -1
            if self.position[1] > self.controller.world.right:
                overshoot = self.position[1] - self.controller.world.right
                self.position[1] = self.controller.world.right - overshoot
                self.velocity[1] *= -1
            elif self.position[1] < self.controller.world.left:
                overshoot = self.controller.world.left - self.position[1]
                self.position[1] = self.controller.world.left - overshoot
                self.velocity[1] *= -1


class RandomWalker(Agent):
    """
    A simple agent that moves randomly.
    """

    def __init__(self, controller=None, will_log=False):
        x, y = controller.random_world_position()
        super().__init__(x, y, controller=controller, will_log=False)
        self.agent_type = AgentTypes.agent

    def steer(self) -> np.ndarray:
        """
        Calculate steering forces based on agent interactions and environmental factors.
        This might set a desired change in velocity but does not directly update the
        agent's position.
        """
        return np.array([random.random() * 2 - 1, random.random() * 2 - 1])

    def perform_step_logic(self, steering: np.ndarray) -> None:
        """
        Based on the current state of the agent, perform the logic required
        to update the agent's position and velocity.

        E.g:
        self.velocity += self.steer()
        # enforce speed limit
        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity /= np.linalg.norm(self.velocity)
            self.velocity *= self.max_speed
        self.position += self.velocity
        """
        self.velocity += steering
        # enforce speed limit
        if np.linalg.norm(self.velocity) > self.controller.world.max_speed:
            self.velocity /= np.linalg.norm(self.velocity)
            self.velocity *= self.controller.world.max_speed
        self.position += self.velocity
