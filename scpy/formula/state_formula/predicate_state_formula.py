"""
    TODO: Write docstring for module
"""
from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.formula.state_formula.state_formula import StateFormula
from scpy.literal import Literal
from scpy.predicate import Predicate
from scpy.state import State


@dataclass(frozen=True, order=True)
class PredicateStateFormula(StateFormula):
    """
    TODO: Write docstring for class
    """
    predicate: Predicate = Field(default_factory=Predicate)

    def __str__(self) -> str:
        return str(self.predicate)

    def evaluate_state(self, state: State) -> bool:
        lit = Literal(self.predicate)
        if -lit in state:
            return False
        return lit in state
