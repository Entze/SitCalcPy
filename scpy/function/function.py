from typing import Sequence, TypeAlias, Union, Optional

from pydantic import Field
from pydantic.dataclasses import dataclass

_Function: TypeAlias = 'Function'
# TODO: is this the best solution, to avoid circular import?
_Formula: TypeAlias = 'Formula'  # type: ignore
_Assignment: TypeAlias = 'Assignment'  # type: ignore


@dataclass(frozen=True, order=True)
class Function:
    symbol: Optional[str] = Field(default=None)
    arguments: Sequence[Union[_Function, int, _Formula, _Assignment]] = Field(default_factory=tuple)

    def __str__(self) -> str:
        if self.arguments:
            return "{}({})".format(self.symbol, ','.join(str(argument) for argument in self.arguments))
        elif self.symbol is None:
            return "()"
        else:
            assert isinstance(self.symbol, str)
            return self.symbol
