from typing import Union, Literal

from pydantic.dataclasses import dataclass

from scpy.formula.formula import Formula
from scpy.formula.path_formula.path_formula import PathFormula
from scpy.formula.state_formula.state_formula import StateFormula
from scpy.path import Path
from scpy.situation import Situation
from scpy.state import State
from scpy.trace import Trace


@dataclass(frozen=True, order=True)
class TrueFormula(PathFormula, StateFormula):

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
class FalseFormula(PathFormula, StateFormula):

    def __str__(self) -> str:
        return "⊥"

    def evaluate(self, e: Union[State, Situation, Path, Trace]) -> bool:
        return False

    def evaluate_state(self, state: State) -> bool:
        return False

    def evaluate_situation(self, situation: Situation) -> bool:
        return False

    def evaluate_path(self, path: Path) -> Union[bool, Literal['Inconclusive']]:
        return False

    def evaluate_trace(self, trace: Trace) -> Union[bool, Literal['Inconclusive']]:
        return False


@dataclass(frozen=True, order=True)
class NegationFormula(PathFormula, StateFormula):
    formula: Union[Formula, PathFormula, StateFormula]

    def __str__(self) -> str:
        return "¬{}".format(self.formula)

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


@dataclass(frozen=True, order=True)
class ConjunctionFormula(PathFormula, StateFormula):
    left: Union[Formula, PathFormula, StateFormula]
    right: Union[Formula, PathFormula, StateFormula]

    def __str__(self) -> str:
        return "{} ∧ {}".format(self.left, self.right)

    def evaluate(self, e: Union[State, Situation, Path, Trace])-> Union[bool, Literal['Inconclusive']]:
        left_res = self.left.evaluate(e)
        if left_res == 'Inconclusive' or not left_res:
            return left_res
        right_res = self.right.evaluate(e)
        if right_res == 'Inconclusive':
            return right_res
        return left_res and right_res

    def evaluate_state(self, state: State) -> bool:
        left_res = self.left.evaluate_state(state)
        if left_res == 'Inconclusive' or not left_res:
            return left_res
        right_res = self.right.evaluate_state(state)
        if right_res == 'Inconclusive':
            return right_res
        return left_res and right_res

    def evaluate_situation(self, situation: Situation) -> bool:
        left_res = self.left.evaluate_situation(situation)
        if left_res == 'Inconclusive' or not left_res:
            return left_res
        right_res = self.right.evaluate_situation(situation)
        if right_res == 'Inconclusive':
            return right_res
        return left_res and right_res

    def evaluate_path(self, path: Path) -> Union[bool, Literal['Inconclusive']]:
        left_res = self.left.evaluate_path(path)
        if left_res == 'Inconclusive' or not left_res:
            return left_res
        right_res = self.right.evaluate_path(path)
        if right_res == 'Inconclusive':
            return right_res
        return left_res and right_res

    def evaluate_trace(self, trace: Trace) -> Union[bool, Literal['Inconclusive']]:
        left_res = self.left.evaluate_trace(trace)
        if left_res == 'Inconclusive' or not left_res:
            return left_res
        right_res = self.right.evaluate_trace(trace)
        if right_res == 'Inconclusive':
            return right_res
        return left_res and right_res

@dataclass(frozen=True, order=True)
class DisjunctionFormula(PathFormula, StateFormula):
    left: Union[Formula, PathFormula, StateFormula]
    right: Union[Formula, PathFormula, StateFormula]

    def __str__(self) -> str:
        return "{} ∨ {}".format(self.left, self.right)

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
