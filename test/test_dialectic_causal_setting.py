# noinspection DuplicatedCode
import unittest

from frozendict import frozendict

from scpy.causal_setting.dialectic_causal_setting import DialecticCausalSetting, consolidate_action
from scpy.preorder import MutablePreorder, Preorder
from scpy.situation.situation import Situation
from test.test_dialectic_causal_setting_instances import MilkCausalSetting, need_l, money_p, buy_p, asks_p, \
    need_p, position_need_l, position_need_f, position_compl_need_f, position_compl_need_l, fact_need, \
    supports_fact_need_need, argument_fact_need_need_l, money_l, position_compl_buy_f, position_compl_buy_l, buy_l, \
    necc_p_compl_money_compl_buy, supports_necc_p_compl_money_compl_buy_compl_buy, \
    argument_necc_p_compl_money_compl_buy_compl_buy_l, supports_fact_compl_money_compl_money_f, \
    argument_fact_compl_money_l, \
    fact_compl_money, suff_p_need_buy, hyp_need, hyp_compl_need, hyp_buy, hyp_compl_buy, attacks_hyp_buy_compl_buy_f, \
    attacks_hyp_buy_compl_buy_l, attacks_suff_p_need_buy_compl_buy_l, attacks_suff_p_need_buy_compl_buy_f, \
    supports_fact_need_need_l, fact_compl_buy, fact_buy, position_buy_f, position_buy_l, supports_suff_p_need_buy_buy_f, \
    argument_suff_p_need_buy_buy_l, attacks_necc_p_compl_money_comply_buy_buy_f, \
    attacks_necc_p_compl_money_compl_buy_buy_l, supports_fact_compl_money_compl_money_l, defends_hyp_money_money_f, \
    defends_hyp_money_money_l, hyp_money, hyp_compl_money, supports_hyp_compl_money_compl_money_l, \
    supports_hyp_compl_money_compl_money_f, counterargument_suff_p_need_buy_buy_l, counterargument_fact_need_need_l, \
    counterargument_necc_p_compl_money_compl_buy_compl_buy_l, counterargument_hyp_compl_money_compl_money_l, \
    argument_hyp_money_money_l

fact_set = frozenset({need_l, -money_l})
awareness_set = frozenset({need_p, asks_p, buy_p, money_p})
argument_scheme = frozendict({
    fact_need: (frozenset(), frozenset({need_l})),
    fact_compl_money: (frozenset(), frozenset({-money_l})),
    hyp_need: (frozenset(), frozenset({need_l})),
    hyp_compl_need: (frozenset(), frozenset({-need_l})),
    hyp_buy: (frozenset(), frozenset({buy_l})),
    hyp_compl_buy: (frozenset(), frozenset({-buy_l})),
    hyp_money: (frozenset(), frozenset({money_l})),
    hyp_compl_money: (frozenset(), frozenset({-money_l})),
    necc_p_compl_money_compl_buy: (frozenset({-money_l}), frozenset({-buy_l})),
    suff_p_need_buy: (frozenset({need_l}), frozenset({buy_l})),
})
strength_preorder_ = MutablePreorder()
strength_preorder_.precedes(suff_p_need_buy, necc_p_compl_money_compl_buy)
strength_preorder_.precedes(necc_p_compl_money_compl_buy, fact_buy)
strength_preorder_.precedes(suff_p_need_buy, fact_buy)
strength_preorder_.precedes(suff_p_need_buy, fact_compl_buy)
strength_preorder_.precedes(hyp_buy, fact_compl_buy)
strength_preorder_.precedes(hyp_compl_buy, fact_buy)
strength_preorder_.precedes(hyp_buy, hyp_money)
strength_preorder_.precedes(hyp_money, hyp_buy)
strength_preorder_.precedes(hyp_money, hyp_compl_money)
strength_preorder_.precedes(hyp_compl_money, hyp_money)
strength_preorder = Preorder(strength_preorder_)
s0 = Situation(frozenset())


# noinspection DuplicatedCode
class TestConstructor(unittest.TestCase):

    def test_base(self):
        t = DialecticCausalSetting()

    def test_milk(self):
        t = MilkCausalSetting(fact_set=frozenset({need_l}))


