from typing import FrozenSet

from frozendict import frozendict  # type: ignore
from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.action.action import Action
from scpy.agent.agent import Agent
from scpy.predicate.predicate import Predicate
from scpy.situation.epistemic_situation import EpistemicSituation
from scpy.state.state import State


@dataclass(frozen=True, order=True)
class EpistemicCausalSetting:
    fluents: FrozenSet[Predicate] = Field(default_factory=frozenset)
    actions: FrozenSet[Action] = Field(default_factory=frozenset)
    agents: FrozenSet[Agent] = Field(default_factory=frozenset)

    def do(self, action: Action, situation: EpistemicSituation) -> EpistemicSituation:
        state = situation.state
        state_ = self.do_state(action, state)
        knowledge_relation = situation.knowledge_relation
        knowledge_relation_ = frozendict({
            agent: frozendict({
                self.do_state(action, k_state): log_probability for k_state, log_probability in relation.items()
            }) for agent, relation in knowledge_relation.items()
        })
        situation_ = EpistemicSituation(
            state=state_,
            previous_action=action,
            previous_situation=situation,
            knowledge_relation=knowledge_relation_
        )
        return situation_

    def do_state(self, action: Action, state: State) -> State:
        raise NotImplementedError

    def poss(self, action: Action, situation: EpistemicSituation) -> bool:
        return action in self.actions and self.poss_state(action, situation.state)

    def poss_state(self, action: Action, state: State) -> bool:
        raise NotImplementedError
