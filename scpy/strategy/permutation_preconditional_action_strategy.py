from typing import Iterator

from pydantic.dataclasses import dataclass

from scpy.action.action import Action
from scpy.causal_setting.causal_setting import CausalSetting
from scpy.formula.formula import Formula
from scpy.state.state import State
from scpy.strategy.strategy import Strategy


@dataclass
class PermutationPreconditionalActionStrategy(Strategy):
    condition: Formula

    def all_applicable_actions(self, causal_setting: CausalSetting, state: State) -> Iterator[Action]:
        if self.condition.evaluate(state):
            yield from causal_setting.all_poss_actions_state(state)
