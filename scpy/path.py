from typing import Set

from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.causal_setting.causal_setting import CausalSetting
from scpy.situation import Situation
from scpy.trace import Trace


@dataclass
class Path:
    initial_situation: Situation
    traces: Set[Trace] = Field(default_factory=set)
    len: int = Field(default=0)

    def __len__(self):
        return self.len

    def expand(self, causal_setting: CausalSetting):
        if not self.traces:
            initial_trace = Trace((self.initial_situation.state,))
            self.traces.add(initial_trace)
        else:
            traces = set()
            for trace in self.traces:
                state = trace.last_state
                for action in causal_setting.all_poss_actions_state(state):
                    trace_ = trace.extend(causal_setting, action)
                    traces.add(trace_)
            self.traces = traces
        self.len += 1
