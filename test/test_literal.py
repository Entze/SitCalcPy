# noinspection DuplicatedCode
import unittest

from scpy.literal import Literal
from scpy.predicate import Predicate


class TestConstructor(unittest.TestCase):

    def test_create_simple(self):
        """

        :return:
        """
        a = Predicate('a')
        a_lit = Literal(a)
        expected = 'a'
        actual = a_lit.predicate.functor
        self.assertEqual(expected, actual)