# noinspection DuplicatedCode
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

    def test_milk_alt_initial_buy(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set)

        s1 = t.do(position_buy_f, s0)

        expected = {position_buy_l}
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

    def test_milk_alt_supports_suff_p_need_buy_buy(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              argument_scheme=argument_scheme)

        s1 = Situation(frozenset({position_buy_l}))
        s2 = t.do(supports_suff_p_need_buy_buy_f, s1)

        expected = {position_buy_l,
                    argument_suff_p_need_buy_buy_l}
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
        s3 = t.do(supports_fact_compl_money_compl_money_f, s2)

        expected = {position_compl_buy_l, argument_necc_p_compl_money_compl_buy_compl_buy_l,
                    argument_fact_compl_money_l}
        actual = set(s3.state)

        self.assertSetEqual(expected, actual)

    def test_milk_alt_supports_fact_need_need(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              argument_scheme=argument_scheme)

        s2 = Situation(frozenset({position_buy_l, argument_suff_p_need_buy_buy_l}))
        s3 = t.do(supports_fact_need_need, s2)

        expected = {position_buy_l,
                    argument_suff_p_need_buy_buy_l,
                    argument_fact_need_need_l}
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

    def test_milk_alt_attacks_necc_p_compl_money_compl_buy_buy(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              argument_scheme=argument_scheme)

        s3 = Situation(frozenset({position_buy_l,
                                  argument_suff_p_need_buy_buy_l,
                                  argument_fact_need_need_l}))
        s4 = t.do(attacks_necc_p_compl_money_comply_buy_buy_f, s3)

        expected = {position_buy_l,
                    argument_suff_p_need_buy_buy_l,
                    argument_fact_need_need_l,
                    attacks_necc_p_compl_money_compl_buy_buy_l}
        actual = set(s4.state)

        self.assertSetEqual(expected, actual)

    def test_milk_attacks_suff_p_need_buy_compl_buy(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              argument_scheme=argument_scheme)
        s3 = Situation(frozenset({
            position_compl_buy_l,
            argument_necc_p_compl_money_compl_buy_compl_buy_l,
            argument_fact_compl_money_l}))
        s4 = t.do(attacks_suff_p_need_buy_compl_buy_f, s3)

        expected = {
            position_compl_buy_l,
            argument_necc_p_compl_money_compl_buy_compl_buy_l,
            argument_fact_compl_money_l,
            attacks_suff_p_need_buy_compl_buy_l}
        actual = set(s4.state)

        self.assertSetEqual(expected, actual)

    def test_milk_alt_supports_fact_compl_money_compl_money(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              argument_scheme=argument_scheme,
                              strength_preorder=strength_preorder)
        s4 = Situation(frozenset({position_buy_l,
                                  argument_suff_p_need_buy_buy_l,
                                  argument_fact_need_need_l,
                                  attacks_necc_p_compl_money_compl_buy_buy_l}))
        s5 = t.do(supports_hyp_compl_money_compl_money_f, s4)

        expected = {position_buy_l,
                    argument_suff_p_need_buy_buy_l,
                    argument_fact_need_need_l,
                    attacks_necc_p_compl_money_compl_buy_buy_l,
                    supports_hyp_compl_money_compl_money_l}
        actual = set(s5.state)

        self.assertSetEqual(expected, actual)

    def test_milk_supports_fact_need_need(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              argument_scheme=argument_scheme)
        s4 = Situation(frozenset({
            position_compl_buy_l,
            argument_necc_p_compl_money_compl_buy_compl_buy_l,
            argument_fact_compl_money_l,
            attacks_suff_p_need_buy_compl_buy_l}))
        s5 = t.do(supports_fact_need_need, s4)

        expected = {
            position_compl_buy_l,
            argument_necc_p_compl_money_compl_buy_compl_buy_l,
            argument_fact_compl_money_l,
            attacks_suff_p_need_buy_compl_buy_l,
            supports_fact_need_need_l,
        }
        actual = set(s5.state)

        self.assertSetEqual(expected, actual)

    def test_milk_alt_defends_hyp_money_money(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              argument_scheme=argument_scheme,
                              strength_preorder=strength_preorder)

        s5 = Situation(frozenset({position_buy_l,
                                  argument_suff_p_need_buy_buy_l,
                                  argument_fact_need_need_l,
                                  attacks_necc_p_compl_money_compl_buy_buy_l,
                                  supports_hyp_compl_money_compl_money_l}))
        s6 = t.do(defends_hyp_money_money_f, s5)

        expected = {position_buy_l,
                    argument_suff_p_need_buy_buy_l,
                    argument_fact_need_need_l,
                    attacks_necc_p_compl_money_compl_buy_buy_l,
                    supports_hyp_compl_money_compl_money_l,
                    defends_hyp_money_money_l}
        actual = set(s6.state)

        self.assertSetEqual(expected, actual)

    def test_milk_simple_consolidate(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              argument_scheme=argument_scheme)

        s2 = Situation(frozenset({position_need_l, argument_fact_need_need_l}))
        s3 = t.do(consolidate_action, s2)

        expected = {position_need_l, argument_fact_need_need_l}
        actual = set(s3.state)

        self.assertSetEqual(expected, actual)

    def test_milk_consolidate(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              argument_scheme=argument_scheme)

        s5 = Situation(frozenset({
            position_compl_buy_l,
            argument_necc_p_compl_money_compl_buy_compl_buy_l,
            argument_fact_compl_money_l,
            attacks_suff_p_need_buy_compl_buy_l,
            supports_fact_need_need_l,
        }))
        s6 = t.do(consolidate_action, s5)

        expected = {
            position_compl_buy_l,
            argument_necc_p_compl_money_compl_buy_compl_buy_l,
            argument_fact_compl_money_l,
            counterargument_suff_p_need_buy_buy_l,
            counterargument_fact_need_need_l,
        }

        actual = set(s6.state)

        self.assertSetEqual(expected, actual)

    def test_milk_alt_consolidate(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              argument_scheme=argument_scheme)
        s6 = Situation(frozenset({position_buy_l,
                                  argument_suff_p_need_buy_buy_l,
                                  argument_fact_need_need_l,
                                  attacks_necc_p_compl_money_compl_buy_buy_l,
                                  supports_hyp_compl_money_compl_money_l,
                                  defends_hyp_money_money_l}))
        s7 = t.do(consolidate_action, s6)

        expected = {position_buy_l,
                    argument_suff_p_need_buy_buy_l,
                    argument_fact_need_need_l,
                    counterargument_necc_p_compl_money_compl_buy_compl_buy_l,
                    counterargument_hyp_compl_money_compl_money_l,
                    argument_hyp_money_money_l}
        actual = set(s7.state)

        self.assertSetEqual(expected, actual)


