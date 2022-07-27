"""
    TODO: Write docstring for module
"""
from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.formula.state_formula.state_formula import StateFormula
from scpy.literal import Literal
from scpy.state import State


@dataclass(frozen=True, order=True)
class PredicateStateFormula(StateFormula):
    """
    TODO: Write docstring for class
    """
    literal: Literal = Field(default_factory=Literal)

    def evaluate_state(self, state: State) -> bool:
        if self.literal in state:
            return True
        if -self.literal in state:
            return False
        return not self.literal.sign
