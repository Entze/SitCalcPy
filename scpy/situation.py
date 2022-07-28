"""
    TODO: Write docstring for module
"""
from typing import Optional, TypeAlias, Mapping, FrozenSet

from frozendict import frozendict  # type: ignore
from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.action import Action
from scpy.agent import Agent
from scpy.state import State

_Situation: TypeAlias = 'Situation'


@dataclass(frozen=True, order=True)
class Situation:
    """
    TODO: Write docstring for class
    """
    state: State = Field(default_factory=frozenset)
    previous_action: Optional[Action] = Field(default=None)
    previous_situation: Optional[_Situation] = Field(default=None, repr=False)
    knowledge_relation: Mapping[Agent, FrozenSet[_Situation]] = Field(default_factory=frozendict)

    def __str__(self) -> str:
        if self.previous_action is not None:
            return "{}->{}{}{}".format(self.previous_action, '{', ','.join(str(literal) for literal in self.state), '}')
        else:
            return "{}{}{}".format('{', ','.join(str(literal) for literal in self.state), '}')
