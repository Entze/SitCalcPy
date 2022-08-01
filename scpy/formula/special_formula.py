from typing import Union

from pydantic.dataclasses import dataclass

from scpy.formula.palat_formula.palat_formula import PalatFormula
from scpy.formula.path_formula.path_formula import PathFormula
from scpy.formula.state_formula.state_formula import StateFormula
from scpy.path.path import Path
from scpy.situation.situation import Situation
from scpy.state.state import State
from scpy.trace.trace import Trace


@dataclass(frozen=True, order=True)
class TrueFormula(PathFormula, StateFormula, PalatFormula):

    def __str__(self) -> str:
        return "⊤"

    def evaluate(self, e: Union[State, Situation, Path, Trace]) -> bool:
        return True

    def evaluate_state(self, state: State) -> bool:
        return True

    def evaluate_situation(self, situation: Situation) -> bool:
        return True

    def evaluate_path(self, path: Path) -> bool:
        return True

    def evaluate_trace(self, trace: Trace) -> bool:
        return True


@dataclass(frozen=True, order=True)
class FalseFormula(PathFormula, StateFormula, PalatFormula):

    def __str__(self) -> str:
        return "⊥"

    def evaluate(self, e: Union[State, Situation, Path, Trace]) -> bool:
        return False

    def evaluate_state(self, state: State) -> bool:
        return False

    def evaluate_situation(self, situation: Situation) -> bool:
        return False

    def evaluate_path(self, path: Path) -> bool:
        return False

    def evaluate_trace(self, trace: Trace) -> bool:
        return False




