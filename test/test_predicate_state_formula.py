# noinspection DuplicatedCode
import unittest

from scpy.formula.state_formula.predicate_state_formula import PredicateStateFormula
from scpy.literal import Literal
from scpy.predicate import Predicate


class TestConstructor(unittest.TestCase):

    def test_create_simple(self):
        """

        :return:
        """
        a = Predicate('a')
        a_lit = Literal(a)
        phi = PredicateStateFormula(a_lit)
        expected = 'a'
        actual = phi.literal.predicate.functor
        self.assertEqual(expected, actual)
