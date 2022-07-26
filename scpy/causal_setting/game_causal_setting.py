from pydantic.dataclasses import dataclass

from scpy.action.action import Action
from scpy.agent.agent import Agent
from scpy.causal_setting.causal_setting import CausalSetting
from scpy.primitives import Function, Predicate
from scpy.situation.situation import Situation
from scpy.state.state import State


@dataclass(frozen=True, order=True)
class GameCausalSetting(CausalSetting):

    def _legal_move_state(self, agent: Agent, move: Function, state: State) -> bool:
        raise NotImplementedError

    def _legal_move_situation(self, agent: Agent, move: Function, situation: Situation) -> bool:
        return self._legal_move_state(agent, move, situation.state)

    def poss_state(self, action: Action, state: State) -> bool:
        if action.symbol != 'tick' and len(action.arguments) != len(self.agents) and not all(
                isinstance(argument, Function) for argument in action.arguments):
            return False
        return all(self._legal_move_state(agent, move, state) for agent, move in enumerate(action.arguments) if
                   isinstance(move, Function))

    def _poss(self, action: Action, situation: Situation) -> bool:
        if action.symbol != 'tick' and len(action.arguments) != len(self.agents) and not all(
                isinstance(argument, Function) for argument in action.arguments):
            return False
        return all(self._legal_move_situation(agent, move, situation) for agent, move in enumerate(action.arguments) if
                   isinstance(move, Function))

    def next_player(self, current_player: Agent = 0) -> Agent:
        return (current_player + 1) % len(self.agents)

    def tick(self, player: Agent, move: Function) -> Action:
        args = [GameCausalSetting.noop() for _ in range(0, player)] + \
               [move] + \
               [GameCausalSetting.noop() for _ in range(player + 1, len(self.agents))]
        return Function('tick', tuple(args))

    @staticmethod
    def noop() -> Function:
        return Function('noop')

    @staticmethod
    def control(player: Agent = 0) -> Predicate:
        return Predicate('control', (player,))
