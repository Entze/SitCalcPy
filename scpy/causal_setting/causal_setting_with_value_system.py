from typing import Mapping, Optional, Sequence, Tuple

from frozendict import frozendict  # type: ignore
from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.action.action import Action
from scpy.agent.agent import Agent
from scpy.causal_setting.causal_setting import CausalSetting
from scpy.dataclass_config import DataclassConfig
from scpy.function.function import Function
from scpy.preorder import Preorder
from scpy.situation.situation import Situation
from scpy.state.state import State


@dataclass(frozen=True, order=True, config=DataclassConfig)
class CausalSettingWithValueSystem(CausalSetting):
    value_system: Mapping[Agent, Preorder] = Field(default_factory=frozendict)

    def do_state(self, action: Action, state: State) -> State:
        raise NotImplementedError

    def poss_state(self, action: Action, state: State) -> bool:
        raise NotImplementedError

    def valuation_situation(self,
                            action: Action,
                            situation: Situation,
                            agent: Agent,
                            value: Function) -> Optional[bool]:
        return self.valuation_state(action, situation.state, agent, value)

    def valuation_state(self, action: Action, state: State, agent: Agent, value: Function) -> Optional[bool]:
        raise NotImplementedError

    def defeats_state(self,
                      value1: Function, plan1: Sequence[Action],
                      value2: Function, plan2: Sequence[Action],
                      agent: Agent, state: State) -> bool:
        return agent in self.value_system and \
               self.attacks_state(value1, plan1, value2, plan2, agent, state) and \
               not self.value_system[agent].is_strictly_preceded(value1, value2)

    def plan_valuation(self, value: Function, plan: Sequence, agent: Agent, state: State) -> Tuple[bool, bool]:
        positive = False
        negative = False
        state_ = state
        for action in plan:
            if positive and negative:
                break
            res = self.valuation_state(action, state_, agent, value)
            positive = positive or res is True
            negative = negative or res is False
            state_ = self.do_state(action, state_)
        return positive, negative

    def attacks_state(self,
                      value1: Function, plan1: Sequence[Action],
                      value2: Function, plan2: Sequence[Action],
                      agent: Agent, state: State) -> bool:
        positive1, negative1 = self.plan_valuation(value1, plan1, agent, state)
        positive2, negative2 = self.plan_valuation(value2, plan2, agent, state)

        if positive1 and positive2 and plan1 != plan2:
            return True
        if (positive1 or positive2) and (negative1 or negative2) and plan1 == plan2:
            return True
        return False
