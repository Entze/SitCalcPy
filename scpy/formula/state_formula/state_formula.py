"""
    TODO: Write docstring for module
"""
from pydantic.dataclasses import dataclass

from scpy.formula.formula import Formula
from scpy.path import Path
from scpy.situation import Situation
from scpy.trace import Trace


@dataclass(frozen=True, order=True)
class StateFormula(Formula):

    def evaluate_situation(self, situation: Situation):
        return self.evaluate_state(situation.state)

    def evaluate_trace(self, trace: Trace) -> bool:
        return self.evaluate_state(trace.first_state)

    def evaluate_path(self, path: Path) -> bool:
        return self.evaluate_situation(path.initial_situation)
