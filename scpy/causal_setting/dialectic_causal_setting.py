from typing import Tuple, Mapping, FrozenSet, Set, Collection, MutableMapping

from frozendict import frozendict  # type: ignore
from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.action.action import Action
from scpy.agent.agent import Agent
from scpy.causal_setting.causal_setting import CausalSetting
from scpy.dataclass_config import DataclassConfig
from scpy.preorder import Preorder
from scpy.primitives import Function, Literal, Predicate
from scpy.situation.situation import Situation
from scpy.state.state import State


@dataclass(frozen=True, order=True, config=DataclassConfig)
class DialecticCausalSetting(CausalSetting):
    fact_set: State = Field(default_factory=frozenset)
    awareness_set: FrozenSet[Predicate] = Field(default_factory=frozenset)
    argument_scheme: Mapping[Function, Tuple[FrozenSet[Literal], FrozenSet[Literal]]] = Field(
        default_factory=frozendict)
    strength_preorder: Preorder = Field(default_factory=Preorder)
    fluents: FrozenSet[Predicate] = Field(init=False, repr=False, default_factory=frozenset)
    actions: FrozenSet[Action] = Field(init=False, repr=False, default_factory=frozenset)
    agents: FrozenSet[Agent] = Field(default_factory=frozenset)

    def __post_init__(self) -> None:
        actions: Set[Action] = set()
        if isinstance(self.awareness_set, frozenset):
            for pred in self.awareness_set:
                argument = Literal(pred)
                actions.add(Function('position', (argument,)))
                actions.add(Function('position', (-argument,)))
        if isinstance(self.argument_scheme, Mapping):
            for argument, cognitive_cond in self.argument_scheme.items():  # type: ignore[assignment]
                preds, poses = cognitive_cond
                for pos in poses:
                    actions.add(Function('supports', (argument, pos)))

        object.__setattr__(self, 'actions', frozenset(actions))

    def __do_initial_state(self, action: Action) -> State:
        if action.symbol != 'position':
            raise ValueError(
                f"Unknown Action {action}. In initial state Action has to be of form {Function('position', (Function('Argument'),))}.")
        argument = action.arguments[0]
        if not isinstance(argument, Literal):
            raise ValueError(f"Unknown Action {action}. Position has to be a Literal")
        if argument.predicate not in self.awareness_set:
            raise ValueError(f"Unknown Action {action}. {argument.predicate} is not in the awareness set.")
        argument_lit = Literal(Predicate('position', (argument,)))
        return frozenset({argument_lit})

    def __do_argument(self, action: Action, state: State, incomplete: Mapping[Literal, Collection[Literal]]) -> State:
        if action.symbol != 'supports':
            raise ValueError(
                f"Unknown Action {action}. In incomplete state Action has to be of form {Function('supports', (Function('Argument'), Function('Position')))}")
        if len(action.arguments) < 2:
            raise ValueError(
                f"Unknown Action {action}. In incomplete state Action has to be of form {Function('supports', (Function('Argument'), Function('Position')))}")
        argument = action.arguments[0]
        position = action.arguments[1]
        if not isinstance(argument, Function):
            raise ValueError(f"Unknown Action {action}. Argument must be a Function.")
        if not isinstance(position, Literal):
            raise ValueError(f"Unknown Action {action}. Position must be a Literal.")
        if argument not in self.argument_scheme:
            raise ValueError(f"Unknown Action {action}. Argument not in argument scheme.")
        if position not in incomplete:
            raise ValueError(f"Unknown Action {action}. Position does not need support.")

        state_ = set(state)
        argument_pred = Predicate('argument', (argument,))
        argument_lit = Literal(argument_pred)
        if -argument_lit in state_:
            state_.remove(-argument_lit)
        state_.add(argument_lit)
        return frozenset(state_)

    # def attacks(self, state: State) -> Mapping[Function, ]:

    def incomplete(self, state: State) -> Mapping[Literal, Collection[Literal]]:
        positions: Set[Literal] = set()
        facts: Set[Function] = set()
        hypotheses: Set[Function] = set()
        arguments: Set[Function] = set()

        for literal in state:
            if literal.predicate.functor == 'position':
                assert isinstance(literal.predicate.arguments[0], Literal)
                positions.add(literal.predicate.arguments[0])
            if literal.predicate.functor == 'argument':
                argument_ = literal.predicate
                argument = argument_.arguments[0]
                assert isinstance(argument, Function)
                if argument.symbol == 'fact':
                    facts.add(argument)
                elif argument.symbol == 'hyp':
                    hypotheses.add(argument)
                else:
                    arguments.add(argument)

        supported: Set[Literal] = {fact.arguments[0] for fact in facts if isinstance(fact.arguments[0], Literal)} | {
            hypothesis.arguments[0] for hypothesis in hypotheses if isinstance(hypothesis.arguments[0], Literal)}
        incomplete: MutableMapping[Literal, Set[Literal]] = {}
        for position in positions:
            if position not in supported:
                incomplete[position] = set()
        for argument in arguments:
            assert isinstance(argument, Function)
            assert argument in self.argument_scheme
            preds, poses = self.argument_scheme[argument]
            incomplete_ = set()
            for pred in preds:
                if pred not in supported:
                    incomplete_.add(pred)
            if not incomplete_:
                supported.update(poses)
                next_incomplete = dict(incomplete)
                for pos, preds_ in incomplete.items():
                    if preds_ <= poses:
                        del next_incomplete[pos]
                        supported.add(pos)
                incomplete = next_incomplete
            else:
                for pos in poses:
                    incomplete.setdefault(pos, set())
                    incomplete[pos].update(incomplete_)
        return incomplete

    def do_state(self, action: Action, state: State) -> State:
        if not state:
            return self.__do_initial_state(action)
        incomplete = self.incomplete(state)
        if incomplete:
            return self.__do_argument(action, state, incomplete)
        # attacks = self.attacks(state)
        assert False
        return state

    def poss(self, action: Action, situation: Situation) -> bool:
        return self.poss_state(action, situation.state)

    def poss_state(self, action: Action, state: State) -> bool:
        pass
