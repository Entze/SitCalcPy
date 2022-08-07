from typing import Mapping, FrozenSet

from frozendict import frozendict  # type: ignore
from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.action.action import Action
from scpy.agent.agent import Agent
from scpy.primitives import Predicate
from scpy.resource.resource import Resource
from scpy.situation.situation_with_resources import SituationWithResources
from scpy.state.state import State


@dataclass(frozen=True, order=True)
class CausalSettingWithResources:
    fluents: FrozenSet[Predicate] = Field(default_factory=frozenset)
    action_cost: Mapping[Action, Mapping[Resource, float]] = Field(default_factory=frozendict)
    agents: FrozenSet[Agent] = Field(default_factory=frozenset)

    def do(self, action: Action, situation: SituationWithResources) -> SituationWithResources:
        state = situation.state
        state_ = self.do_state(action, state)
        resources_ = dict(situation.resources)
        for resource, cost in self.action_cost[action].items():
            resources_[resource] -= cost
        situation_ = SituationWithResources(state=state_,
                                            previous_action=action,
                                            previous_situation=situation,
                                            resources=frozendict(resources_))
        return situation_

    def do_state(self, action: Action, state: State) -> State:
        raise NotImplementedError

    def poss(self, action: Action, situation: SituationWithResources) -> bool:
        if action not in self.action_cost:
            return False
        for resource, cost in self.action_cost[action].items():
            if situation.resources[resource] < cost:
                return False
        return self.poss_state(action, situation.state)

    def poss_state(self, action: Action, state: State) -> bool:
        raise NotImplementedError
