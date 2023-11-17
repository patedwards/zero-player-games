"""
Todo: docstring
"""

import random
import dataclasses

import numpy as np
from agents.base import Agent, AgentTypes
from typing import List, Dict, Union
from numpy import ndarray

REFLECTION = False


def calculate_distance(a, b):
    """
    param a: np.array
    param b: np.array

    return: float
    """
    return np.linalg.norm(a - b)


@dataclasses.dataclass
class BoidParameters:
    """TODO: add docstring"""

    cohesion_distance: float = 25
    alignment_tolerance: float = 30
    separation_tolerance: float = 10
    max_speed: float = 2
    max_force: float = 0.2
    cohesion_weight: float = 0.1
    separation_weight: float = 0.05
    alignment_weight: float = 0.05
    boid_death_zone: float = 3


class Boid(Agent):
    """
    A simple agent that moves randomly.
    """

    def __init__(self, controller=None, will_log=False):
        x, y = controller.random_world_position()
        self.parameters = BoidParameters()
        super().__init__(x, y, controller=controller, will_log=False)
        self.agent_type = AgentTypes.boid
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.array([random.random() * 2 - 1, random.random() * 2 - 1])
        self.agent_type = AgentTypes.boid
        # enforce speed limit
        if np.linalg.norm(self.velocity) > self.parameters.max_speed:
            self.velocity /= np.linalg.norm(self.velocity)
            self.velocity *= self.parameters.max_speed

    def steer(self) -> np.ndarray:
        """
        Calculate steering forces based on agent interactions and environmental factors.
        This might set a desired change in velocity but does not directly update the
        agent's position.
        """
        boids = self.nearby_agents 
        # ignore dead boids
        boids = [boid for boid in boids if boid.agent_type != AgentTypes.dead]
        v1 = self.rule_cohesion(boids)
        v2 = self.rule_alignment(boids)
        v3 = self.rule_separation(boids)
        return v1 + v2 + v3

    def rule_cohesion(self, boids):
        """
        TODO: add docstring
        """
        center = np.array([0.0, 0.0])  # Initializing with float values
        count = 0
        for boid in boids:
            distance = calculate_distance(boid.position, self.position)
            if boid.agent_type == AgentTypes.ravenoid:
                return np.array([0.0, 0.0])
            elif (
                distance < self.parameters.cohesion_distance
            ):  # within a certain distance
                center += boid.position
                count += 1
        if count == 0:
            return np.array([0.0, 0.0])
        center /= count
        return (center - self.position) * self.parameters.cohesion_weight

    def rule_alignment(self, boids):
        """
        TODO: add docstring
        """
        mean_velocity = np.array([0.0, 0.0])  # Initializing with float values
        count = 0

        for boid in boids:
            distance = calculate_distance(boid.position, self.position)
            if boid.agent_type == AgentTypes.ravenoid:
                # then turn 90 degrees
                new_velocity = np.array(
                    [self.velocity[1], -self.velocity[0]]
                )   
                return new_velocity * self.parameters.alignment_weight
            elif (
                distance < self.parameters.alignment_tolerance
            ):  # within a certain distance
                mean_velocity += boid.velocity
                count += 1
        if count == 0:
            return np.array([0.0, 0.0])
        mean_velocity /= count
        return mean_velocity * self.parameters.alignment_weight

    def rule_separation(self, boids):
        """
        TODO: add docstring
        """
        move = np.array([0.0, 0.0])  # Initializing with float values
        for boid in boids:
            distance = calculate_distance(boid.position, self.position)
            if boid.agent_type == AgentTypes.ravenoid:
                # then turn 90 degrees
                new_velocity = np.array(
                    [self.velocity[1], -self.velocity[0]]
                )
                return new_velocity * self.parameters.separation_weight
            elif (
                distance < self.parameters.separation_tolerance
            ):  # within a certain distance
                move -= boid.position - self.position
        return move * self.parameters.separation_weight

    def perform_step_logic(self, steering):
        """
        TODO: add docstring
        """
        if np.linalg.norm(steering) > self.parameters.max_force:
            steering /= np.linalg.norm(steering)
            steering *= self.parameters.max_force
        self.velocity += steering
        if np.linalg.norm(self.velocity) > self.parameters.max_speed:
            self.velocity /= np.linalg.norm(self.velocity)
            self.velocity *= self.parameters.max_speed
        self.position += self.velocity


class Ravenoid(Boid):
    """
    A simple agent that chases boids, using internal logic only.
    """

    def __init__(self, controller=None, will_log=False):
        super().__init__(
            controller=controller,
        )
        self.agent_type = AgentTypes.ravenoid

    def perform_step_logic(self, steering):
        super().perform_step_logic(steering)
        # and then if there are any boids nearby, kill them
        boids = self.nearby_agents
        for boid in boids:
            if boid.agent_type == AgentTypes.boid:
                distance = calculate_distance(boid.position, self.position)
                if distance < self.parameters.boid_death_zone:
                    boid.agent_type = AgentTypes.dead

class RavenoidWithSteeringWheel(Boid):
    """
    A ravenoid that takes actions based on the environment.
    """
    def __init__(self, controller=None, will_log=False):
        super().__init__(
            controller=controller,
        )
        self.agent_type = AgentTypes.ravenoid
        self.kill_count = 0
        self.steering_action = [0, 0]

    def steer(self) -> ndarray:
        return np.array(self.steering_action)

    def perform_step_logic(self, steering):
        super().perform_step_logic(steering)
        # and then if there are any boids nearby, kill them
        self.kill_count = 0
        boids = self.nearby_agents
        for boid in boids:
            if boid.agent_type == AgentTypes.boid:
                distance = calculate_distance(boid.position, self.position)
                if distance < self.parameters.boid_death_zone:
                    boid.agent_type = AgentTypes.dead
                    self.kill_count += 1
