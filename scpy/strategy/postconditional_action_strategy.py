from typing import Iterator

from pydantic.dataclasses import dataclass

from scpy.action.action import Action
from scpy.causal_setting.causal_setting import CausalSetting
from scpy.formula.formula import Formula
from scpy.state.state import State
from scpy.strategy.strategy import Strategy


@dataclass
class PostconditionalActionStrategy(Strategy):
    action: Action
    condition: Formula

    def all_applicable_actions(self, causal_setting: CausalSetting, state: State) -> Iterator[Action]:
        if not causal_setting.poss_state(self.action, state):
            yield from ()
        else:
            state_ = causal_setting.do_state(self.action, state)
            if self.condition.evaluate(state_):
                yield self.action
