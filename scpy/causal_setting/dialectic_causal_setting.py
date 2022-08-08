from typing import Tuple, Mapping, FrozenSet, Set, Collection, MutableMapping, Type, Sequence

from frozendict import frozendict  # type: ignore
from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.action.action import Action
from scpy.agent.agent import Agent
from scpy.causal_setting.causal_setting import CausalSetting
from scpy.dataclass_config import DataclassConfig
from scpy.preorder import Preorder
from scpy.primitives import Function, Literal, Predicate
from scpy.relation import Relation
from scpy.situation.situation import Situation
from scpy.state.state import State
from scpy.util import from_function_to_predicate


@dataclass(frozen=True, order=True, config=DataclassConfig)
class DialecticCausalSetting(CausalSetting):
    fact_set: State = Field(default_factory=frozenset)
    awareness_set: FrozenSet[Predicate] = Field(default_factory=frozenset)
    argument_scheme: Mapping[Function, Tuple[FrozenSet[Literal], FrozenSet[Literal]]] = Field(
        default_factory=frozendict)
    conflict_relation: Relation = Field(default_factory=Relation)
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

    def __extract_argument_position(self, action: Action, symbol: str = 'supports') -> \
            Tuple[Function, Literal]:
        if action.symbol != symbol:
            raise ValueError(
                f"Unknown Action {action}. Action.symbol is {action.symbol} but should be {symbol}")
        if len(action.arguments) < 2:
            raise ValueError(
                f"Unknown Action {action}. Not enough arguments.")
        argument = action.arguments[0]
        position = action.arguments[1]
        if not isinstance(argument, Function):
            raise ValueError(
                f"Unknown Action {action}. Argument must be of type Function, but is type {type(argument).__name__}.")
        if not isinstance(position, Literal):
            raise ValueError(
                f"Unknown Action {action}. Position must be of type Literal, but is type {type(argument).__name__}.")
        if argument not in self.argument_scheme:
            raise ValueError(f"Unknown Action {action}. Argument not in argument scheme.")

        return argument, position

    def __do_reasoning(self, action: Action, state: State, incomplete: Mapping[Literal, Collection[Literal]],
                       functor: str = 'argument') -> State:
        argument, position = self.__extract_argument_position(action)
        if not (position in incomplete and not incomplete[position]) and not any(
                position in preds for pos, preds in incomplete.items()):
            raise ValueError(f"Unknown Action {action}. Position does not need support.")
        state_ = set(state)
        argument_pred = Predicate(functor, (argument, position))
        argument_lit = Literal(argument_pred)
        if -argument_lit in state_:
            state_.remove(-argument_lit)
        state_.add(argument_lit)
        return frozenset(state_)

    def __do_attack(self, action: Action, state: State, attacks: Mapping[Function, Collection[Literal]]) -> State:
        argument,position = self.__extract_argument_position(action, 'attacks')
        if argument not in attacks:
            raise ValueError(f"Unknown action {action}. Does not attack argument.")

        attack_pred = from_function_to_predicate(action)
        attack_lit = Literal(attack_pred)
        state_ = set(state)
        if -attack_lit in state:
            state_.remove(-attack_lit)
        state_.add(attack_lit)
        return frozenset(state_)

    def __is_well_formed(self, literal: Literal, functor: str, *types: Type) -> bool:
        if literal.predicate.functor != functor:
            return False
        types_: Sequence[Type] = tuple(types)
        if len(types_) < len(literal.predicate.arguments):
            return False
        for i, argument in enumerate(literal.predicate.arguments):
            type_: Type = types_[i]
            if not isinstance(argument, type_):  # type: ignore
                return False
        return True

    def attacks(self, state: State) -> Mapping[Function, Collection[Literal]]:
        arguments = set()
        counterarguments = set()
        for literal in state:
            if literal.predicate.functor == 'argument':
                if len(literal.predicate.arguments) < 2:
                    continue
                argument = literal.predicate.arguments[0]
                if not isinstance(argument, Function):
                    continue
                position = literal.predicate.arguments[1]
                if not isinstance(position, Literal):
                    continue
                arguments.add((argument, position))
            elif literal.predicate.functor == 'attacks':
                if len(literal.predicate.arguments) < 2:
                    continue
                argument = literal.predicate.arguments[0]
                if not isinstance(argument, Function):
                    continue
                position = literal.predicate.arguments[1]
                if not isinstance(position, Literal):
                    continue
                counterarguments.add((argument, position))
        attacks: MutableMapping[Function, Set[Literal]] = {}
        for (argument, position) in arguments:
            attacks_ = {counterargument for counterargument in self.conflict_relation[argument]
                        if (counterargument, -position) not in counterarguments}

            attacks_ |= {counterargument for (counterargument, (preds, poses)) in self.argument_scheme.items()
                         if -position in poses}

            for attack in attacks_:
                attacks.setdefault(attack, set()).add(position)

        return attacks

    def incomplete_attacks(self, state: State) -> Mapping[Literal, Function]:
        attacks: MutableMapping[Literal, Function] = {}
        supports: MutableMapping[Literal, Function] = {}
        for literal in state:
            if self.__is_well_formed(literal, 'attacks', Function, Literal):
                argument, position = literal.predicate.arguments
                assert isinstance(argument, Function)
                assert isinstance(position, Literal)
                attacks[position] = argument
            elif self.__is_well_formed(literal, 'supports', Function, Literal) or \
                    self.__is_well_formed(literal, 'argument', Function, Literal) or \
                    self.__is_well_formed(literal, 'counterargument', Function, Literal):
                argument, position = literal.predicate.arguments
                assert isinstance(argument, Function)
                assert isinstance(position, Literal)
                supports[position] = argument

        incomplete_attacks: MutableMapping[Literal, Function] = {}

        for position, argument in attacks.items():
            preds, _ = self.argument_scheme[argument]
            if not all(pred in supports for pred in preds):
                incomplete_attacks[position] = argument

        return incomplete_attacks

    def undefended_attacks(self, state: State) -> Mapping[Literal, Function]:
        raise NotImplementedError

    def incomplete_arguments(self, state: State) -> Mapping[Literal, Collection[Literal]]:
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
        incomplete_arguments = self.incomplete_arguments(state)
        if incomplete_arguments:
            return self.__do_reasoning(action, state, incomplete_arguments)
        incomplete_attacks = self.incomplete_attacks(state)
        if incomplete_attacks:
            pass
        attacks = self.attacks(state)
        if attacks:
            return self.__do_attack(action, state, attacks)
        return state

    def poss(self, action: Action, situation: Situation) -> bool:
        return self.poss_state(action, situation.state)

    def poss_state(self, action: Action, state: State) -> bool:
        pass
