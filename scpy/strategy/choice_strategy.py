from typing import Iterator

import more_itertools
from pydantic.dataclasses import dataclass

from scpy.action.action import Action
from scpy.causal_setting.causal_setting import CausalSetting
from scpy.state.state import State
from scpy.strategy.strategy import Strategy


@dataclass
class ChoiceStrategy(Strategy):
    left: Strategy
    right: Strategy

    def all_applicable_actions(self, causal_setting: CausalSetting, state: State) -> Iterator[Action]:
        left_all_applicable_actions = self.left.all_applicable_actions(causal_setting, state)
        right_all_applicable_actions = self.right.all_applicable_actions(causal_setting, state)
        return more_itertools.roundrobin(left_all_applicable_actions, right_all_applicable_actions)
