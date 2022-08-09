from typing import Tuple, Mapping, FrozenSet, Set, Collection, MutableMapping, Type, Sequence, Optional

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
from scpy.util import from_function_to_predicate


@dataclass(frozen=True, order=True, config=DataclassConfig)
class DialecticCausalSetting(CausalSetting):
    fact_set: State = Field(default_factory=frozenset)
    awareness_set: FrozenSet[Predicate] = Field(default_factory=frozenset)
    argument_scheme: Mapping[Function, Tuple[FrozenSet[Literal], FrozenSet[Literal]]] = Field(
        default_factory=frozendict)
    conflict_relation: Preorder = Field(default_factory=Preorder)
    strength_preorder: Preorder = Field(default_factory=Preorder)
    fluents: FrozenSet[Predicate] = Field(init=False, repr=False, default_factory=frozenset)
    actions: FrozenSet[Action] = Field(init=False, repr=False, default_factory=frozenset)
    agents: FrozenSet[Agent] = Field(default_factory=frozenset)

    def __post_init__(self) -> None:
        actions: Set[Action] = set()
        if isinstance(self.awareness_set, frozenset):
            for pred in self.awareness_set:
                arg = Literal(pred)
                actions.add(Function('position', (arg,)))
                actions.add(Function('position', (-arg,)))
        if isinstance(self.argument_scheme, Mapping):
            for arg, cogn_ctx in self.argument_scheme.items():  # type: ignore[assignment]
                preds, poses = cogn_ctx
                for pos in poses:
                    actions.add(Function('supports', (arg, pos)))

        object.__setattr__(self, 'actions', frozenset(actions))

    def __extract_argument_position(self, action: Action, symbol: str = 'supports') -> \
            Tuple[Function, Literal]:
        if action.symbol != symbol:
            raise ValueError(
                f"Unknown Action {action}. Action.symbol is {action.symbol} but should be {symbol}")
        if len(action.arguments) < 2:
            raise ValueError(
                f"Unknown Action {action}. Not enough arguments.")
        arg = action.arguments[0]
        pos = action.arguments[1]
        if not isinstance(arg, Function):
            raise ValueError(
                f"Unknown Action {action}. {arg} must be of type Function, but is type {type(arg).__name__}.")
        if not isinstance(pos, Literal):
            raise ValueError(
                f"Unknown Action {action}. {pos} must be of type Literal, but is type {type(pos).__name__}.")
        if arg not in self.argument_scheme:
            raise ValueError(f"Unknown Action {action}. Argument not in argument scheme.")
        if pos.predicate not in self.awareness_set:
            raise ValueError(f"Unknown Action {action}. Position not in awareness set.")
        e = arg.arguments[0]
        if isinstance(e, Literal):
            if e.predicate not in self.awareness_set:
                raise ValueError(f"Unknown Action {action}. {e.predicate} not in awareness set.")
        else:
            assert isinstance(e, Function)
            if len(e.arguments) != 2:
                raise ValueError(f"Unknown Action {action}. {e} should have exactly two arguments.")
            c = e.arguments[0]
            if not isinstance(c, Literal):
                raise ValueError(
                    f"Unknown Action {action}. {c} must be of type Literal, but is type {type(c).__name__}.")
            if c.predicate not in self.awareness_set:
                raise ValueError(
                    f"Unknown Action {action}. {c.predicate} not in awareness set."
                )
            p = e.arguments[1]
            if not isinstance(p, Literal):
                raise ValueError(
                    f"Unknown Action {action}. {p} must be of type Literal, but is type {type(p).__name__}.")
            if p.predicate not in self.awareness_set:
                raise ValueError(
                    f"Unknown Action {action}. {p.predicate} not in awareness set."
                )

        return arg, pos

    def __is_well_formed(self, literal: Literal, functor: str, *types: Type) -> bool:
        if literal.predicate.functor != functor:
            return False
        types_: Sequence[Type] = tuple(types)
        if len(types_) < len(literal.predicate.arguments):
            return False
        for i, arg in enumerate(literal.predicate.arguments):
            type_: Type = types_[i]
            # noinspection PyTypeHints
            if not isinstance(arg, type_):
                return False
            if type_ is Literal:
                assert isinstance(arg, Literal)
                if arg.predicate not in self.awareness_set:
                    return False
        return True

    def __do_initial_state(self, action: Action) -> State:
        if action.symbol != 'position':
            raise ValueError(
                f"Unknown Action {action}. In initial state Action has to be of form "
                f"{Function('position', (Function('Position'),))}.")
        pos = action.arguments[0]
        if not isinstance(pos, Literal):
            raise ValueError(f"Unknown Action {action}. Position has to be a Literal")
        if pos.predicate not in self.awareness_set:
            raise ValueError(f"Unknown Action {action}. {pos.predicate} is not in the awareness set.")
        argument_lit = Literal(Predicate('position', (pos,)))
        return frozenset({argument_lit})

    def __do_reasoning(self, action: Action, state: State, incomplete: Mapping[Literal, Collection[Literal]],
                       functor: str = 'argument') -> State:
        arg, pos = self.__extract_argument_position(action)
        if not (pos in incomplete and not incomplete[pos]) and not any(
                pos in preds for _, preds in incomplete.items()):
            raise ValueError(f"Unknown Action {action}. Position does not need support.")
        state_ = set(state)
        argument_pred = Predicate(functor, (arg, pos))
        argument_lit = Literal(argument_pred)
        if -argument_lit in state_:
            state_.remove(-argument_lit)
        state_.add(argument_lit)
        return frozenset(state_)

    def __do_attack(self, action: Action, state: State, attack_map: Mapping[Function, Collection[Literal]]) -> State:
        arg, pos = self.__extract_argument_position(action, 'attacks')
        if arg not in attack_map:
            raise ValueError(f"Unknown action {action}. Does not attack argument.")

        attack_pred = from_function_to_predicate(action)
        attack_lit = Literal(attack_pred)
        state_ = set(state)
        if -attack_lit in state:
            state_.remove(-attack_lit)
        state_.add(attack_lit)
        return frozenset(state_)

    def __do_defense(self, action: Action, state: State,
                     undefended_attacks: Mapping[Function, Collection[Literal]]) -> State:
        def_argument, def_position = self.__extract_argument_position(action, 'defends')
        if all(self.strength_preorder.is_strictly_preceded(def_argument, att_argument) for att_argument in
                   undefended_attacks):
            raise ValueError(f"Unknown Action {action}. Defense is not stronger than attack.")
        state_ = set(state)
        def_argument_pred = from_function_to_predicate(action)
        def_argument_lit = Literal(def_argument_pred)
        if -def_argument_lit in state_:
            state_.remove(-def_argument_lit)
        state_.add(def_argument_lit)
        return frozenset(state_)

    def __do_consolidate(self, state: State) -> State:
        att: Optional[Literal] = None
        attacking = set()
        defending = set()
        for literal in state:
            if self.__is_well_formed(literal, 'attacks', Function, Literal):
                functor = literal.predicate.functor
                arg, pos = literal.predicate.arguments
                assert isinstance(arg, Function)
                assert isinstance(pos, Literal)
                lit = Literal(Predicate(functor, (arg, -pos)))
                attacking.add(lit)
                att = literal
            elif self.__is_well_formed(literal, 'defends', Function, Literal):
                defending.add(literal)
        changed = True
        while changed:
            changed = False
            for literal in state:
                if self.__is_well_formed(literal, 'supports', Function, Literal):
                    arg, pos = literal.predicate.arguments
                    assert isinstance(arg, Function)
                    assert isinstance(pos, Literal)
                    for coll in (attacking, defending):
                        if literal in coll:
                            continue
                        for elem in coll:
                            arg, _ = elem.predicate.arguments
                            assert isinstance(arg, Function)
                            preds, _ = self.argument_scheme[arg]
                            if pos in preds:
                                changed = True
                                coll.add(literal)
                                break

        state_ = set(state)
        for attack in attacking:
            counterargument = Literal(Predicate('counterargument', attack.predicate.arguments))
            if -counterargument in state_:
                state_.remove(-counterargument)
            state_.add(counterargument)

        for defence in defending:
            arg = Literal(Predicate('argument', defence.predicate.arguments))
            if -arg in state_:
                state_.remove(-arg)
            state_.add(arg)
        state_ -= (attacking | defending)
        assert not attacking or att is not None
        if att is not None:
            state_.remove(att)
        return frozenset(state_)

    def unsupported_literals(self, state: State, argument: Function) -> Collection[Literal]:
        preds, poses = self.argument_scheme[argument]
        supported = set()
        for literal in state:
            if self.__is_well_formed(literal, 'supports', Function, Literal):
                arg, pos = literal.predicate.arguments
                supported.add(pos)
        return {pred for pred in preds if pred not in supported}

    def attacks(self, state: State) -> Mapping[Function, Collection[Literal]]:
        arguments = set()
        counterarguments = set()
        for literal in state:
            if self.__is_well_formed(literal, 'argument', Function, Literal):
                arg, pos = literal.predicate.arguments
                assert isinstance(arg, Function)
                assert isinstance(pos, Literal)
                arguments.add((arg, pos))
            elif self.__is_well_formed(literal, 'attacks', Function, Literal):
                arg, pos = literal.predicate.arguments
                assert isinstance(arg, Function)
                assert isinstance(pos, Literal)
                counterarguments.add((arg, pos))
        att: MutableMapping[Function, Set[Literal]] = {}
        for (arg, pos) in arguments:
            attacks_ = {counterargument for counterargument in self.conflict_relation[arg]
                        if (counterargument, -pos) not in counterarguments}

            attacks_ |= {counterargument for (counterargument, (preds, poses)) in self.argument_scheme.items()
                         if -pos in poses}

            for attack in attacks_:
                att.setdefault(attack, set()).add(pos)

        return att

    def incomplete_reasoning(self, state: State, functor: str = 'attacks') -> Mapping[Literal, Function]:
        reasoning: MutableMapping[Literal, Function] = {}
        supporting: MutableMapping[Literal, Function] = {}
        for literal in state:
            if self.__is_well_formed(literal, functor, Function, Literal):
                arg, pos = literal.predicate.arguments
                assert isinstance(arg, Function)
                assert isinstance(pos, Literal)
                reasoning[pos] = arg
            elif self.__is_well_formed(literal, 'supports', Function, Literal):
                arg, pos = literal.predicate.arguments
                assert isinstance(arg, Function)
                assert isinstance(pos, Literal)
                supporting[pos] = arg

        incomplete_reasoning: MutableMapping[Literal, Function] = {}

        for pos, arg in reasoning.items():
            preds, _ = self.argument_scheme[arg]
            if not all(pred in supporting for pred in preds):
                incomplete_reasoning[pos] = arg

        return incomplete_reasoning

    def undefended_attacks(self, state: State) -> Mapping[Function, Collection[Literal]]:
        attacking: MutableMapping[Function, Set[Literal]] = {}
        defending: MutableMapping[Function, Set[Literal]] = {}
        for literal in state:
            if self.__is_well_formed(literal, 'attacks', Function, Literal):
                arg, pos = literal.predicate.arguments
                assert isinstance(arg, Function)
                assert isinstance(pos, Literal)
                attacking.setdefault(arg, set()).add(-pos)
            elif self.__is_well_formed(literal, 'supports', Function, Literal):
                arg, pos = literal.predicate.arguments
                assert isinstance(arg, Function)
                assert isinstance(pos, Literal)
                attacking.setdefault(arg, set()).add(pos)
            elif self.__is_well_formed(literal, 'defends', Function, Literal):
                arg, pos = literal.predicate.arguments
                assert isinstance(arg, Function)
                assert isinstance(pos, Literal)
                defending.setdefault(arg, set()).add(pos)

        defended = False
        strong_defense_needed = False
        strong_defended = False
        for att_argument, att_positions in attacking.items():
            for def_argument, def_positions in defending.items():
                if self.strength_preorder.is_strictly_preceded(def_argument, att_argument):
                    strong_defense_needed = True
                if self.strength_preorder.is_strictly_preceded(att_argument, def_argument):
                    strong_defended = True
                if any(-att_position in def_positions for att_position in att_positions):
                    defended = True

        if not defended or strong_defense_needed and not strong_defended:
            return attacking
        return {}

    def incomplete_arguments(self, state: State) -> Mapping[Literal, Collection[Literal]]:
        positions: Set[Literal] = set()
        facts: Set[Function] = set()
        hypotheses: Set[Function] = set()
        arguments: Set[Function] = set()

        for literal in state:
            if self.__is_well_formed(literal, 'position', Literal):
                pos = literal.predicate.arguments[0]
                assert isinstance(pos, Literal)
                positions.add(pos)
            elif self.__is_well_formed(literal, 'argument', Function, Literal):
                arg = literal.predicate.arguments[0]
                assert isinstance(arg, Function)
                if arg.symbol == 'fact':
                    facts.add(arg)
                elif arg.symbol == 'hyp':
                    hypotheses.add(arg)
                else:
                    arguments.add(arg)

        supported: Set[Literal] = {f.arguments[0] for f in facts if isinstance(f.arguments[0], Literal)} | {
            h.arguments[0] for h in hypotheses if isinstance(h.arguments[0], Literal)}
        incomplete: MutableMapping[Literal, Set[Literal]] = {}
        for pos in positions:
            if pos not in supported:
                incomplete[pos] = set()
        for arg in arguments:
            assert isinstance(arg, Function)
            assert arg in self.argument_scheme
            preds, poses = self.argument_scheme[arg]
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
            return self.__do_reasoning(action, state, incomplete_arguments, 'argument')
        incomplete_attacks = self.incomplete_reasoning(state, 'attacks')
        if incomplete_attacks:
            incomplete = {}
            for lit, arg in incomplete_attacks.items():
                incomplete[lit] = self.unsupported_literals(state, arg)
            return self.__do_reasoning(action, state, incomplete, 'supports')
        incomplete_defends = self.incomplete_reasoning(state, 'defends')
        if incomplete_defends:
            incomplete = {}
            for lit, arg in incomplete_defends.items():
                incomplete[lit] = self.unsupported_literals(state, arg)
            return self.__do_reasoning(action, state, incomplete, 'supports')
        undefended_attacks = self.undefended_attacks(state)
        if undefended_attacks:
            for attack, att_posses in undefended_attacks.items():
                for possible_defence in self.strength_preorder[attack]:
                    if not self.conflict_relation.is_similar(attack, possible_defence):
                        if possible_defence not in self.argument_scheme:
                            continue
                        if not any(-att_pos in self.argument_scheme[possible_defence][1] for att_pos in att_posses):
                            continue
                    if possible_defence.symbol == 'fact':
                        f = possible_defence.arguments[0]
                        assert isinstance(f, Literal)
                        if f not in self.fact_set:
                            continue
                    return self.__do_defense(action, state, undefended_attacks)
        if is_consolidate(action):
            return self.__do_consolidate(state)
        att = self.attacks(state)
        if att:
            return self.__do_attack(action, state, att)
        return state

    def poss(self, action: Action, situation: Situation) -> bool:
        return self.poss_state(action, situation.state)

    def poss_state(self, action: Action, state: State) -> bool:
        pass


