from typing import Iterator

from pydantic.dataclasses import dataclass

from scpy.action.action import Action
from scpy.causal_setting.causal_setting import CausalSetting
from scpy.formula.evaluable_formula import EvaluableFormula
from scpy.state.state import State
from scpy.strategy.strategy import Strategy


@dataclass
class PermutationPostconditionalActionStrategy(Strategy):
    condition: EvaluableFormula

    def all_applicable_actions(self, causal_setting: CausalSetting, state: State) -> Iterator[Action]:
        for action in causal_setting.all_poss_actions_state(state):
            state_ = causal_setting.do_state(action, state)
            if self.condition.evaluate(state_):
                yield action
