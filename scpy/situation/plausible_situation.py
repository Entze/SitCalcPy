from typing import Mapping, Sequence, Set

from frozendict import frozendict  # type: ignore
from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.agent.agent import Agent
from scpy.situation.situation import Situation
from scpy.trace.trace import Trace


@dataclass(frozen=True, order=True)
class PlausibleSituation(Situation):
    believe: Mapping[Agent, Sequence[Set[Trace]]] = Field(default_factory=frozendict)
