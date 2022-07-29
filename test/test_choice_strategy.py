# noinspection DuplicatedCode
import unittest

from scpy.action.action import Action
from scpy.formula.special_formula import NegationFormula, TrueFormula
from scpy.formula.state_formula.predicate_state_formula import PredicateStateFormula
from scpy.function.function import Function
from scpy.predicate.predicate import Predicate
from scpy.strategy.choice_strategy import ChoiceStrategy
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
        cond_1 = PredicateStateFormula(a_pred)
        cond_2 = NegationFormula(PredicateStateFormula(a_pred))

        strat1 = PreconditionalActionStrategy(cond_1, add_b)
        strat2 = PreconditionalActionStrategy(cond_2, add_a)

        strat = ChoiceStrategy(strat1, strat2)


class TestAllApplicableActions(unittest.TestCase):

    def test_simple(self):
        a_pred = Predicate('a')

        cond_1 = PredicateStateFormula(a_pred)
        cond_2 = NegationFormula(PredicateStateFormula(a_pred))

        strat1 = PreconditionalActionStrategy(cond_1, add_b)
        strat2 = PreconditionalActionStrategy(cond_2, add_a)

        strat = ChoiceStrategy(strat1, strat2)

        state0 = frozenset({})

        t = SimpleTestCausalSetting()

        actual = set(strat.all_applicable_actions(t, state0))
        expected = {add_a}

        self.assertSetEqual(expected, actual)

    def test_nested(self):
        strat1 = PreconditionalActionStrategy(TrueFormula(), add_a)
        strat2 = PreconditionalActionStrategy(TrueFormula(), add_b)
        strat3 = PreconditionalActionStrategy(TrueFormula(), remove_a)
        strat4 = PreconditionalActionStrategy(TrueFormula(), remove_b)

        strat_add = ChoiceStrategy(strat1, strat2)
        strat_remove = ChoiceStrategy(strat3, strat4)

        strat = ChoiceStrategy(strat_add, strat_remove)

        state0 = frozenset({})

        t = SimpleTestCausalSetting()

        actual = set(strat.all_applicable_actions(t, state0))
        expected = {add_a, add_b}

        self.assertSetEqual(expected, actual)
