# noinspection DuplicatedCode
import unittest

from scpy.situation import Situation


class TestConstructor(unittest.TestCase):

    def test_create_simple(self):
        """

        :return:
        """
        s = Situation()
        expected = frozenset()
        actual = s.state
        self.assertEqual(expected, actual)
        self.assertIsNone(s.previous_action)
        self.assertIsNone(s.previous_situation)
