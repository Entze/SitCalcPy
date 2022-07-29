# noinspection DuplicatedCode
import unittest

from scpy.predicate.predicate import Predicate


class TestConstructor(unittest.TestCase):

    def test_create_simple(self):
        """

        :return:
        """
        a = Predicate('a')
        actual = a.functor
        expected = 'a'
        self.assertEqual(expected, actual)
