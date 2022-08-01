from pydantic.dataclasses import dataclass

from scpy.action.action import Action
from scpy.causal_setting.causal_setting import CausalSetting
from scpy.function.function import Function
from scpy.literal.literal import Literal
from scpy.predicate.predicate import Predicate
from scpy.state.state import State


@dataclass(frozen=True, order=True)
class SimpleCausalSetting(CausalSetting):

    def do_state(self, action: Action, state: State) -> State:
        elem_raw = action.arguments[0]
        assert isinstance(elem_raw, Function)
        assert elem_raw.symbol is not None
        elem = Predicate(elem_raw.symbol, elem_raw.arguments)
        elem_lit = Literal(elem)
        if action.symbol == 'add':
            state_ = set(state)
            if -elem_lit in state_:
                state_.remove(-elem_lit)
            state_.add(elem_lit)
        elif action.symbol == 'remove':
            state_ = set(state)
            if elem_lit in state_:
                state_.remove(elem_lit)
            state_.add(-elem_lit)
        else:
            return state
        return frozenset(state_)

    def poss_state(self, action: Action, state: State) -> bool:
        if action.symbol in ('add', 'remove'):
            elem_raw = action.arguments[0]
            if not isinstance(elem_raw, Function):
                return False
            if elem_raw.symbol is None:
                return False
            elem = Predicate(elem_raw.symbol, elem_raw.arguments)
            elem_lit = Literal(elem)
            if action.symbol == 'add':
                return elem_lit not in state
            elif action.symbol == 'remove':
                return elem_lit in state
        return True
