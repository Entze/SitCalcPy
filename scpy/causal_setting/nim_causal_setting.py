from typing import FrozenSet, Optional

from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.action.action import Action
from scpy.agent.agent import Agent
from scpy.causal_setting.game_causal_setting import GameCausalSetting
from scpy.primitives import Function, Literal, Predicate
from scpy.state.state import State


@dataclass(frozen=True, order=True)
class NimCausalSetting(GameCausalSetting):
    fluents: FrozenSet[Predicate] = Field(default=frozenset((
        Predicate('stones', (0,)), Predicate('stones', (1,)), Predicate('stones', (2,)),
        Predicate('stones', (3,)), Predicate('stones', (4,)), Predicate('stones', (5,)),
        Predicate('stones', (6,)), Predicate('stones', (7,)),
        Predicate('control', (0,)), Predicate('control', (1,)),
    )))
    actions: FrozenSet[Action] = Field(default=frozenset((
        Function('tick', (Function('take', (1,)), GameCausalSetting.noop())),
        Function('tick', (Function('take', (2,)), GameCausalSetting.noop())),
        Function('tick', (Function('take', (3,)), GameCausalSetting.noop())),
        Function('tick', (GameCausalSetting.noop(), Function('take', (1,)))),
        Function('tick', (GameCausalSetting.noop(), Function('take', (2,)))),
        Function('tick', (GameCausalSetting.noop(), Function('take', (3,)))),
    )))
    agents: FrozenSet[Agent] = Field(default=frozenset((0, 1)))

    def _legal_move_state(self, agent: Agent, move: Function, state: State) -> bool:
        in_control = False
        valid_move = False
        for literal in state:
            if not literal.sign and literal.predicate.functor == 'control' and literal.predicate.arguments[0] == agent:
                return False
            if literal.sign and literal.predicate.functor == 'control' and literal.predicate.arguments[0] == agent:
                in_control = True
            if literal.sign and move.symbol == 'take' and literal.predicate.functor == 'stones':
                assert isinstance(literal.predicate.arguments[0], int)
                stones: int = literal.predicate.arguments[0]
                assert isinstance(move.arguments[0], int)
                take: int = move.arguments[0]
                valid_move = 1 <= take <= 3 and take <= stones
        if move == GameCausalSetting.noop():
            return not in_control
        return in_control and valid_move

    def do_state(self, action: Action, state: State) -> State:
        state_ = set(state)
        take = sum(argument.arguments[0] for argument in action.arguments if
                   isinstance(argument, Action) and
                   argument != GameCausalSetting.noop() and argument.arguments and isinstance(argument.arguments[0],
                                                                                              int))
        assert isinstance(take, int)
        current_player: Optional[Agent] = None
        for literal in state:
            if literal.sign and literal.predicate.functor == 'control':
                state_.remove(literal)
                state_.add(-literal)
                control = literal.predicate.arguments[0]
                assert isinstance(control, int)
                current_player = control
            if literal.sign and literal.predicate.functor == 'stones':
                state_.remove(literal)
                state_.add(-literal)
                stones = literal.predicate.arguments[0]
                assert isinstance(stones, int)
                state_.add(Literal(NimCausalSetting.stones(stones - take)))
        assert current_player is not None
        assert isinstance(current_player, Agent)
        next_player = Literal(Predicate('control', (self.next_player(current_player),)))
        state_.add(next_player)
        if -next_player in state_:
            state_.remove(-next_player)
        return frozenset(state_)

    @staticmethod
    def stones(number: int = 0) -> Predicate:
        return Predicate('stones', (number,))

    @staticmethod
    def take(number: int = 1) -> Function:
        return Function('take', (number,))
