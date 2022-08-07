from typing import TypeAlias, Optional, Sequence, Union

from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.formula.formula import Formula

_Function: TypeAlias = 'Function'
_Predicate: TypeAlias = 'Predicate'
_Assignment: TypeAlias = 'Assignment'
_Literal: TypeAlias = 'Literal'


@dataclass(frozen=True, order=True)
class Assignment:
    predicate: _Predicate
    formula: Formula


@dataclass(frozen=True, order=True)
class Function:
    symbol: Optional[str] = Field(default=None)
    arguments: Sequence[Union[_Function, int, Formula, _Assignment, _Literal]] = Field(default_factory=tuple)

    def __str__(self) -> str:
        if self.arguments:
            return "{}({})".format(self.symbol, ','.join(str(argument) for argument in self.arguments))
        elif self.symbol is None:
            return "()"
        else:
            assert isinstance(self.symbol, str)
            return self.symbol


@dataclass(frozen=True, order=True)
class Predicate:
    functor: str = Field(default="")
    arguments: Sequence[Union[Function, int, _Literal, Assignment, Formula]] = Field(default_factory=tuple)

    def __str__(self) -> str:
        if self.arguments:
            return "{}({})".format(self.functor, ','.join(str(argument) for argument in self.arguments))
        else:
            return self.functor


@dataclass(frozen=True, order=True)
class Literal:
    predicate: Predicate = Field(default_factory=Predicate)
    sign: bool = Field(default=True)

    def __neg__(self) -> _Literal:
        return Literal(self.predicate, not self.sign)

    def __str__(self) -> str:
        if self.sign:
            return str(self.predicate)
        else:
            return "¬{}".format(self.predicate)


Function.__pydantic_model__.update_forward_refs()  # type: ignore
Predicate.__pydantic_model__.update_forward_refs()  # type: ignore
Function.__pydantic_model__.update_forward_refs()  # type: ignore
Assignment.__pydantic_model__.update_forward_refs()  # type: ignore
