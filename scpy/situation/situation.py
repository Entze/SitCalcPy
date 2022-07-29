from typing import Optional, TypeAlias

from frozendict import frozendict  # type: ignore
from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.action.action import Action
from scpy.state.state import State

_Situation: TypeAlias = 'Situation'


@dataclass(frozen=True, order=True)
class Situation:
    state: State = Field(default_factory=frozenset)
    previous_action: Optional[Action] = Field(default=None)
    previous_situation: Optional[_Situation] = Field(default=None, repr=False)

    def __str__(self) -> str:
        if self.previous_action is not None:
            return "{}->{}{}{}".format(self.previous_action, '{', ','.join(str(literal) for literal in self.state), '}')
        else:
            return "{}{}{}".format('{', ','.join(str(literal) for literal in self.state), '}')