def is_consolidate(action: Action) -> bool:
    return action.symbol == 'consolidate' and not action.arguments


consolidate_action: Action = Function('consolidate')


def fact(lit: Literal) -> Function:
    return Function('fact', (lit,))


def hyp(lit: Literal) -> Function:
    return Function('hyp', (lit,))


def suff_p(cond: Literal, pos: Literal) -> Function:
    return Function('suff_p', (Function('cond_for', (cond, pos)),))


def necc_p(cond: Literal, pos: Literal) -> Function:
    return Function('necc_p', (Function('cond_for', (cond, pos)),))


def suff_e(cond: Literal, pos: Literal) -> Function:
    return Function('suff_e', (Function('cond_for', (cond, pos)),))


def necc_e(cond: Literal, pos: Literal) -> Function:
    return Function('necc_e', (Function('cond_for', (cond, pos)),))


def sec_suff_p(cond: Literal, pos: Literal) -> Function:
    return Function('sec_suff_p', (Function('cond_for', (cond, pos)),))


def sec_necc_p(cond: Literal, pos: Literal) -> Function:
    return Function('sec_necc_p', (Function('cond_for', (cond, pos)),))


def sec_suff_e(cond: Literal, pos: Literal) -> Function:
    return Function('sec_suff_e', (Function('cond_for', (cond, pos)),))


