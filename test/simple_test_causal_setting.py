from typing import FrozenSet

from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.action.action import Action
from scpy.agent.agent import Agent
from scpy.causal_setting.simple_causal_setting import SimpleCausalSetting
from scpy.function.function import Function
from scpy.predicate.predicate import Predicate


@dataclass(frozen=True, order=True)
class SimpleTestCausalSetting(SimpleCausalSetting):
    fluents: FrozenSet[Predicate] = Field(default=frozenset({Predicate('a'), Predicate('b'), Predicate('c')}))
    actions: FrozenSet[Action] = Field(default=frozenset({
        Function('add', (Function('a'),)),
        Function('add', (Function('b'),)),
        Function('add', (Function('c'),)),
        Function('remove', (Function('a'),)),
        Function('remove', (Function('b'),)),
        Function('remove', (Function('c'),)),
    }))
    # objects: Mapping[str, Function] = Field(default_factory=frozendict)
    agents: FrozenSet[Agent] = Field(default_factory=frozenset)
