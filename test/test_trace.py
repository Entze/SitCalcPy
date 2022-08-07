# noinspection DuplicatedCode
import unittest

from scpy.primitives import Function, Literal, Predicate
from scpy.trace.trace import Trace

a = Literal(Predicate('a'))
b = Literal(Predicate('b'))
c = Literal(Predicate('c'))

act1 = Function('action', (1,))
act2 = Function('action', (2,))
act3 = Function('action', (3,))


class TestConstructor(unittest.TestCase):

    def test_empty(self):
        state0 = frozenset()
        trace = Trace((state0,))
        trace.invariant()

    def test_singleton(self):
        state0 = frozenset({a})
        trace = Trace((state0,))
        trace.invariant()

    def test_multiple(self):
        state0 = frozenset({a, b})
        state1 = frozenset({a, b, c})
        action1 = act1
        trace = Trace((state0, state1), (action1,))
        trace.invariant()


class TestSlice(unittest.TestCase):

    def test_nullslice(self):
        state0 = frozenset({a, b})
        state1 = frozenset({a, b, c})
        state2 = frozenset({})
        state3 = frozenset({a})
        action1 = act1
        action2 = act2
        action3 = act3
        trace = Trace((state0, state1, state2, state3), (action1, action2, action3))
        actual = trace.slice()
        expected = trace
        self.assertEqual(expected, actual)

    def test_from0(self):
        state0 = frozenset({a, b})
        state1 = frozenset({a, b, c})
        state2 = frozenset({})
        state3 = frozenset({a})
        action1 = act1
        action2 = act2
        action3 = act3
        trace = Trace((state0, state1, state2, state3), (action1, action2, action3))
        actual = trace.slice(from_index=0)
        expected = trace
        self.assertEqual(expected, actual)

    def test_to_end(self):
        state0 = frozenset({a, b})
        state1 = frozenset({a, b, c})
        state2 = frozenset({})
        state3 = frozenset({a})
        action1 = act1
        action2 = act2
        action3 = act3
        trace = Trace((state0, state1, state2, state3), (action1, action2, action3))
        actual = trace.slice(to_index=4)
        expected = trace
        self.assertEqual(expected, actual)

    def test_from0_to_end(self):
        state0 = frozenset({a, b})
        state1 = frozenset({a, b, c})
        state2 = frozenset({})
        state3 = frozenset({a})
        action1 = act1
        action2 = act2
        action3 = act3
        trace = Trace((state0, state1, state2, state3), (action1, action2, action3))
        actual = trace.slice(from_index=0, to_index=4)
        expected = trace
        self.assertEqual(expected, actual)

    def test_from1(self):
        state0 = frozenset({a, b})
        state1 = frozenset({a, b, c})
        state2 = frozenset({})
        state3 = frozenset({a})
        action1 = act1
        action2 = act2
        action3 = act3
        trace = Trace((state0, state1, state2, state3), (action1, action2, action3))
        actual = trace.slice(from_index=1)
        expected = Trace((state1, state2, state3), (action2, action3))
        self.assertEqual(expected, actual)

    def test_to_last(self):
        state0 = frozenset({a, b})
        state1 = frozenset({a, b, c})
        state2 = frozenset({})
        state3 = frozenset({a})
        action1 = act1
        action2 = act2
        action3 = act3
        trace = Trace((state0, state1, state2, state3), (action1, action2, action3))
        actual = trace.slice(to_index=-1)
        expected = Trace((state0, state1, state2), (action1, action2))
        self.assertEqual(expected, actual)

    def test_from1_to_last(self):
        state0 = frozenset({a, b})
        state1 = frozenset({a, b, c})
        state2 = frozenset({})
        state3 = frozenset({a})
        action1 = act1
        action2 = act2
        action3 = act3
        trace = Trace((state0, state1, state2, state3), (action1, action2, action3))
        actual = trace.slice(from_index=1, to_index=-1)
        expected = Trace((state1, state2), (action2,))
        self.assertEqual(expected, actual)
