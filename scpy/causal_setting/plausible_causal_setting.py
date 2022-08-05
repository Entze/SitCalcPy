from typing import FrozenSet, Mapping

from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.action.action import Action
from scpy.agent.agent import Agent
from scpy.predicate.predicate import Predicate
from scpy.situation.plausible_situation import PlausibleSituation
from scpy.state.state import State


@dataclass(frozen=True, order=True)
class PlausibleCausalSetting:
    fluents: FrozenSet[Predicate] = Field(default_factory=frozenset)
    actions: Mapping[Action, Mapping[Action, int]] = Field(default_factory=frozenset)
    sensing_actions: FrozenSet[Action] = Field(default_factory=frozenset)
    agents: FrozenSet[Agent] = Field(default_factory=frozenset)

    def do(self, action: Action, situation: PlausibleSituation) -> PlausibleSituation:
        raise NotImplementedError

    def do_state(self, action: Action, state: State) -> State:
        raise NotImplementedError

    def poss(self, action: Action, situation: PlausibleSituation) -> bool:
        raise NotImplementedError

    def poss_state(self, action: Action, state: State) -> bool:
        raise NotImplementedError
