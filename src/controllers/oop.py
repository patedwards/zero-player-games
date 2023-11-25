# pylint: disable-all

"""
This controller is for simulations where all comms are handled by the controller,
in python i.e no network comms. This is useful for testing and debugging.
"""

import h3
import time
from controllers.base import Controller, SimpleWorld
from typing import Dict, List, Union, Optional

from functools import reduce

from agents.base import Agent

class OOPController(Controller):
    def __init__(self) -> None:
        super().__init__()
        self.agent_data: Dict[str, Agent] = {}
        self.h3_resolution: int = 0
        self.spatial_index: Dict[str, List[str]] = {}
        self.world = SimpleWorld()

    def report_position(self, agent: Agent) -> None:
        # if the agent has reported, get it's old h3 index and remove it from the spatial index
        if agent.id in self.agent_data:
            old_h3_index = self.agent_data[agent.id].h3_index
            self.spatial_index[old_h3_index].remove(agent.id)
        self.agent_data[agent.id] = agent
        h3_index = h3.geo_to_h3(agent.position[0], agent.position[1], self.h3_resolution)
        agent.add_h3_index(h3_index)
        # if there's no entry for this h3 index, create one
        if h3_index not in self.spatial_index:
            self.spatial_index[h3_index] = []
        # add the agent to the spatial index
        self.spatial_index[h3_index].append(agent.id)

    def find_nearby(self, agent_id: str) -> Union[Dict[str, str], List[Agent]]:
        if agent_id not in self.agent_data:
            return {"error": "Agent not found"}

        self_hex = self.agent_data[agent_id].h3_index
        nearby_hexes = h3.k_ring(self_hex, 2)
        nearby_hexes.add(self_hex)

        nearby_agents = []

        for hex in nearby_hexes:
            if hex in self.spatial_index:
                nearby_agents.extend([self.agent_data[i] for i in self.spatial_index[hex] if i != agent_id])

        return nearby_agents

    def get_agents(self) -> List[Agent]:
        return list(self.agent_data.values())

    def clear_agents(self) -> Dict[str, str]:
        self.agent_data.clear()
        return {"status": "success"}

    def shutdown(self) -> None:
        pass

    def leave(self, agent_id: str) -> Union[Dict[str, str], Dict[str, str]]:
        if agent_id in self.agent_data:
            del self.agent_data[agent_id]
            return {"status": "success"}
        else:
            return {"error": "Boid not found"}
