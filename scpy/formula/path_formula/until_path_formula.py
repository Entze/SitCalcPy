from typing import Union, Literal

from pydantic.dataclasses import dataclass

from scpy.formula.path_formula.path_formula import PathFormula
from scpy.path import Path
from scpy.trace import Trace


@dataclass(frozen=True, order=True)
class UntilPathFormula(PathFormula):
    phi: PathFormula
    psi: PathFormula

    def __str__(self) -> str:
        return "{} U {}".format(self.phi, self.psi)

    def evaluate_trace(self, trace: Trace) -> Union[bool, Literal['Inconclusive']]:
        for i in range(len(trace)):
            if self.psi.evaluate(trace.slice(i)) is True:
                return True
            if self.phi.evaluate(trace.slice(i)) is False:
                return False
        return 'Inconclusive'

    def evaluate_path(self, path: Path) -> Union[bool, Literal['Inconclusive']]:
        for i in range(len(path)):
            all_psi_inconclusive = True
            some_phi_false = False
            for trace in path.traces:
                trace_ = trace.slice(i)
                psi_res = self.psi.evaluate(trace_)
                if psi_res is True:
                    return True
                elif psi_res != 'Inconclusive':
                    all_psi_inconclusive = False
                phi_res = self.phi.evaluate(trace_)
                if phi_res == 'Inconclusive':
                    return 'Inconclusive'
                elif phi_res is False:
                    some_phi_false = True
            if all_psi_inconclusive and some_phi_false:
                return 'Inconclusive'
            elif some_phi_false:
                return False
        return 'Inconclusive'
