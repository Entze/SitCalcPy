from typing import Iterator

from pydantic.dataclasses import dataclass

from scpy.action import Action
from scpy.causal_setting.causal_setting import CausalSetting
from scpy.state import State
from scpy.strategy.strategy import Strategy


@dataclass
class PermutationStrategy(Strategy):

    def all_applicable_actions(self, causal_setting: CausalSetting, state: State) -> Iterator[Action]:
        return causal_setting.all_poss_actions_state(state)
