from typing import Sequence

from scpy.formula.palat_formula.palat_formula import PalatFormula
from scpy.primitives import Assignment


class PublicAssignmentPalatFormula(PalatFormula):
    assignment: Sequence[Assignment]
    holds: PalatFormula
