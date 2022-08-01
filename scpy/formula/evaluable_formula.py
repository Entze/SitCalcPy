import typing
from typing import Union, Literal

from pydantic.dataclasses import dataclass

from scpy.formula.formula import Formula
from scpy.path.path import Path
from scpy.situation.situation import Situation
from scpy.state.state import State
from scpy.trace.trace import Trace


@dataclass(frozen=True, order=True)
class EvaluableFormula(Formula):

    def evaluate(self, e: Union[State, Situation, Path, Trace]) -> Union[bool, Literal['Inconclusive']]:
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

    def evaluate_path(self, path: Path) -> Union[bool, Literal['Inconclusive']]:
        raise NotImplementedError

    def evaluate_trace(self, trace: Trace) -> Union[bool, Literal['Inconclusive']]:
        raise NotImplementedError
