# noinspection DuplicatedCode
import unittest

from scpy.primitives import Literal, Predicate


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
