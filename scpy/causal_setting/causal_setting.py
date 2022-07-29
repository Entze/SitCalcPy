from typing import FrozenSet, Iterator, TypeAlias

from frozendict import frozendict  # type: ignore
from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.action.action import Action
from scpy.agent.agent import Agent
from scpy.predicate.predicate import Predicate
from scpy.situation.situation import Situation
from scpy.state.state import State

_CausalSetting: TypeAlias = 'CausalSetting'


@dataclass(frozen=True, order=True)
class CausalSetting:
    fluents: FrozenSet[Predicate] = Field(default_factory=frozenset)
    actions: FrozenSet[Action] = Field(default_factory=frozenset)
    # objects: Mapping[str, Function] = Field(default_factory=frozendict)
    agents: FrozenSet[Agent] = Field(default_factory=frozenset)

    def do_state(self, action: Action, state: State) -> State:
        raise NotImplementedError

    def _do_situation_without_knowledge_relation(self,
                                                 action: Action,
                                                 situation: Situation) -> Situation:
        state = situation.state
        state_ = self.do_state(action, state)
        situation_ = Situation(
            state=state_,
            previous_action=action,
            previous_situation=situation,
        )
        return situation_

    def do(self, action: Action, situation: Situation) -> Situation:
        state = situation.state
        state_ = self.do_state(action, state)
        knowledge_relation = situation.knowledge_relation
        knowledge_relation_ = frozendict({agent: frozenset(
            self._do_situation_without_knowledge_relation(action, alternative) for alternative in alternatives) for
            agent, alternatives in knowledge_relation.items()})
        situation_ = Situation(
            state=state_,
            previous_action=action,
            previous_situation=situation,
            knowledge_relation=knowledge_relation_
        )
        return situation_

    def poss_state(self, action: Action, state: State) -> bool:
        raise NotImplementedError

    def _poss(self, action: Action, situation: Situation) -> bool:
        return self.poss_state(action, situation.state)

    def poss(self, action: Action, situation: Situation) -> bool:
        return action in self.actions and self._poss(action, situation)

    def all_poss_actions_state(self, state: State) -> Iterator[Action]:
        return (action for action in self.actions if self.poss_state(action, state))

    def all_actions(self) -> Iterator[Action]:
        yield from self.actions

    def all_poss_actions(self, situation: Situation) -> Iterator[Action]:
        return (action for action in self.actions if self.poss(action, situation))
