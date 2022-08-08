# noinspection DuplicatedCode
import unittest

from frozendict import frozendict

from scpy.causal_setting.dialectic_causal_setting import DialecticCausalSetting
from scpy.situation.situation import Situation
from test.simple_test_dialectic_causal_setting import MilkCausalSetting, need_l, money_p, buy_p, asks_p, \
    need_p, position_need_l, position_need_f, position_compl_need_f, position_compl_need_l, fact_need, \
    supports_fact_need_need, argument_fact_need_need_l, money_l, position_compl_buy_f, position_compl_buy_l, buy_l, \
    necc_p_compl_money_compl_buy, supports_necc_p_compl_money_compl_buy_compl_buy, \
    argument_necc_p_compl_money_compl_buy_compl_buy_l, supports_fact_compl_money_compl_money, \
    argument_fact_compl_money_l, \
    fact_compl_money, suff_p_need_buy, hyp_need, hyp_compl_need, hyp_buy, hyp_compl_buy, attacks_hyp_buy_compl_buy_f, \
    attacks_hyp_buy_compl_buy_l, attacks_suff_p_need_buy_compl_buy_l

fact_set = frozenset({need_l, -money_l})
awareness_set = frozenset({need_p, asks_p, buy_p, money_p})
argument_scheme = frozendict({
    fact_need: (frozenset(), frozenset({need_l})),
    fact_compl_money: (frozenset(), frozenset({-money_l})),
    hyp_need: (frozenset(), frozenset({need_l})),
    hyp_compl_need: (frozenset(), frozenset({-need_l})),
    hyp_buy: (frozenset(), frozenset({buy_l})),
    hyp_compl_buy: (frozenset(), frozenset({-buy_l})),
    necc_p_compl_money_compl_buy: (frozenset({-money_l}), frozenset({-buy_l})),
    suff_p_need_buy: (frozenset({need_l}), frozenset({buy_l})),
})
s0 = Situation(frozenset())


class TestConstructor(unittest.TestCase):

    def test_base(self):
        t = DialecticCausalSetting()

    def test_milk(self):
        t = MilkCausalSetting(fact_set=frozenset({need_l}))


class TestDo(unittest.TestCase):

    def test_milk_simple_initial_do_need(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set)

        s1 = t.do(position_need_f, s0)

        expected = {position_need_l}
        actual = set(s1.state)

        self.assertSetEqual(expected, actual)

    def test_milk_initial_compl_buy(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set)

        s1 = t.do(position_compl_buy_f, s0)

        expected = {position_compl_buy_l}
        actual = set(s1.state)

        self.assertSetEqual(expected, actual)

    def test_milk_simple_initial_do_compl_need(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set)
        s1 = t.do(position_compl_need_f, s0)

        expected = {position_compl_need_l}
        actual = set(s1.state)

        self.assertSetEqual(expected, actual)

    def test_milk_supports_necc_p_compl_money_compl_buy_compl_buy(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              argument_scheme=argument_scheme)

        s1 = Situation(frozenset({position_compl_buy_l}))
        s2 = t.do(supports_necc_p_compl_money_compl_buy_compl_buy, s1)

        expected = {position_compl_buy_l, argument_necc_p_compl_money_compl_buy_compl_buy_l}
        actual = set(s2.state)

        self.assertSetEqual(expected, actual)

    def test_milk_simple_supports_fact_need_need(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              argument_scheme=argument_scheme)
        s1 = Situation(frozenset({position_need_l}))
        s2 = t.do(supports_fact_need_need, s1)

        expected = {position_need_l, argument_fact_need_need_l}
        actual = set(s2.state)

        self.assertSetEqual(expected, actual)

    def test_milk_supports_fact_compl_money_compl_money(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              argument_scheme=argument_scheme)
        s2 = Situation(frozenset({position_compl_buy_l, argument_necc_p_compl_money_compl_buy_compl_buy_l}))
        s3 = t.do(supports_fact_compl_money_compl_money, s2)

        expected = {position_compl_buy_l, argument_necc_p_compl_money_compl_buy_compl_buy_l,
                    argument_fact_compl_money_l}
        actual = set(s3.state)

        self.assertSetEqual(expected, actual)

    def test_milk_attacks_hyp_buy_compl_buy(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              argument_scheme=argument_scheme)
        s3 = Situation(frozenset({
            position_compl_buy_l,
            argument_necc_p_compl_money_compl_buy_compl_buy_l,
            argument_fact_compl_money_l}))
        s4 = t.do(attacks_hyp_buy_compl_buy_f, s3)
        expected = {
            position_compl_buy_l,
            argument_necc_p_compl_money_compl_buy_compl_buy_l,
            argument_fact_compl_money_l,
            attacks_hyp_buy_compl_buy_l}
        actual = set(s4.state)

        self.assertSetEqual(expected, actual)


