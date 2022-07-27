# noinspection DuplicatedCode
import unittest

from scpy.causal_setting.game_causal_setting import GameCausalSetting
from scpy.causal_setting.nim_causal_setting import NimCausalSetting
from scpy.function import Function
from scpy.literal import Literal
from scpy.path import Path
from scpy.situation import Situation


class TestConstructor(unittest.TestCase):

    def test_create_simple(self):
        t = NimCausalSetting()


class TestPoss(unittest.TestCase):

    def test_simple(self):
        t = NimCausalSetting()
        state = frozenset((Literal(NimCausalSetting.stones(7)), Literal(GameCausalSetting.control(0))))
        s0 = Situation(state)
        actual = t.poss(t.tick(0, NimCausalSetting.take(1)), s0)
        expected = True
        self.assertEqual(expected, actual)

    def test_not_enough(self):
        t = NimCausalSetting()
        state = frozenset((Literal(NimCausalSetting.stones(7)), Literal(GameCausalSetting.control(0))))
        s0 = Situation(state)
        actual = t.poss(t.tick(0, NimCausalSetting.take(0)), s0)
        expected = False
        self.assertEqual(expected, actual)

    def test_more_than_stones(self):
        t = NimCausalSetting()
        state = frozenset((Literal(NimCausalSetting.stones(2)), Literal(GameCausalSetting.control(0))))
        s0 = Situation(state)
        actual = t.poss(t.tick(0, NimCausalSetting.take(3)), s0)
        expected = False
        self.assertEqual(expected, actual)

    def test_too_much(self):
        t = NimCausalSetting()
        state = frozenset((Literal(NimCausalSetting.stones(7)), Literal(GameCausalSetting.control(0))))
        s0 = Situation(state)
        actual = t.poss(t.tick(0, NimCausalSetting.take(4)), s0)
        expected = False
        self.assertEqual(expected, actual)

    def test_double_noop(self):
        t = NimCausalSetting()
        state = frozenset((Literal(NimCausalSetting.stones(7)), Literal(GameCausalSetting.control(0))))
        s0 = Situation(state)
        actual = t.poss(Function('tick', (GameCausalSetting.noop(), GameCausalSetting.noop())), s0)
        expected = False
        self.assertEqual(expected, actual)

    def test_double_take(self):
        t = NimCausalSetting()
        state = frozenset((Literal(NimCausalSetting.stones(7)), Literal(GameCausalSetting.control(0))))
        s0 = Situation(state)
        actual = t.poss(Function('tick', (NimCausalSetting.take(2), NimCausalSetting.take(3))), s0)
        expected = False
        self.assertEqual(expected, actual)

    def test_reversed_move_1(self):
        t = NimCausalSetting()
        state = frozenset((Literal(NimCausalSetting.stones(7)), Literal(GameCausalSetting.control(0))))
        s0 = Situation(state)
        actual = t.poss(t.tick(1, NimCausalSetting.take(2)), s0)
        expected = False
        self.assertEqual(expected, actual)

    def test_reversed_move_2(self):
        t = NimCausalSetting()
        state = frozenset((Literal(NimCausalSetting.stones(7)), Literal(GameCausalSetting.control(1))))
        s0 = Situation(state)
        actual = t.poss(t.tick(0, NimCausalSetting.take(2)), s0)
        expected = False
        self.assertEqual(expected, actual)

    def test_not_enough_noop(self):
        t = NimCausalSetting()
        state = frozenset((Literal(NimCausalSetting.stones(7)), Literal(GameCausalSetting.control(0))))
        s0 = Situation(state)
        actual = t.poss(Function('tick', (NimCausalSetting.take(2),)), s0)
        expected = False
        self.assertEqual(expected, actual)

    def test_too_many_noop(self):
        t = NimCausalSetting()
        state = frozenset((Literal(NimCausalSetting.stones(7)), Literal(GameCausalSetting.control(0))))
        s0 = Situation(state)
        actual = t.poss(
            Function('tick', (GameCausalSetting.noop(), GameCausalSetting.noop(), GameCausalSetting.noop())), s0)
        expected = False
        self.assertEqual(expected, actual)


class TestDo(unittest.TestCase):

    def test_simple(self):
        t = NimCausalSetting()
        state = frozenset((Literal(NimCausalSetting.stones(7)), Literal(GameCausalSetting.control(0))))
        s0 = Situation(state)
        action = t.tick(0, NimCausalSetting.take(3))
        s1 = t.do(action, s0)
        expected = frozenset(
            (-Literal(NimCausalSetting.stones(7)),
             Literal(NimCausalSetting.stones(4)),
             -Literal(GameCausalSetting.control(0)),
             Literal(GameCausalSetting.control(1))))
        actual = s1.state
        self.assertSetEqual(expected, actual)
        expected = action
        actual = s1.previous_action
        self.assertEqual(expected, actual)
        expected = s0
        actual = s1.previous_situation
        self.assertEqual(expected, actual)

    def test_full(self):
        t = NimCausalSetting()
        state = frozenset((Literal(NimCausalSetting.stones(7)), Literal(GameCausalSetting.control(0))))
        s0 = Situation(state)
        action1 = t.tick(0, NimCausalSetting.take(3))
        s1 = t.do(action1, s0)
        action2 = t.tick(1, NimCausalSetting.take(3))
        s2 = t.do(action2, s1)
        action3 = t.tick(0, NimCausalSetting.take(1))
        s3 = t.do(action3, s2)
        expected = frozenset(
            (-Literal(NimCausalSetting.stones(7)),
             -Literal(NimCausalSetting.stones(4)),
             -Literal(NimCausalSetting.stones(1)),
             Literal(NimCausalSetting.stones(0)),
             -Literal(GameCausalSetting.control(0)),
             Literal(GameCausalSetting.control(1))))
        actual = s3.state
        self.assertSetEqual(expected, actual)
        expected = action3
        actual = s3.previous_action
        self.assertEqual(expected, actual)
        expected = s2
        actual = s3.previous_situation
        self.assertEqual(expected, actual)


class TestAllPossActions(unittest.TestCase):

    def test_simple(self):
        t = NimCausalSetting()
        state = frozenset((Literal(NimCausalSetting.stones(7)), Literal(GameCausalSetting.control(0))))
        s0 = Situation(state)
        actual = set(t.all_poss_actions(s0))
        expected = {
            t.tick(0, NimCausalSetting.take(1)),
            t.tick(0, NimCausalSetting.take(2)),
            t.tick(0, NimCausalSetting.take(3)),
        }
        self.assertSetEqual(expected, actual)

class TestWithPaths(unittest.TestCase):

    def test_simple(self):
        t = NimCausalSetting()
        state = frozenset((Literal(NimCausalSetting.stones(7)), Literal(GameCausalSetting.control(0))))
        s0 = Situation(state)
        p = Path(s0)
        p.expand(t)
        p.expand(t)
        expected = 3
        actual = len(p.traces)
        self.assertEqual(expected, actual)