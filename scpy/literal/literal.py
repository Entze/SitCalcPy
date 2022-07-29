"""
    TODO: Write docstring for module
"""
from typing import TypeAlias

from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.predicate.predicate import Predicate

_Literal: TypeAlias = 'Literal'


@dataclass(frozen=True, order=True)
class Literal:
    """
    TODO: Write docstring for class
    """
    predicate: Predicate = Field(default_factory=Predicate)
    sign: bool = Field(default=True)

    def __neg__(self) -> _Literal:
        return Literal(self.predicate, not self.sign)

    def __str__(self) -> str:
        if self.sign:
            return str(self.predicate)
        else:
            return "¬{}".format(self.predicate)
