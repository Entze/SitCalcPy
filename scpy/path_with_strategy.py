from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.causal_setting.causal_setting import CausalSetting
from scpy.path import Path
from scpy.strategy.choice_strategy import ChoiceStrategy
from scpy.strategy.strategy import Strategy
from scpy.trace import Trace


@dataclass
class PathWithStrategy(Path):
    strategy: Strategy = Field(default_factory=ChoiceStrategy)

    def expand(self, causal_setting: CausalSetting):
        if not self.traces:
            initial_trace = Trace((self.initial_situation.state,))
            self.traces.add(initial_trace)
        else:
            traces = set()
            for trace in self.traces:
                state = trace.last_state
                applicable_actions = self.strategy.all_applicable_actions(causal_setting, state)
                for action in applicable_actions:
                    trace_ = trace.extend(causal_setting, action)
                    traces.add(trace_)
            self.traces = traces
        self.len += 1
