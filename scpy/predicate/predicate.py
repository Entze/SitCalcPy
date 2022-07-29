"""
    TODO: Write docstring for module
"""

from typing import Sequence, Union

from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.function.function import Function


@dataclass(frozen=True, order=True)
class Predicate:
    """
    TODO: Write docstring for class
    """
    functor: str = Field(default="")
    arguments: Sequence[Union[Function, int]] = Field(default_factory=tuple)

    def __str__(self) -> str:
        if self.arguments:
            return "{}({})".format(self.functor, ','.join(str(argument) for argument in self.arguments))
        else:
            return self.functor
