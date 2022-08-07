# noinspection DuplicatedCode
import unittest

from scpy.primitives import Function


class TestConstructor(unittest.TestCase):

    def test_create_simple(self):
        """

        :return:
        """
        a = Function('a')
        actual = a.symbol
        expected = 'a'
        self.assertEqual(expected, actual)
