import random
from typing import FrozenSet, Mapping

from frozendict import frozendict
from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.action.action import Action
from scpy.agent.agent import Agent
from scpy.causal_setting.plausible_causal_setting import PlausibleCausalSetting
from scpy.function.function import Function
from scpy.literal.literal import Literal
from scpy.predicate.predicate import Predicate
from scpy.situation.plausible_situation import PlausibleSituation
from scpy.state.state import State

heads: Predicate = Predicate('heads')
heads_lit: Literal = Literal(heads)
flip: Function = Function('flip')
flip_heads: Function = Function('flip', (Function('heads'),))
flip_tails: Function = Function('flip', (Function('tails'),))
noop: Function = Function('noop')
sense_heads: Function = Function('sense', (Function('heads'),))


@dataclass(frozen=True, order=True)
class CoinflipTestPlausibleCausalSetting(PlausibleCausalSetting):
    fluents: FrozenSet[Predicate] = Field(default=frozenset({heads}))
    actions: Mapping[Action, Mapping[Action, int]] = Field(default=frozendict({
        flip: frozendict({flip_heads: 0,
                          flip_tails: 0,
                          noop: 1}),
    }))
    sensing_actions: FrozenSet[Action] = Field(default=frozenset({sense_heads}))
    agents: FrozenSet[Agent] = Field(default=frozenset({0}))

    def do(self, action: Action, situation: PlausibleSituation) -> PlausibleSituation:
        actual_action = action
        if action == flip:
            h = bool(random.getrandbits(1))
            if h:
                actual_action = flip_heads
            else:
                actual_action = flip_tails
        state_ = self.do_state(actual_action, situation.state)
        raise NotImplementedError

    def do_state(self, action: Action, state: State) -> State:
        state_ = set()
        if action == flip_heads:
            state_.add(heads_lit)
        elif action == flip_tails:
            state_.add(-heads_lit)
        elif action == flip:
            h = bool(random.getrandbits(1))
            if h:
                state_.add(heads_lit)
            else:
                state_.add(-heads_lit)
        else:
            return state

    def poss(self, action: Action, situation: PlausibleSituation) -> bool:
        return action in self.actions.keys()

    def poss_state(self, action: Action, state: State) -> bool:
        return action in self.actions.keys()
