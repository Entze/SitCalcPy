"""
    TODO: Write docstring for module
"""

from typing import Sequence, TypeAlias, Union

from pydantic import Field
from pydantic.dataclasses import dataclass

_Function: TypeAlias = 'Function'


@dataclass(frozen=True, order=True)
class Function:
    """
    TODO: Write docstring for class
    """
    symbol: str = Field(default="")
    arguments: Sequence[Union[_Function, int]] = Field(default_factory=tuple)
