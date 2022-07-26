"""
    TODO: Write docstring for module
"""

from typing import Sequence

from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.function import Function


@dataclass(frozen=True, order=True)
class Predicate:
    """
    TODO: Write docstring for class
    """
    functor: str = Field(default="")
    arguments: Sequence[Function | int] = Field(default_factory=tuple)