# noinspection DuplicatedCode
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


# noinspection DuplicatedCode
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
                    hyp_buy: {-buy_l},
                    hyp_money: {-money_l}}
        actual = t.attacks(s3.state)

        self.assertDictEqual(expected, actual)


# noinspection DuplicatedCode
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
        actual = t.incomplete_reasoning(s4.state)

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
        actual = t.incomplete_reasoning(s4.state)

        self.assertDictEqual(expected, actual)


# noinspection DuplicatedCode
class TestUndefendedAttacks(unittest.TestCase):

    def test_milk_attacks_hyp_buy_compl_buy(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              argument_scheme=argument_scheme,
                              strength_preorder=strength_preorder)
        s4 = Situation(frozenset({
            position_compl_buy_l,
            argument_necc_p_compl_money_compl_buy_compl_buy_l,
            argument_fact_compl_money_l,
            attacks_hyp_buy_compl_buy_l}))

        expected = {
            hyp_buy: {buy_l}
        }
        actual = t.undefended_attacks(s4.state)

        self.assertDictEqual(expected, actual)

    def test_milk_attacks_suff_p_needs_buy_compl_buy(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              argument_scheme=argument_scheme)
        s5 = Situation(frozenset({
            position_compl_buy_l,
            argument_necc_p_compl_money_compl_buy_compl_buy_l,
            argument_fact_compl_money_l,
            attacks_suff_p_need_buy_compl_buy_l,
            supports_fact_need_need_l,
        }))

        expected = {
            suff_p_need_buy: {buy_l},
            fact_need: {need_l}
        }
        actual = t.undefended_attacks(s5.state)

        self.assertDictEqual(expected, actual)

    def test_milk_alt_attacks_necc_p_compl_money_compl_buy_buy_l(self):
        t = MilkCausalSetting(fact_set=fact_set,
                              awareness_set=awareness_set,
                              argument_scheme=argument_scheme,
                              strength_preorder=strength_preorder)

        s5 = Situation(frozenset({position_buy_l,
                                  argument_suff_p_need_buy_buy_l,
                                  argument_fact_need_need_l,
                                  attacks_necc_p_compl_money_compl_buy_buy_l,
                                  supports_fact_compl_money_compl_money_l}))

        expected = {
            necc_p_compl_money_compl_buy: {-buy_l},
            fact_compl_money: {-money_l}
        }
        actual = t.undefended_attacks(s5.state)

        self.assertDictEqual(expected, actual)
