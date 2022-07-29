from typing import Mapping

from frozendict import frozendict  # type: ignore
from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.agent.agent import Agent
from scpy.situation.situation import Situation
from scpy.state.state import State


@dataclass(frozen=True, order=True)
class EpistemicSituation(Situation):
    knowledge_relation: Mapping[Agent, Mapping[State, float]] = Field(default_factory=frozendict)
