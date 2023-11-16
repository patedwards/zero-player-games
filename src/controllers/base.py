# pylint: disable-all
from abc import ABC, abstractmethod
from typing import Dict, List, final
import random

class SimpleWorld:
    wraparound = True
    top = 256
    bottom = 0
    left = 0
    right = 256
    width = right - left
    height = top - bottom
    max_speed = 1

# Define the abstract base class 'Controller'
class Controller(ABC):
    """
    The controller can be thought of as the interface between the
    agents and the network. Instances of this class can be either
    a property of an Agent itself, or a Client that is monitoring
    the agents. Some methods will only be called by the agent,
    others will only be called by the client, and some will be
    called by both.
    """
    @abstractmethod
    def __init__(self):
        """
        Initialize the controller, this can include things like:
         - setting up connections to the network
         - starting background threads.
        """
        self.world = SimpleWorld()

    @abstractmethod
    def report_position(self, agent_id, position, velocity):
        """
        This is called by the agent to report its position to the
        controller and through the controller to the network.
        """
        pass

    @abstractmethod
    def find_nearby(self, agent_id: str) -> Dict[str, List[float]]:
        """
        This is called by the agent to find nearby agents.
        """
        pass

    @abstractmethod
    def get_agents(self):
        """
        This is called by the agent/client to get all agents.
        """
        pass

    @abstractmethod
    def clear_agents(self):
        """
        This is called by a client to clear all agents.
        """
        pass

    @abstractmethod
    def leave(self, agent_id):
        pass

    @abstractmethod
    def shutdown(self):
        pass

    @final
    def random_world_position(self):
        return (
            random.uniform(self.world.bottom, self.world.top),
            random.uniform(self.world.left, self.world.right),
        )