class TestIncomplete(unittest.TestCase):

    def test_milk_simple_position_need(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              )
        s1 = Situation(frozenset({position_need_l}))

        expected = {need_l: set()}
        actual = t.incomplete_arguments(s1.state)

        self.assertDictEqual(expected, actual)

    def test_milk_position_compl_buy(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set)

        s1 = Situation(frozenset({position_compl_buy_l}))

        expected = {-buy_l: set()}
        actual = t.incomplete_arguments(s1.state)

        self.assertDictEqual(expected, actual)

    def test_milk_simple_complete(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              )
        s2 = Situation(frozenset({position_need_l, argument_fact_need_need_l}))

        expected = {}
        actual = t.incomplete_arguments(s2.state)

        self.assertDictEqual(expected, actual)

    def test_milk_argument_necc_p_compl_money_compl_buy_compl_buy(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              argument_scheme=argument_scheme)
        s2 = Situation(frozenset({position_compl_buy_l, argument_necc_p_compl_money_compl_buy_compl_buy_l}))

        expected = {-buy_l: {-money_l}}
        actual = t.incomplete_arguments(s2.state)
        self.assertDictEqual(expected, actual)

    def test_milk_complete(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              argument_scheme=argument_scheme)

        s3 = Situation(
            frozenset(
                {position_compl_buy_l, argument_necc_p_compl_money_compl_buy_compl_buy_l, argument_fact_compl_money_l}))

        expected = {}
        actual = t.incomplete_arguments(s3.state)

        self.assertDictEqual(expected, actual)


class TestAttacks(unittest.TestCase):

    def test_milk_simple_attacks(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              argument_scheme=argument_scheme)
        s2 = Situation(frozenset({position_need_l, argument_fact_need_need_l}))

        expected = {hyp_compl_need: {need_l}}
        actual = t.attacks(s2.state)

        self.assertDictEqual(expected, actual)

    def test_milk_attacks(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              argument_scheme=argument_scheme)
        s3 = Situation(frozenset({
            position_compl_buy_l,
            argument_necc_p_compl_money_compl_buy_compl_buy_l,
            argument_fact_compl_money_l}))

        expected = {suff_p_need_buy: {-buy_l},
                    hyp_buy: {-buy_l}}
        actual = t.attacks(s3.state)

        self.assertDictEqual(expected, actual)


class TestIncompleteAttacks(unittest.TestCase):

    def test_milk_simple_incomplete_attacks(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              argument_scheme=argument_scheme)
        s4 = Situation(frozenset({
            position_compl_buy_l,
            argument_necc_p_compl_money_compl_buy_compl_buy_l,
            argument_fact_compl_money_l,
            attacks_hyp_buy_compl_buy_l}))

        expected = {}
        actual = t.incomplete_attacks(s4.state)

        self.assertDictEqual(expected, actual)

    def test_milk_incomplete_attacks(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              argument_scheme=argument_scheme)
        s4 = Situation(frozenset({
            position_compl_buy_l,
            argument_necc_p_compl_money_compl_buy_compl_buy_l,
            argument_fact_compl_money_l,
            attacks_suff_p_need_buy_compl_buy_l}))

        expected = {-buy_l: suff_p_need_buy}
        actual = t.incomplete_attacks(s4.state)

        self.assertDictEqual(expected, actual)
