"""
    TODO: Write docstring for module
"""
import typing
from typing import Union

from pydantic import validator
from pydantic.dataclasses import dataclass

from scpy.path import Path
from scpy.situation import Situation
from scpy.state import State
from scpy.trace import Trace


@dataclass(frozen=True, order=True)
class Formula:
    """
    TODO: Write docstring for class
    """

    def evaluate(self, e: Union[State, Situation, Path, Trace]) -> bool:
        if isinstance(e, frozenset):
            return self.evaluate_state(e)
        elif isinstance(e, Situation):
            return self.evaluate_situation(e)
        elif isinstance(e, Path):
            return self.evaluate_path(e)
        elif isinstance(e, Trace):
            return self.evaluate_trace(e)
        else:
            typing.assert_never(e)

    def evaluate_state(self, state: State) -> bool:
        raise NotImplementedError

    def evaluate_situation(self, situation: Situation) -> bool:
        raise NotImplementedError

    def evaluate_path(self, path: Path) -> bool:
        raise NotImplementedError

    def evaluate_trace(self, trace: Trace) -> bool:
        raise NotImplementedError


@dataclass(frozen=True, order=True)
class TrueFormula(Formula):

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
class FalseFormula(Formula):

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


@dataclass(frozen=True, order=True)
class NegationFormula(Formula):
    formula: Formula

    def evaluate(self, e: Union[State, Situation, Path, Trace]) -> bool:
        return not self.formula.evaluate(e)

    def evaluate_state(self, state: State) -> bool:
        return not self.formula.evaluate_state(state)

    def evaluate_situation(self, situation: Situation) -> bool:
        return not self.formula.evaluate_situation(situation)

    def evaluate_path(self, path: Path) -> bool:
        return not self.formula.evaluate_path(path)

    def evaluate_trace(self, trace: Trace) -> bool:
        return not self.formula.evaluate_trace(trace)



@dataclass(frozen=True, order=True)
class Conjunction(Formula):
    left: Formula
    right: Formula

    def evaluate(self, e: Union[State, Situation, Path, Trace]) -> bool:
        return self.left.evaluate(e) and self.right.evaluate(e)

    def evaluate_state(self, state: State) -> bool:
        return self.left.evaluate_state(state) and self.right.evaluate_state(state)

    def evaluate_situation(self, situation: Situation) -> bool:
        return self.left.evaluate_situation(situation) and self.right.evaluate_situation(situation)

    def evaluate_path(self, path: Path) -> bool:
        return self.left.evaluate_path(path) and self.right.evaluate_path(path)

    def evaluate_trace(self, trace: Trace) -> bool:
        return self.left.evaluate_trace(trace) and self.right.evaluate_trace(trace)
