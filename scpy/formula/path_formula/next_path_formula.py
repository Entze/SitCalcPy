from typing import Union, Literal

from pydantic.dataclasses import dataclass

from scpy.formula.path_formula.path_formula import PathFormula
from scpy.path import Path
from scpy.trace import Trace


@dataclass(frozen=True, order=True)
class NextPathFormula(PathFormula):
    phi: PathFormula

    def __str__(self) -> str:
        return "X({})".format(self.phi)

    def evaluate_trace(self, trace: Trace) -> Union[bool, Literal['Inconclusive']]:
        if len(trace) <= 1:
            return 'Inconclusive'
        return self.phi.evaluate(trace.slice(1))

    def evaluate_path(self, path: Path) -> Union[bool, Literal['Inconclusive']]:
        if len(path) <= 1:
            return 'Inconclusive'
        return any(self.phi.evaluate(trace.slice(1)) for trace in path.traces)
