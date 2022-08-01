from typing import Union, Literal

from pydantic.dataclasses import dataclass

from scpy.formula.evaluable_formula import EvaluableFormula
from scpy.path.path import Path
from scpy.situation.situation import Situation
from scpy.trace.trace import Trace


@dataclass(frozen=True, order=True)
class StateFormula(EvaluableFormula):

    def evaluate_situation(self, situation: Situation) -> bool:
        return self.evaluate_state(situation.state)

    def evaluate_trace(self, trace: Trace) -> Union[bool, Literal['Inconclusive']]:
        return self.evaluate_state(trace.first_state)

    def evaluate_path(self, path: Path) -> Union[bool, Literal['Inconclusive']]:
        return self.evaluate_situation(path.initial_situation)
