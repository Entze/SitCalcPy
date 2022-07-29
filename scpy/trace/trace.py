from copy import deepcopy
from typing import Sequence, TypeAlias, Optional, List

from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.action.action import Action
from scpy.causal_setting.causal_setting import CausalSetting
from scpy.state.state import State

_Trace: TypeAlias = 'Trace'


@dataclass(frozen=True, order=True)
class Trace:
    states: Sequence[State] = Field(default_factory=tuple)
    actions: Sequence[Action] = Field(default_factory=tuple)

    def invariant(self) -> None:
        if len(self.states) - 1 == len(self.actions):
            return

        raise RuntimeError("states and actions mismatched")

    def __len__(self) -> int:
        self.invariant()
        return len(self.states)

    def __str__(self) -> str:
        self.invariant()
        s = "{}{}{}".format('{', ','.join(str(literal) for literal in self.first_state), '}')
        for i, a in enumerate(self.actions):
            s += " {} ".format(a)
            s += "{}{}{}".format('{', ','.join(str(literal) for literal in self.states[i + 1]), '}')
        return s

    @property
    def first_state(self) -> State:
        self.invariant()
        return self.states[0]

    @property
    def last_state(self) -> State:
        self.invariant()
        return self.states[-1]

    def extend(self, causal_setting: CausalSetting, action: Action) -> _Trace:
        self.invariant()
        state_ = causal_setting.do_state(action, self.last_state)
        states_ = (*self.states, state_)
        actions_ = (*self.actions, action)
        return Trace(states_, actions_)

    def slice(self, from_index: Optional[int] = None, to_index: Optional[int] = None) -> _Trace:
        self.invariant()
        actions__: List[Optional[Action]] = [None]
        actions__.extend(self.actions)
        if from_index is None and to_index is None:
            return deepcopy(self)
        else:
            states_ = self.states[from_index:to_index]
            from_index_ = from_index + 1 if from_index is not None else None
            actions_: Sequence[Action] = tuple(
                action for action in actions__[from_index_:to_index] if action is not None)
            return Trace(states_, actions_)
