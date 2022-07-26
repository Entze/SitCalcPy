from pydantic.dataclasses import dataclass

from scpy.formula.palat_formula.palat_formula import PalatFormula
from scpy.primitives import Predicate


@dataclass(frozen=True, order=True)
class PredicatePalatFormula(PalatFormula):
    predicate: Predicate
