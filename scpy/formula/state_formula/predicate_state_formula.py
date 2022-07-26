"""
    TODO: Write docstring for module
"""
from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.formula.state_formula.state_formula import StateFormula
from scpy.literal import Literal


@dataclass
class PredicateStateFormula(StateFormula):
    """
    TODO: Write docstring for class
    """
    literal: Literal = Field(default_factory=Literal)
