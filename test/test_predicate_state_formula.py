# noinspection DuplicatedCode
import unittest

from scpy.formula.negation_formula import EvaluableNegationFormula
from scpy.formula.state_formula.predicate_state_formula import PredicateStateFormula
from scpy.primitives import Literal, Predicate
from scpy.situation.situation import Situation


class TestConstructor(unittest.TestCase):

    def test_create_simple(self):
        a = Predicate('a')
        phi = PredicateStateFormula(a)
        expected = 'a'
        actual = phi.predicate.functor
        self.assertEqual(expected, actual)


class TestEvaluateSituation(unittest.TestCase):

    def test_simple(self):
        a = Predicate('a')
        a_lit = Literal(a)
        phi = PredicateStateFormula(a)
        state = frozenset({a_lit})
        s0 = Situation(state)
        expected = True
        actual = phi.evaluate(s0)
        self.assertEqual(expected, actual)

    def test_negation(self):
        a = Predicate('a')
        a_lit = Literal(a)
        phi = EvaluableNegationFormula(PredicateStateFormula(a))
        state = frozenset({-a_lit})
        s0 = Situation(state)
        expected = True
        actual = phi.evaluate(s0)
        self.assertEqual(expected, actual)

    def test_default_negation(self):
        a = Predicate('a')
        a_lit = Literal(a)
        b = Predicate('b')
        b_lit = Literal(b)
        phi = EvaluableNegationFormula(PredicateStateFormula(a))
        state = frozenset({b_lit})
        s0 = Situation(state)
        expected = True
        actual = phi.evaluate(s0)
        self.assertEqual(expected, actual)

    def test_strong_negation(self):
        a = Predicate('a')
        a_lit = Literal(a)
        phi = PredicateStateFormula(a)
        state = frozenset({-a_lit})
        s0 = Situation(state)
        expected = False
        actual = phi.evaluate(s0)
        self.assertEqual(expected, actual)


class TestEvaluateState(unittest.TestCase):

    def test_simple(self):
        a = Predicate('a')
        a_lit = Literal(a)
        phi = PredicateStateFormula(a)
        state = frozenset({a_lit})
        expected = True
        actual = phi.evaluate(state)
        self.assertEqual(expected, actual)
