from typing import Optional, FrozenSet, Mapping

from frozendict import frozendict
from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.action.action import Action
from scpy.agent.agent import Agent
from scpy.causal_setting.causal_setting_with_value_system import CausalSettingWithValueSystem
from scpy.dataclass_config import DataclassConfig
from scpy.primitives import Function, Literal, Predicate
from scpy.preorder import MutablePreorder, Preorder
from scpy.state.state import State

mut_simple_value_system = MutablePreorder()

privacy = Function('privacy')
safety = Function('safety')
good_condition = Function('good_condition')

mut_simple_value_system.precedes(privacy, good_condition)
mut_simple_value_system.precedes(privacy, safety)
mut_simple_value_system.precedes(good_condition, safety)

simple_value_system = Preorder(mut_simple_value_system)

at_0 = Predicate('at', (0,))
lit_at_0 = Literal(at_0)
at_1 = Predicate('at', (1,))
lit_at_1 = Literal(at_1)
at_2 = Predicate('at', (2,))
lit_at_2 = Literal(at_2)
at_3 = Predicate('at', (3,))
lit_at_3 = Literal(at_3)
at_4 = Predicate('at', (4,))
lit_at_4 = Literal(at_4)

alpha_1 = Function('α', (1,))
alpha_2 = Function('α', (2,))
alpha_3 = Function('α', (3,))
alpha_4 = Function('α', (4,))
alpha_5 = Function('α', (5,))
alpha_6 = Function('α', (6,))


@dataclass(frozen=True, order=True, config=DataclassConfig)
class SimpleTestCausalSettingWithValueSystem(CausalSettingWithValueSystem):
    fluents: FrozenSet[Predicate] = Field(default=frozenset({at_0, at_1, at_2, at_3, at_4}))
    actions: FrozenSet[Action] = Field(default=frozenset({alpha_1, alpha_2, alpha_3, alpha_4, alpha_5, alpha_6}))
    agents: FrozenSet[Agent] = Field(default=frozenset({0}))
    value_system: Mapping[Agent, Preorder] = Field(default=frozendict({0: simple_value_system}))

    def do_state(self, action: Action, state: State) -> State:
        if lit_at_0 in state:
            if action == alpha_1:
                return frozenset({lit_at_1})
            if action == alpha_2:
                return frozenset({lit_at_2})
            raise ValueError(f'Unknown action {action}')
        if lit_at_1 in state:
            if action == alpha_6:
                return frozenset({lit_at_4})
            raise ValueError(f'Unknown action {action}')
        if lit_at_2 in state:
            if action == alpha_3:
                return frozenset({lit_at_4})
            if action == alpha_4:
                return frozenset({lit_at_3})
            raise ValueError(f'Unknown action {action}')
        if lit_at_3 in state:
            if action == alpha_5:
                return frozenset({lit_at_4})
            raise ValueError(f'Unknown action {action}')
        if lit_at_4 in state:
            return state
        raise ValueError(f'Unknown state {state}')

    def poss_state(self, action: Action, state: State) -> bool:
        if lit_at_0 in state:
            return action in (alpha_1, alpha_2)
        if lit_at_1 in state:
            return action == alpha_6
        if lit_at_2 in state:
            return action in (alpha_3, alpha_4)
        if lit_at_3 in state:
            return action == alpha_5
        if lit_at_4 in state:
            return True
        return False

    def valuation_state(self, action: Action, state: State, agent: Agent, value: Function) -> Optional[bool]:
        if action == alpha_1 and lit_at_0 in state and value == privacy:
            return False
        if action == alpha_2 and lit_at_0 in state and value == privacy:
            return True
        if action == alpha_3 and lit_at_2 in state and value == safety:
            return False
        if action == alpha_4 and lit_at_2 in state and value == safety:
            return True
        if action == alpha_5 and lit_at_3 in state and value == good_condition:
            return False
        return None
