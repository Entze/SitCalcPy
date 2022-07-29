import math
from random import choice, getrandbits
from typing import FrozenSet, MutableMapping

from frozendict import frozendict
from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.action.action import Action
from scpy.agent.agent import Agent
from scpy.causal_setting.game_causal_setting import GameCausalSetting
from scpy.function.function import Function
from scpy.predicate.predicate import Predicate
from scpy.situation.epistemic_situation import EpistemicSituation
from scpy.state.state import State


@dataclass(frozen=True, order=True)
class SimpleTestEpistemicCausalSetting(GameCausalSetting):
    fluents: FrozenSet[Predicate] = Field(default=frozenset({Predicate('a'), Predicate('b'), Predicate('c')}))
    actions: FrozenSet[Action] = Field(default=frozenset({
        Function('tick', (Function('shake'), GameCausalSetting.noop())),
        Function('tick', (Function('look'), GameCausalSetting.noop())),
        Function('tick', (GameCausalSetting.noop(), Function('shake'))),
        Function('tick', (GameCausalSetting.noop(), Function('look'))),
    }))
    agents: FrozenSet[Agent] = Field(default=frozenset({0, 1}))

    def _legal_move_state(self, agent: Agent, move: Function, state: State) -> bool:
        if sum(1 for literal in state if literal.sign and literal.predicate in self.fluents):
            return move.symbol != 'shake'
        return True

    def extract_move(self, action: Action) -> Function:
        assert action.arguments
        assert isinstance(action.arguments[0], Function)
        move: Function = action.arguments[0]
        if move == GameCausalSetting.noop():
            assert isinstance(action.arguments[1], Function)
            move = action.arguments[1]

        assert move != GameCausalSetting.noop()
        return move

    def do_state(self, action: Action, state: State) -> State:
        move = self.extract_move(action)
        if move.symbol == 'shake':
            coin = bool(getrandbits(1))
            if coin:
                rem = choice(tuple(state))
                state_ = set(state)
                state_.remove(rem)
                return frozenset(state_)
        return state

    def do(self, action: Action, situation: EpistemicSituation) -> EpistemicSituation:
        move = self.extract_move(action)
        state_ = self.do_state(action, situation.state)
        knowledge_relation_: MutableMapping[Agent, MutableMapping[State, float]] = {key: dict(value) for
                                                                                    key, value in
                                                                                    situation.knowledge_relation.items()}
        if move.symbol == 'look':
            agent: Agent = action.arguments.index(move)

            for state in situation.knowledge_relation[agent]:
                knowledge_relation_[agent][state] = float('-inf')
            knowledge_relation_[agent][state_] = 0.0
        elif move.symbol == 'shake':
            for agent in situation.knowledge_relation:
                for state in situation.knowledge_relation[agent]:
                    nr_fluents = sum(1 for literal in state if literal.sign and literal.predicate in self.fluents)
                    if nr_fluents > 0:
                        prob = situation.knowledge_relation[agent][state]
                        for literal in state:
                            reduced_state = set(state)
                            reduced_state.remove(literal)
                            reduced_state = frozenset(reduced_state)
                            knowledge_relation_[agent][reduced_state] = prob + math.log(1 / 2) + math.log(
                                1 / nr_fluents)
                        knowledge_relation_[agent][state] = prob + math.log(1 / 2)
        return EpistemicSituation(state=state_,
                                  previous_situation=situation,
                                  previous_action=action,
                                  knowledge_relation=frozendict(
                                      {key: frozendict(value) for key, value in knowledge_relation_.items()}))