def exo_e(pos: Literal) -> Function:
    return Function('exo_e', (Function('cond_for', (pos, Function('exo', (pos,)))),))


def position_literal(pos: Literal, sign: bool = True) -> Literal:
    return Literal(Predicate('position', (pos,)), sign)


def argument_literal(arg: Function, pos: Literal, sign: bool = True) -> Literal:
    return Literal(Predicate('argument', (arg, pos)), sign)


def counterargument_literal(arg: Function, pos: Literal, sign: bool = True) -> Literal:
    return Literal(Predicate('counterargument', (arg, pos)), sign)


def supports_literal(arg: Function, pos: Literal, sign: bool = True) -> Literal:
    return Literal(Predicate('supports', (arg, pos)), sign)


def attacks_literal(arg: Function, pos: Literal, sign: bool = True) -> Literal:
    return Literal(Predicate('attacks', (arg, pos)), sign)


def defends_literal(arg: Function, pos: Literal, sign: bool = True) -> Literal:
    return Literal(Predicate('defends', (arg, pos)), sign)


def exo_literal(pos: Literal, sign: bool = True) -> Literal:
    return Literal(Predicate('exo', (pos,)), sign)


def position_action(arg: Function, pos: Literal) -> Action:
    return Function('position', (arg, pos))


def argument_action(arg: Function, pos: Literal) -> Action:
    return Function('argument', (arg, pos))


def counterargument_action(arg: Function, pos: Literal) -> Action:
    return Function('counterargument', (arg, pos))


def supports_action(arg: Function, pos: Literal) -> Action:
    return Function('supports', (arg, pos))


def attacks_action(arg: Function, pos: Literal) -> Action:
    return Function('attacks', (arg, pos))


def defends_action(arg: Function, pos: Literal) -> Action:
    return Function('defends', (arg, pos))
