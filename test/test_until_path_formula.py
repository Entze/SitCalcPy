# noinspection DuplicatedCode
import unittest

from scpy.formula.conjunction_formula import EvaluableConjunctionFormula
from scpy.formula.disjunction_formula import EvaluableDisjunctionFormula
from scpy.formula.negation_formula import EvaluableNegationFormula
from scpy.formula.path_formula.next_path_formula import NextPathFormula
from scpy.formula.path_formula.state_path_formula import StatePathFormula
from scpy.formula.path_formula.until_path_formula import UntilPathFormula
from scpy.formula.state_formula.predicate_state_formula import PredicateStateFormula
from scpy.primitives import Literal, Predicate
from scpy.path.path import Path
from scpy.situation.situation import Situation
from test.simple_test_causal_setting import SimpleTestCausalSetting


class TestConstructor(unittest.TestCase):

    def test_create_simple(self):
        a = Predicate('a')
        cap_phi = PredicateStateFormula(a)
        cap_phi_comp = EvaluableNegationFormula(PredicateStateFormula(a))
        phi_ = StatePathFormula(cap_phi)
        psi_ = StatePathFormula(cap_phi_comp)
        phi = UntilPathFormula(phi_, psi_)


class TestEvaluatePath(unittest.TestCase):

    def test_expanded(self):
        a = Predicate('a')
        a_lit = Literal(a)
        cap_phi = PredicateStateFormula(a)
        cap_phi_comp = EvaluableNegationFormula(PredicateStateFormula(a))
        phi_ = StatePathFormula(cap_phi)
        psi_ = StatePathFormula(cap_phi_comp)
        phi = UntilPathFormula(phi_, psi_)

        state0 = frozenset({a_lit})
        s0 = Situation(state0)

        t = SimpleTestCausalSetting()

        p = Path(s0)
        p.expand(t)
        p.expand(t)

        actual = phi.evaluate(p)
        expected = True

        self.assertEqual(expected, actual)

    def test_unexpanded(self):
        a = Predicate('a')
        a_lit = Literal(a)
        cap_phi = PredicateStateFormula(a)
        cap_phi_comp = EvaluableNegationFormula(PredicateStateFormula(a))
        phi_ = StatePathFormula(cap_phi)
        psi_ = StatePathFormula(cap_phi_comp)
        phi = UntilPathFormula(phi_, psi_)

        state0 = frozenset({a_lit})
        s0 = Situation(state0)

        p = Path(s0)
        actual = phi.evaluate(p)
        expected = 'Inconclusive'

        self.assertEqual(expected, actual)

    def test_counterexample(self):
        a = Predicate('a')
        a_lit = Literal(a)
        b = Predicate('b')
        cap_phi = PredicateStateFormula(a)
        cap_phi_comp = EvaluableNegationFormula(PredicateStateFormula(a))
        cap_delta = PredicateStateFormula(b)
        psi_ = EvaluableConjunctionFormula(cap_phi_comp, cap_delta)
        phi_ = StatePathFormula(cap_phi)
        phi = UntilPathFormula(phi_, psi_)

        state0 = frozenset({a_lit})
        s0 = Situation(state0)

        t = SimpleTestCausalSetting()

        p = Path(s0)
        p.expand(t)
        p.expand(t)

        actual = phi.evaluate(p)
        expected = False

        self.assertEqual(expected, actual)

    def test_complex_psi_unexpanded0(self):
        a = Predicate('a')
        a_lit = Literal(a)
        b = Predicate('b')
        cap_phi = PredicateStateFormula(a)
        cap_phi_comp = EvaluableNegationFormula(PredicateStateFormula(a))
        cap_delta = PredicateStateFormula(b)
        delta_ = EvaluableConjunctionFormula(cap_phi_comp, cap_delta)
        psi_ = NextPathFormula(delta_)
        phi_ = StatePathFormula(cap_phi)
        phi = UntilPathFormula(phi_, psi_)

        state0 = frozenset({a_lit})
        s0 = Situation(state0)

        t = SimpleTestCausalSetting()

        p = Path(s0)

        actual = phi.evaluate(p)
        expected = 'Inconclusive'

        self.assertEqual(expected, actual)

    def test_complex_psi_unexpanded1(self):
        a = Predicate('a')
        a_lit = Literal(a)
        b = Predicate('b')
        cap_phi = PredicateStateFormula(a)
        cap_phi_comp = EvaluableNegationFormula(PredicateStateFormula(a))
        cap_delta = PredicateStateFormula(b)
        delta_ = EvaluableConjunctionFormula(cap_phi_comp, cap_delta)
        psi_ = NextPathFormula(delta_)
        phi_ = StatePathFormula(cap_phi)
        phi = UntilPathFormula(phi_, psi_)

        state0 = frozenset({a_lit})
        s0 = Situation(state0)

        t = SimpleTestCausalSetting()

        p = Path(s0)
        p.expand(t)

        actual = phi.evaluate(p)
        expected = 'Inconclusive'

        self.assertEqual(expected, actual)

    def test_complex_psi_unexpanded2(self):
        a = Predicate('a')
        a_lit = Literal(a)
        b = Predicate('b')
        cap_phi = PredicateStateFormula(a)
        cap_phi_comp = EvaluableNegationFormula(PredicateStateFormula(a))
        cap_delta = PredicateStateFormula(b)
        delta_ = EvaluableConjunctionFormula(cap_phi_comp, cap_delta)
        psi_ = NextPathFormula(delta_)
        phi_ = StatePathFormula(cap_phi)
        phi = UntilPathFormula(phi_, psi_)

        state0 = frozenset({a_lit})
        s0 = Situation(state0)

        t = SimpleTestCausalSetting()

        p = Path(s0)
        p.expand(t)
        p.expand(t)

        actual = phi.evaluate(p)
        expected = 'Inconclusive'

        self.assertEqual(expected, actual)

    def test_complex_psi(self):
        a = Predicate('a')
        a_lit = Literal(a)
        b = Predicate('b')
        cap_phi = PredicateStateFormula(a)
        cap_phi_comp = EvaluableNegationFormula(PredicateStateFormula(a))
        cap_delta = PredicateStateFormula(b)
        delta_ = EvaluableConjunctionFormula(cap_phi_comp, cap_delta)
        psi_ = NextPathFormula(delta_)
        phi_ = StatePathFormula(cap_phi)
        phi = UntilPathFormula(phi_, psi_)

        state0 = frozenset({a_lit})
        s0 = Situation(state0)

        t = SimpleTestCausalSetting()

        p = Path(s0)
        p.expand(t)
        p.expand(t)
        p.expand(t)

        actual = phi.evaluate(p)
        expected = True

        self.assertEqual(expected, actual)

    def test_complex_unexpanded0(self):
        a = Predicate('a')
        a_lit = Literal(a)
        b = Predicate('b')
        b_lit = Literal(b)
        cap_phi = PredicateStateFormula(a)
        cap_phi_comp = EvaluableNegationFormula(PredicateStateFormula(a))
        cap_delta = PredicateStateFormula(b)
        cap_delta_comp = EvaluableNegationFormula(PredicateStateFormula(b))
        psi_ = EvaluableDisjunctionFormula(cap_phi_comp, cap_delta_comp)
        phi_ = EvaluableConjunctionFormula(cap_phi, cap_delta)
        phi = UntilPathFormula(phi_, psi_)

        state0 = frozenset({a_lit, b_lit})
        s0 = Situation(state0)

        p = Path(s0)

        actual = phi.evaluate(p)
        expected = 'Inconclusive'

        self.assertEqual(expected, actual)

    def test_complex_unexpanded1(self):
        a = Predicate('a')
        a_lit = Literal(a)
        b = Predicate('b')
        b_lit = Literal(b)
        cap_phi = PredicateStateFormula(a)
        cap_phi_comp = EvaluableNegationFormula(PredicateStateFormula(a))
        cap_delta = PredicateStateFormula(b)
        cap_delta_comp = EvaluableNegationFormula(PredicateStateFormula(b))
        psi_ = EvaluableDisjunctionFormula(cap_phi_comp, cap_delta_comp)
        phi_ = EvaluableConjunctionFormula(cap_phi, cap_delta)
        phi = UntilPathFormula(phi_, psi_)

        state0 = frozenset({a_lit, b_lit})
        s0 = Situation(state0)

        t = SimpleTestCausalSetting()

        p = Path(s0)
        p.expand(t)

        actual = phi.evaluate(p)
        expected = 'Inconclusive'

        self.assertEqual(expected, actual)

    def test_complex_phi(self):
        a = Predicate('a')
        a_lit = Literal(a)
        b = Predicate('b')
        b_lit = Literal(b)
        cap_phi = PredicateStateFormula(a)
        cap_phi_comp = EvaluableNegationFormula(PredicateStateFormula(a))
        cap_delta = PredicateStateFormula(b)
        cap_delta_comp = EvaluableNegationFormula(PredicateStateFormula(b))
        psi_ = EvaluableDisjunctionFormula(cap_phi_comp, cap_delta_comp)
        phi_ = EvaluableConjunctionFormula(cap_phi, cap_delta)
        phi = UntilPathFormula(phi_, psi_)

        state0 = frozenset({a_lit, b_lit})
        s0 = Situation(state0)

        t = SimpleTestCausalSetting()

        p = Path(s0)
        p.expand(t)
        p.expand(t)

        actual = phi.evaluate(p)
        expected = True

        self.assertEqual(expected, actual)

    def test_inconclusive_phi(self):
        a = Predicate('a')
        a_lit = Literal(a)
        b = Predicate('b')
        b_lit = Literal(b)
        cap_phi = PredicateStateFormula(a)
        cap_phi_comp = EvaluableNegationFormula(PredicateStateFormula(a))
        cap_delta = PredicateStateFormula(b)
        cap_delta_comp = EvaluableNegationFormula(PredicateStateFormula(b))
        phi_ = NextPathFormula(EvaluableConjunctionFormula(cap_phi, cap_delta))
        psi_ = StatePathFormula(cap_delta)
        phi = UntilPathFormula(phi_, psi_)

        state0 = frozenset({a_lit})
        s0 = Situation(state0)

        t = SimpleTestCausalSetting()

        p = Path(s0)
        p.expand(t)

        actual = phi.evaluate(p)
        expected = 'Inconclusive'

        self.assertEqual(expected, actual)
