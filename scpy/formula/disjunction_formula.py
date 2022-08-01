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
class DisjunctionFormula(PalatFormula):
    left: Formula
    right: Formula

    def __str__(self) -> str:
        return "{} ∨ {}".format(self.left, self.right)


@dataclass(frozen=True, order=True)
class EvaluableDisjunctionFormula(DisjunctionFormula, PathFormula, StateFormula):
    left: EvaluableFormula
    right: EvaluableFormula

    def evaluate(self, e: Union[State, Situation, Path, Trace]) -> Union[bool, Literal['Inconclusive']]:
        left_res = self.left.evaluate(e)
        if left_res == 'Inconclusive' or left_res:
            return left_res
        right_res = self.right.evaluate(e)
        if right_res == 'Inconclusive':
            return right_res
        return left_res or right_res

    def evaluate_state(self, state: State) -> bool:
        left_res = self.left.evaluate_state(state)
        if left_res == 'Inconclusive' or left_res:
            return left_res
        right_res = self.right.evaluate_state(state)
        if right_res == 'Inconclusive':
            return right_res
        return left_res or right_res

    def evaluate_situation(self, situation: Situation) -> bool:
        left_res = self.left.evaluate_situation(situation)
        if left_res == 'Inconclusive' or left_res:
            return left_res
        right_res = self.right.evaluate_situation(situation)
        if right_res == 'Inconclusive':
            return right_res
        return left_res or right_res

    def evaluate_path(self, path: Path) -> Union[bool, Literal['Inconclusive']]:
        left_res = self.left.evaluate_path(path)
        if left_res == 'Inconclusive' or left_res:
            return left_res
        right_res = self.right.evaluate_path(path)
        if right_res == 'Inconclusive':
            return right_res
        return left_res or right_res

    def evaluate_trace(self, trace: Trace) -> Union[bool, Literal['Inconclusive']]:
        left_res = self.left.evaluate_trace(trace)
        if left_res == 'Inconclusive' or left_res:
            return left_res
        right_res = self.right.evaluate_trace(trace)
        if right_res == 'Inconclusive':
            return right_res
        return left_res or right_res
