from typing import Union, Literal

from pydantic.dataclasses import dataclass

from scpy.formula.evaluable_formula import EvaluableFormula
from scpy.formula.formula import Formula
from scpy.formula.palat_formula.palat_formula import PalatFormula
from scpy.formula.path_formula.path_formula import PathFormula
from scpy.formula.state_formula.state_formula import StateFormula
from scpy.path.path import Path
from scpy.situation.situation import Situation
from scpy.state.state import State
from scpy.trace.trace import Trace


@dataclass(frozen=True, order=True)
class NegationFormula(PalatFormula):
    formula: Formula

    def __str__(self) -> str:
        return "¬{}".format(self.formula)


@dataclass(frozen=True, order=True)
class EvaluableNegationFormula(NegationFormula, PathFormula, StateFormula):
    formula: EvaluableFormula

    def evaluate(self, e: Union[State, Situation, Path, Trace]) -> Union[bool, Literal['Inconclusive']]:
        res = self.formula.evaluate(e)
        if res == 'Inconclusive':
            return res
        return not res

    def evaluate_state(self, state: State) -> bool:
        res = self.formula.evaluate_state(state)
        if res == 'Inconclusive':
            return res
        return not res

    def evaluate_situation(self, situation: Situation) -> bool:
        res = self.formula.evaluate_situation(situation)
        if res == 'Inconclusive':
            return res
        return not res

    def evaluate_path(self, path: Path) -> Union[bool, Literal['Inconclusive']]:
        res = self.formula.evaluate_path(path)
        if res == 'Inconclusive':
            return res
        return not res

    def evaluate_trace(self, trace: Trace) -> Union[bool, Literal['Inconclusive']]:
        res = self.formula.evaluate_trace(trace)
        if res == 'Inconclusive':
            return res
        return not res
