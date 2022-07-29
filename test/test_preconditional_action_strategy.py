# noinspection DuplicatedCode
import unittest

from scpy.action.action import Action
from scpy.formula.state_formula.predicate_state_formula import PredicateStateFormula
from scpy.function.function import Function
from scpy.literal.literal import Literal
from scpy.predicate.predicate import Predicate
from scpy.strategy.preconditional_action_strategy import PreconditionalActionStrategy
from test.simple_test_causal_setting import SimpleTestCausalSetting

a = Function('a')
b = Function('b')
add_a: Action = Function('add', (a,))
add_b: Action = Function('add', (b,))
remove_a: Action = Function('remove', (a,))
remove_b: Action = Function('remove', (b,))


class TestConstructor(unittest.TestCase):

    def test_create_simple(self):
        a_pred = Predicate('a')
        cond = PredicateStateFormula(a_pred)

        strat = PreconditionalActionStrategy(cond, remove_a)


class TestAllApplicableActions(unittest.TestCase):

    def test_simple(self):
        a_pred = Predicate('a')
        a_lit = Literal(a_pred)
        state0 = frozenset({a_lit})

        cond = PredicateStateFormula(a_pred)

        strat = PreconditionalActionStrategy(cond, remove_a)

        t = SimpleTestCausalSetting()

        actual = set(strat.all_applicable_actions(t, state0))
        expected = {remove_a}
        self.assertSetEqual(expected, actual)

    def test_simple_empty(self):
        a_pred = Predicate('a')
        a_lit = Literal(a_pred)
        state0 = frozenset({-a_lit})

        cond = PredicateStateFormula(a_pred)

        strat = PreconditionalActionStrategy(cond, remove_a)

        t = SimpleTestCausalSetting()

        actual = set(strat.all_applicable_actions(t, state0))
        expected = set()
        self.assertSetEqual(expected, actual)
