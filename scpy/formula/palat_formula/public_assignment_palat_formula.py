from typing import Sequence

from scpy.assignment.assignment import Assignment
from scpy.formula.palat_formula.palat_formula import PalatFormula


class PublicAssignmentPalatFormula(PalatFormula):
    assignment: Sequence[Assignment]
    holds: PalatFormula
