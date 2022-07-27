from typing import Literal, Union

from pydantic.dataclasses import dataclass

from scpy.formula.path_formula.path_formula import PathFormula
from scpy.formula.state_formula.state_formula import StateFormula
from scpy.path import Path
from scpy.trace import Trace


@dataclass(frozen=True, order=True)
class StatePathFormula(PathFormula):
    state_formula: StateFormula

    def evaluate_trace(self, trace: Trace) -> Union[bool, Literal['Inconclusive']]:
        return self.state_formula.evaluate(trace.first_state)

    def evaluate_path(self, path: Path) -> Union[bool, Literal['Inconclusive']]:
        return self.state_formula.evaluate(path.initial_situation)
