# noinspection DuplicatedCode
import unittest

from scpy.primitives import Function
from scpy.preorder import MutablePreorder, Preorder


class TestConstructor(unittest.TestCase):

    def test_from_mutable_to_immutable(self):

        a = Function('a')
        b = Function('b')
        c = Function('c')

        p = MutablePreorder()

        p.precedes(a, b)
        p.precedes(a, c)
        p.precedes(b, c)
        p.precedes(c, b)

        i = Preorder(p)

        for e in (a, b, c):
            for f in (a, b, c):
                expected = p.is_preceded(e, f)
                actual = i.is_preceded(e, f)
                self.assertEqual(expected, actual)

        for e in (a, b, c):
            for f in (a, b, c):
                expected = p.is_similar(e, f)
                actual = i.is_similar(e, f)
                self.assertEqual(expected, actual)

        for e in (a, b, c):
            for f in (a, b, c):
                expected = p.is_strictly_preceded(e, f)
                actual = i.is_strictly_preceded(e, f)
                self.assertEqual(expected, actual)

    def test_from_mutable_to_mutable(self):

        a = Function('a')
        b = Function('b')
        c = Function('c')

        p = MutablePreorder()

        p.precedes(a, b)
        p.precedes(a, c)
        p.precedes(b, c)
        p.precedes(c, b)

        q = MutablePreorder(p)

        for e in (a, b, c):
            for f in (a, b, c):
                expected = p.is_preceded(e, f)
                actual = q.is_preceded(e, f)
                self.assertEqual(expected, actual)

        for e in (a, b, c):
            for f in (a, b, c):
                expected = p.is_similar(e, f)
                actual = q.is_similar(e, f)
                self.assertEqual(expected, actual)

        for e in (a, b, c):
            for f in (a, b, c):
                expected = p.is_strictly_preceded(e, f)
                actual = q.is_strictly_preceded(e, f)
                self.assertEqual(expected, actual)


class TestPrecedes(unittest.TestCase):

    def test_adding_two(self):
        a = Function('a')
        b = Function('b')

        p = MutablePreorder()

        p.precedes(a, b)
        expected = True
        actual = p.is_preceded(a, b)

        self.assertEqual(expected, actual)

    def test_adding_three(self):
        a = Function('a')
        b = Function('b')
        c = Function('c')

        p = MutablePreorder()

        p.precedes(a, b)
        p.precedes(a, c)
        p.precedes(b, c)
        p.precedes(c, b)

        expected = True
        actual = p.is_similar(b, c)

        self.assertEqual(expected, actual)
