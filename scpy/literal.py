"""
    TODO: Write docstring for module
"""

from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.predicate import Predicate


@dataclass(frozen=True, order=True)
class Literal:
    """
    TODO: Write docstring for class
    """
    predicate: Predicate = Field(default_factory=Predicate)
    sign: bool = Field(default=True)

    def __neg__(self):
        return Literal(self.predicate, not self.sign)
