# noinspection DuplicatedCode
import unittest

from scpy.action.action import Action
from scpy.formula.negation_formula import EvaluableNegationFormula
from scpy.formula.special_formula import TrueFormula
from scpy.formula.state_formula.predicate_state_formula import PredicateStateFormula
from scpy.function.function import Function
from scpy.literal.literal import Literal
from scpy.path.path_with_strategy import PathWithStrategy
from scpy.predicate.predicate import Predicate
from scpy.situation.situation import Situation
from scpy.strategy.choice_strategy import ChoiceStrategy
from scpy.strategy.preconditional_action_strategy import PreconditionalActionStrategy
from scpy.trace.trace import Trace
from test.simple_test_causal_setting import SimpleTestCausalSetting

a = Function('a')
b = Function('b')
c = Function('c')
add_a: Action = Function('add', (a,))
add_b: Action = Function('add', (b,))
add_c: Action = Function('add', (c,))
remove_a: Action = Function('remove', (a,))
remove_b: Action = Function('remove', (b,))
remove_c: Action = Function('remove', (c,))


class TestConstructor(unittest.TestCase):

    def test_create_simple(self):
        a_pred = Predicate('a')
        cond_a = EvaluableNegationFormula(PredicateStateFormula(a_pred))
        cond_a_comp = PredicateStateFormula(a_pred)

        strat_a = PreconditionalActionStrategy(cond_a, add_a)
        strat_add_b = PreconditionalActionStrategy(cond_a_comp, add_b)
        strat_remove_b = PreconditionalActionStrategy(cond_a_comp, remove_b)

        strat_b = ChoiceStrategy(strat_add_b, strat_remove_b)

        strat = ChoiceStrategy(strat_a, strat_b)

        state0 = frozenset()
        s0 = Situation(state0)
        p = PathWithStrategy(s0, strategy=strat)


