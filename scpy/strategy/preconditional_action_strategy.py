from typing import Iterator

from pydantic.dataclasses import dataclass

from scpy.action.action import Action
from scpy.causal_setting.causal_setting import CausalSetting
from scpy.formula.evaluable_formula import EvaluableFormula
from scpy.state.state import State
from scpy.strategy.strategy import Strategy


@dataclass
class PreconditionalActionStrategy(Strategy):
    condition: EvaluableFormula
    action: Action

    def all_applicable_actions(self, causal_setting: CausalSetting, state: State) -> Iterator[Action]:
        if not causal_setting.poss_state(self.action, state):
            yield from ()
        elif self.condition.evaluate(state):
            yield self.action
