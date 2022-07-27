# noinspection DuplicatedCode
import unittest

from scpy.formula.path_formula.next_path_formula import NextPathFormula
from scpy.formula.path_formula.state_path_formula import StatePathFormula
from scpy.formula.state_formula.predicate_state_formula import PredicateStateFormula
from scpy.literal import Literal
from scpy.path import Path
from scpy.predicate import Predicate
from scpy.situation import Situation
from test.simple_test_causal_setting import SimpleTestCausalSetting


class TestConstructor(unittest.TestCase):

    def test_create_simple(self):
        a = Predicate('a')
        a_lit = Literal(a)
        cap_phi = PredicateStateFormula(a_lit)
        phi_ = StatePathFormula(cap_phi)
        phi = NextPathFormula(phi_)


class TestEvaluatePath(unittest.TestCase):

    def test_simple_expanded(self):
        a = Predicate('a')
        a_lit = Literal(a)
        cap_phi = PredicateStateFormula(a_lit)
        phi_ = StatePathFormula(cap_phi)
        phi = NextPathFormula(phi_)
        state = frozenset({a_lit})
        s0 = Situation(state)
        t = SimpleTestCausalSetting()

        path = Path(s0)
        path.expand(t)
        path.expand(t)

        actual = phi.evaluate_path(path)
        expected = True
        self.assertEqual(expected, actual)

    def test_simple_unexpanded(self):
        a = Predicate('a')
        a_lit = Literal(a)
        cap_phi = PredicateStateFormula(a_lit)
        phi_ = StatePathFormula(cap_phi)
        phi = NextPathFormula(phi_)
        state = frozenset({a_lit})
        s0 = Situation(state)

        path = Path(s0)

        actual = phi.evaluate_path(path)
        expected = 'Inconclusive'
        self.assertEqual(expected, actual)

    def test_nested(self):
        a = Predicate('a')
        a_lit = Literal(a)
        cap_phi = PredicateStateFormula(a_lit)
        phi__ = StatePathFormula(cap_phi)
        phi_ = NextPathFormula(phi__)
        phi = NextPathFormula(phi_)
        state = frozenset({a_lit})
        s0 = Situation(state)
        t = SimpleTestCausalSetting()

        path = Path(s0)
        path.expand(t)
        path.expand(t)
        path.expand(t)

        actual = phi.evaluate_path(path)
        expected = True
        self.assertEqual(expected, actual)

    def test_counterexample_impossible(self):
        d = Predicate('d')
        d_lit = Literal(d)
        cap_phi = PredicateStateFormula(d_lit)
        phi_ = StatePathFormula(cap_phi)
        phi = NextPathFormula(phi_)
        state = frozenset()
        s0 = Situation(state)
        t = SimpleTestCausalSetting()

        path = Path(s0)
        path.expand(t)
        path.expand(t)

        actual = phi.evaluate_path(path)
        expected = False
        self.assertEqual(expected, actual)