class TestExpand(unittest.TestCase):

    def test_simple_none(self):
        a_pred = Predicate('a')
        cond_a = EvaluableNegationFormula(PredicateStateFormula(a_pred))
        cond_a_comp = PredicateStateFormula(a_pred)

        strat_a = PreconditionalActionStrategy(cond_a, add_a)
        strat_add_b = PreconditionalActionStrategy(cond_a_comp, add_b)
        strat_remove_b = PreconditionalActionStrategy(cond_a_comp, remove_b)

        strat_b = ChoiceStrategy(strat_add_b, strat_remove_b)

        strat = ChoiceStrategy(strat_a, strat_b)

        state0 = frozenset()
        s0 = Situation(state0)
        p = PathWithStrategy(s0, strategy=strat)
        actual = p.traces
        expected = set()

        self.assertSetEqual(expected, actual)

    def test_simple_once(self):
        a_pred = Predicate('a')
        cond_a = EvaluableNegationFormula(PredicateStateFormula(a_pred))
        cond_a_comp = PredicateStateFormula(a_pred)

        strat_a = PreconditionalActionStrategy(cond_a, add_a)
        strat_add_b = PreconditionalActionStrategy(cond_a_comp, add_b)
        strat_remove_b = PreconditionalActionStrategy(cond_a_comp, remove_b)

        strat_b = ChoiceStrategy(strat_add_b, strat_remove_b)

        strat = ChoiceStrategy(strat_a, strat_b)

        state0 = frozenset()
        s0 = Situation(state0)
        p = PathWithStrategy(s0, strategy=strat)

        t = SimpleTestCausalSetting()

        p.expand(t)

        actual = p.traces
        expected = {Trace((state0,))}

        self.assertSetEqual(expected, actual)

    def test_simple_twice(self):
        a_pred = Predicate('a')
        a_lit = Literal(a_pred)
        cond_a = EvaluableNegationFormula(PredicateStateFormula(a_pred))
        cond_a_comp = PredicateStateFormula(a_pred)

        strat_a = PreconditionalActionStrategy(cond_a, add_a)
        strat_add_b = PreconditionalActionStrategy(cond_a_comp, add_b)
        strat_remove_b = PreconditionalActionStrategy(cond_a_comp, remove_b)

        strat_b = ChoiceStrategy(strat_add_b, strat_remove_b)

        strat = ChoiceStrategy(strat_a, strat_b)

        state0 = frozenset()
        state1 = frozenset({a_lit})
        s0 = Situation(state0)
        p = PathWithStrategy(s0, strategy=strat)

        t = SimpleTestCausalSetting()

        p.expand(t)
        p.expand(t)

        actual = p.traces
        expected = {
            Trace((state0, state1), (add_a,))
        }

        self.assertSetEqual(expected, actual)

    def test_simple_thrice(self):
        a_pred = Predicate('a')
        a_lit = Literal(a_pred)
        b_pred = Predicate('b')
        b_lit = Literal(b_pred)
        cond_a = EvaluableNegationFormula(PredicateStateFormula(a_pred))
        cond_a_comp = PredicateStateFormula(a_pred)

        strat_a = PreconditionalActionStrategy(cond_a, add_a)
        strat_add_b = PreconditionalActionStrategy(cond_a_comp, add_b)
        strat_remove_b = PreconditionalActionStrategy(cond_a_comp, remove_b)

        strat_b = ChoiceStrategy(strat_add_b, strat_remove_b)

        strat = ChoiceStrategy(strat_a, strat_b)

        state0 = frozenset()
        state1 = frozenset({a_lit})
        state2 = frozenset({a_lit, b_lit})
        s0 = Situation(state0)
        p = PathWithStrategy(s0, strategy=strat)

        t = SimpleTestCausalSetting()

        p.expand(t)
        p.expand(t)
        p.expand(t)

        actual = p.traces
        expected = {
            Trace((state0, state1, state2), (add_a, add_b))
        }

        self.assertSetEqual(expected, actual)

    def test_simple_four_times(self):
        a_pred = Predicate('a')
        a_lit = Literal(a_pred)
        b_pred = Predicate('b')
        b_lit = Literal(b_pred)
        cond_a = EvaluableNegationFormula(PredicateStateFormula(a_pred))
        cond_a_comp = PredicateStateFormula(a_pred)

        strat_a = PreconditionalActionStrategy(cond_a, add_a)
        strat_add_b = PreconditionalActionStrategy(cond_a_comp, add_b)
        strat_remove_b = PreconditionalActionStrategy(cond_a_comp, remove_b)

        strat_b = ChoiceStrategy(strat_add_b, strat_remove_b)

        strat = ChoiceStrategy(strat_a, strat_b)

        state0 = frozenset()
        state1 = frozenset({a_lit})
        state2 = frozenset({a_lit, b_lit})
        state3 = frozenset({a_lit, -b_lit})
        s0 = Situation(state0)
        p = PathWithStrategy(s0, strategy=strat)

        t = SimpleTestCausalSetting()

        p.expand(t)
        p.expand(t)
        p.expand(t)
        p.expand(t)

        actual = p.traces
        expected = {
            Trace((state0, state1, state2, state3), (add_a, add_b, remove_b))
        }

        self.assertSetEqual(expected, actual)

    def test_complex_once(self):
        a_pred = Predicate('a')
        a_lit = Literal(a_pred)
        b_pred = Predicate('b')
        b_lit = Literal(b_pred)
        c_pred = Predicate('c')
        c_lit = Literal(c_pred)
        cond_a = EvaluableNegationFormula(PredicateStateFormula(a_pred))
        cond_a_comp = PredicateStateFormula(a_pred)

        strat_a = PreconditionalActionStrategy(cond_a, add_a)
        strat_add_b = PreconditionalActionStrategy(cond_a_comp, add_b)
        strat_remove_b = PreconditionalActionStrategy(cond_a_comp, remove_b)
        strat_add_c = PreconditionalActionStrategy(TrueFormula(), add_c)
        strat_remove_c = PreconditionalActionStrategy(TrueFormula(), remove_c)

        strat_b = ChoiceStrategy(strat_add_b, strat_remove_b)
        strat_c = ChoiceStrategy(strat_add_c, strat_remove_c)

        strat_ex = ChoiceStrategy(strat_b, strat_c)

        strat = ChoiceStrategy(strat_a, strat_ex)

        state1 = frozenset()
        s0 = Situation(state1)
        p = PathWithStrategy(s0, strategy=strat)

        t = SimpleTestCausalSetting()

        p.expand(t)

        actual = p.traces
        expected = {
            Trace((state1,), ()),
        }

        self.assertSetEqual(expected, actual)

    def test_complex_twice(self):
        a_pred = Predicate('a')
        a_lit = Literal(a_pred)
        b_pred = Predicate('b')
        b_lit = Literal(b_pred)
        c_pred = Predicate('c')
        c_lit = Literal(c_pred)
        cond_a = EvaluableNegationFormula(PredicateStateFormula(a_pred))
        cond_a_comp = PredicateStateFormula(a_pred)

        strat_a = PreconditionalActionStrategy(cond_a, add_a)
        strat_add_b = PreconditionalActionStrategy(cond_a_comp, add_b)
        strat_remove_b = PreconditionalActionStrategy(cond_a_comp, remove_b)
        strat_add_c = PreconditionalActionStrategy(TrueFormula(), add_c)
        strat_remove_c = PreconditionalActionStrategy(TrueFormula(), remove_c)

        strat_b = ChoiceStrategy(strat_add_b, strat_remove_b)
        strat_c = ChoiceStrategy(strat_add_c, strat_remove_c)

        strat_ex = ChoiceStrategy(strat_b, strat_c)

        strat = ChoiceStrategy(strat_a, strat_ex)

        state1 = frozenset()
        state1a = frozenset({a_lit})
        state1b = frozenset({c_lit})
        s0 = Situation(state1)
        p = PathWithStrategy(s0, strategy=strat)

        t = SimpleTestCausalSetting()

        p.expand(t)
        p.expand(t)

        actual = p.traces
        expected = {
            Trace((state1, state1a), (add_a,)),
            Trace((state1, state1b), (add_c,)),
        }

        self.assertSetEqual(expected, actual)

    def test_complex_thrice(self):
        a_pred = Predicate('a')
        a_lit = Literal(a_pred)
        b_pred = Predicate('b')
        b_lit = Literal(b_pred)
        c_pred = Predicate('c')
        c_lit = Literal(c_pred)
        cond_a = EvaluableNegationFormula(PredicateStateFormula(a_pred))
        cond_a_comp = PredicateStateFormula(a_pred)

        strat_a = PreconditionalActionStrategy(cond_a, add_a)
        strat_add_b = PreconditionalActionStrategy(cond_a_comp, add_b)
        strat_remove_b = PreconditionalActionStrategy(cond_a_comp, remove_b)
        strat_add_c = PreconditionalActionStrategy(TrueFormula(), add_c)
        strat_remove_c = PreconditionalActionStrategy(TrueFormula(), remove_c)

        strat_b = ChoiceStrategy(strat_add_b, strat_remove_b)
        strat_c = ChoiceStrategy(strat_add_c, strat_remove_c)

        strat_ex = ChoiceStrategy(strat_b, strat_c)

        strat = ChoiceStrategy(strat_a, strat_ex)

        state1 = frozenset()
        state1a = frozenset({a_lit})
        state1a1 = frozenset({a_lit, b_lit})
        state1a2 = frozenset({a_lit, c_lit})
        state1b = frozenset({c_lit})
        state1b1 = frozenset({a_lit, c_lit})
        state1b2 = frozenset({-c_lit})
        s0 = Situation(state1)
        p = PathWithStrategy(s0, strategy=strat)

        t = SimpleTestCausalSetting()

        p.expand(t)
        p.expand(t)
        p.expand(t)

        actual = p.traces
        expected = {
            Trace((state1, state1a, state1a1), (add_a, add_b)),
            Trace((state1, state1a, state1a2), (add_a, add_c)),
            Trace((state1, state1b, state1b1), (add_c, add_a)),
            Trace((state1, state1b, state1b2), (add_c, remove_c)),
        }

        self.assertSetEqual(expected, actual)

    def test_complex_four_times(self):
        a_pred = Predicate('a')
        a_lit = Literal(a_pred)
        b_pred = Predicate('b')
        b_lit = Literal(b_pred)
        c_pred = Predicate('c')
        c_lit = Literal(c_pred)
        cond_a = EvaluableNegationFormula(PredicateStateFormula(a_pred))
        cond_a_comp = PredicateStateFormula(a_pred)

        strat_a = PreconditionalActionStrategy(cond_a, add_a)
        strat_add_b = PreconditionalActionStrategy(cond_a_comp, add_b)
        strat_remove_b = PreconditionalActionStrategy(cond_a_comp, remove_b)
        strat_add_c = PreconditionalActionStrategy(TrueFormula(), add_c)
        strat_remove_c = PreconditionalActionStrategy(TrueFormula(), remove_c)

        strat_b = ChoiceStrategy(strat_add_b, strat_remove_b)
        strat_c = ChoiceStrategy(strat_add_c, strat_remove_c)

        strat_ex = ChoiceStrategy(strat_b, strat_c)

        strat = ChoiceStrategy(strat_a, strat_ex)

        state1 = frozenset()
        state1a = frozenset({a_lit})  # add(a)
        state1a1 = frozenset({a_lit, b_lit})  # add(a) add(b)
        state1a1a = frozenset({a_lit, -b_lit})  # add(a) add(b) remove(b)
        state1a1b = frozenset({a_lit, b_lit, c_lit})  # add(a) add(b) add(c)
        state1a2 = frozenset({a_lit, c_lit})  # add(a) add(c)
        state1a2a = frozenset({a_lit, b_lit, c_lit})  # add(a) add(c) add(b)
        state1a2b = frozenset({a_lit, -c_lit})  # add(a) add(c) remove(b)
        state1b = frozenset({c_lit})  # add(c)
        state1b1 = frozenset({a_lit, c_lit})  # add(c) add(a)
        state1b1a = frozenset({a_lit, b_lit, c_lit})  # add(c) add(a) add(b)
        state1b1b = frozenset({a_lit, -c_lit})  # add(c) add(a) remove(c)
        state1b2 = frozenset({-c_lit})  # add(c) remove(c)
        state1b2a = frozenset({c_lit})  # add(c) remove(c) add(c)
        state1b2b = frozenset({a_lit, -c_lit})  # add(c) remove(c) add(a)
        s0 = Situation(state1)
        p = PathWithStrategy(s0, strategy=strat)

        t = SimpleTestCausalSetting()

        p.expand(t)
        p.expand(t)
        p.expand(t)
        p.expand(t)

        actual = p.traces
        expected = {
            Trace((state1, state1a, state1a1, state1a1a), (add_a, add_b, remove_b)),
            Trace((state1, state1a, state1a1, state1a1b), (add_a, add_b, add_c)),
            Trace((state1, state1a, state1a2, state1a2a), (add_a, add_c, add_b)),
            Trace((state1, state1a, state1a2, state1a2b), (add_a, add_c, remove_c)),
            Trace((state1, state1b, state1b1, state1b1a), (add_c, add_a, add_b)),
            Trace((state1, state1b, state1b1, state1b1b), (add_c, add_a, remove_c)),
            Trace((state1, state1b, state1b2, state1b2a), (add_c, remove_c, add_c)),
            Trace((state1, state1b, state1b2, state1b2b), (add_c, remove_c, add_a)),
        }

        self.assertSetEqual(expected, actual)
