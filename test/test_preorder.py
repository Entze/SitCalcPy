# noinspection DuplicatedCode
import unittest

from parameterized import parameterized

from scpy.preorder import MutablePreorder, Preorder
from scpy.primitives import Function

a = Function('a')
b = Function('b')
c = Function('c')
d = Function('d')
e = Function('e')
f = Function('f')
g = Function('g')


# noinspection DuplicatedCode
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

    @parameterized.expand((
            (a, a, False),
            (a, b, True),
            (a, c, False),
            (b, a, False),
            (b, b, False),
            (b, c, True),
            (c, a, False),
            (c, b, False),
            (c, c, False),
    ))
    def test_from_tuples(self, left, right, expected):

        p = Preorder.from_tuples((a, b), (b, c))

        actual = p.is_preceded(left, right)

        self.assertEqual(expected, actual, f"{left} ≺ {right}" if expected else f"{left} ⊀ {right}")

    @parameterized.expand((
            (a, a, False),
            (a, b, True),
            (a, c, True),
            (b, a, False),
            (b, b, False),
            (b, c, True),
            (c, a, False),
            (c, b, False),
            (c, c, False),
    ))
    def test_from_tuples_transitivity(self, left, right, expected):

        p = Preorder.from_tuples((a, b), (b, c), transitivity=True)

        actual = p.is_preceded(left, right)

        self.assertEqual(expected, actual,
                         "Under transitivity: " f"{left} ≺ {right}" if expected else f"{left} ⊀ {right}")

    @parameterized.expand((
            (a, a, False),
            (a, b, True),
            (a, c, False),
            (b, a, True),
            (b, b, False),
            (b, c, True),
            (c, a, False),
            (c, b, True),
            (c, c, False),
    ))
    def test_from_tuples_symmetry(self, left, right, expected):

        p = Preorder.from_tuples((a, b), (b, c), symmetry=True)
        actual = p.is_preceded(left, right)

        self.assertEqual(expected, actual, "Under symmetry: " f"{left} ≺ {right}" if expected else f"{left} ⊀ {right}")

    @parameterized.expand((
            (a, a, True),
            (a, b, True),
            (a, c, False),
            (b, a, False),
            (b, b, True),
            (b, c, True),
            (c, a, False),
            (c, b, False),
            (c, c, True),
    ))
    def test_from_tuples_reflexivity(self, left, right, expected):

        p = Preorder.from_tuples((a, b), (b, c), reflexivity=True)

        actual = p.is_preceded(left, right)

        self.assertEqual(expected, actual,
                         "Under reflexivity: " f"{left} ≺ {right}" if expected else f"{left} ⊀ {right}")

    @parameterized.expand((
            (((a, b), (b, c)), a, a, True),
            (((a, b), (b, c)), a, b, True),
            (((a, b), (b, c)), a, c, True),
            (((a, b), (b, c)), b, a, True),
            (((a, b), (b, c)), b, b, True),
            (((a, b), (b, c)), b, c, True),
            (((a, b), (b, c)), c, a, True),
            (((a, b), (b, c)), c, b, True),
            (((a, b), (b, c)), c, c, True),
    ))
    def test_from_tuples_transitivity_symmetry(self, tuples, left, right, expected):

        p = Preorder.from_tuples(*tuples, transitivity=True, symmetry=True)
        actual = p.is_preceded(left, right)

        self.assertEqual(expected, actual,
                         "Under transitivity and symmetry: " f"{left} ≺ {right}" if expected else f"{left} ⊀ {right}")


# noinspection DuplicatedCode
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
        p = MutablePreorder()

        p.precedes(a, b)
        p.precedes(a, c)
        p.precedes(b, c)
        p.precedes(c, b)

        expected = True
        actual = p.is_similar(b, c)

        self.assertEqual(expected, actual)
