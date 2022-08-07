# noinspection DuplicatedCode
import unittest

from frozendict import frozendict

from scpy.causal_setting.dialectic_causal_setting import DialecticCausalSetting
from scpy.situation.situation import Situation
from test.simple_test_dialectic_causal_setting import MilkCausalSetting, need_l, money_p, buy_p, asks_p, \
    need_p, position_need_l, position_need_f, position_need_compl_f, position_need_compl_l, fact_need, \
    supports_fact_need_need, argument_fact_need_l, money_l

fact_set = frozenset({need_l, -money_l})
awareness_set = frozenset({need_p, asks_p, buy_p, money_p})
argument_scheme = frozendict({
    fact_need: (frozenset(), frozenset({need_l}))
})
s0 = Situation(frozenset())


class TestConstructor(unittest.TestCase):

    def test_base(self):
        t = DialecticCausalSetting()

    def test_milk(self):
        t = MilkCausalSetting(fact_set=frozenset({need_l}))


class TestDo(unittest.TestCase):

    def test_simple_initial_do_need(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set)

        s1 = t.do(position_need_f, s0)

        expected = {position_need_l}
        actual = set(s1.state)

        self.assertSetEqual(expected, actual)

    def test_simple_initial_do_need_compl(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set)
        s1 = t.do(position_need_compl_f, s0)

        expected = {position_need_compl_l}
        actual = set(s1.state)

        self.assertSetEqual(expected, actual)

    def test_simple_supports_fact_need_need(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              argument_scheme=argument_scheme)
        s1 = Situation(frozenset({position_need_l}))
        s2 = t.do(supports_fact_need_need, s1)

        expected = {position_need_l, argument_fact_need_l}
        actual = set(s2.state)

        self.assertSetEqual(expected, actual)


class TestIncomplete(unittest.TestCase):

    def test_simple_position_need(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              )
        s1 = Situation(frozenset({position_need_l}))

        expected = {need_l: set()}
        actual = t.incomplete(s1.state)

        self.assertDictEqual(expected, actual)

    def test_simple_complete(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              )
        s2 = Situation(frozenset({position_need_l, argument_fact_need_l}))

        expected = {}
        actual = t.incomplete(s2.state)

        self.assertDictEqual(expected, actual)
