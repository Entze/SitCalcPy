from numbers import Number
from typing import Mapping

from frozendict import frozendict  # type: ignore
from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.function.function import Function
from scpy.situation.situation import Situation


@dataclass(frozen=True, order=True)
class SituationWithResources(Situation):
    resources: Mapping[Function, float] = Field(default_factory=frozendict)
