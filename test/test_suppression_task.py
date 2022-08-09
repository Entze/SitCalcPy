import unittest

from scpy.causal_setting.dialectic_causal_setting import position_literal, suff_p, argument_literal, \
    supports_action, fact, attacks_action, necc_p, attacks_literal, hyp, supports_literal, consolidate_action, \
    counterargument_literal, defends_action, defends_literal
from scpy.situation.situation import Situation
from test.test_dialectic_causal_setting_instances import l, GroupI, e, GroupII, GroupIII, o, t


# noinspection DuplicatedCode
class TestGroupISheHasAnEssayToFinish(unittest.TestCase):

    def test_stays_in_library_1a(self):
        cs = GroupI(fact_set=frozenset({e}))
        s1 = Situation(frozenset({position_literal(l)}))
        s2 = cs.do(supports_action(suff_p(e, l), l), s1)

        expected = {
            position_literal(l),
            argument_literal(suff_p(e, l), l),
        }
        actual = set(s2.state)

        self.assertSetEqual(expected, actual)

    def test_stays_in_library_1b(self):
        cs = GroupI(fact_set=frozenset({e}))
        s2 = Situation(frozenset({
            position_literal(l),
            argument_literal(suff_p(e, l), l)}))
        s3 = cs.do(supports_action(fact(e), e), s2)

        expected = {
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(fact(e), e)
        }
        actual = set(s3.state)

        self.assertSetEqual(expected, actual)

    def test_stays_in_library_2a(self):
        cs = GroupI(fact_set=frozenset({e}))
        s3 = Situation(frozenset({
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(fact(e), e)
        }))
        s4 = cs.do(attacks_action(necc_p(-e, -l), l), s3)

        expected = {
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(fact(e), e),
            attacks_literal(necc_p(-e, -l), l),
        }
        actual = set(s4.state)

        self.assertSetEqual(expected, actual)

    def test_stays_in_library_2b(self):
        cs = GroupI(fact_set=frozenset({e}))
        s4 = Situation(frozenset({
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(fact(e), e),
            attacks_literal(necc_p(-e, -l), l),
        }))
        s5 = cs.do(supports_action(hyp(-e), -e), s4)

        expected = {
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(fact(e), e),
            attacks_literal(necc_p(-e, -l), l),
            supports_literal(hyp(-e), -e)
        }
        actual = set(s5.state)

        self.assertSetEqual(expected, actual)

    def test_stays_in_library_3(self):
        cs = GroupI(fact_set=frozenset({e}))
        s5 = Situation(frozenset({
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(fact(e), e),
            attacks_literal(necc_p(-e, -l), l),
            supports_literal(hyp(-e), -e)
        }))
        s6 = cs.do(defends_action(fact(e), e), s5)

        expected = {
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(fact(e), e),
            attacks_literal(necc_p(-e, -l), l),
            supports_literal(hyp(-e), -e),
            defends_literal(fact(e), e),
        }
        actual = set(s6.state)

        self.assertSetEqual(expected, actual)

    def test_stays_in_library_4(self):
        cs = GroupI(fact_set=frozenset({e}))
        s6 = Situation(frozenset({
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(fact(e), e),
            attacks_literal(necc_p(-e, -l), l),
            supports_literal(hyp(-e), -e),
            defends_literal(fact(e), e),
        }))
        s7 = cs.do(consolidate_action, s6)

        expected = {
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(fact(e), e),
            counterargument_literal(necc_p(-e, -l), -l),
            counterargument_literal(hyp(-e), -e),
        }
        actual = set(s7.state)

        self.assertSetEqual(expected, actual)

    def test_doesnt_stay_in_library_1a(self):
        cs = GroupI(fact_set=frozenset({e}))
        s1 = Situation(frozenset({position_literal(-l)}))
        s2 = cs.do(supports_action(necc_p(-e, -l), -l), s1)

        expected = {
            position_literal(-l),
            argument_literal(necc_p(-e, -l), -l),
        }
        actual = set(s2.state)

        self.assertSetEqual(expected, actual)

    def test_doesnt_stay_in_library_1b(self):
        cs = GroupI(fact_set=frozenset({e}))
        s2 = Situation(frozenset({
            position_literal(-l),
            argument_literal(necc_p(-e, -l), -l),
        }))
        s3 = cs.do(supports_action(hyp(-e), -e), s2)

        expected = {
            position_literal(-l),
            argument_literal(necc_p(-e, -l), -l),
            argument_literal(hyp(-e), -e)
        }
        actual = set(s3.state)

        self.assertSetEqual(expected, actual)

    def test_doesnt_stay_in_library_2(self):
        cs = GroupI(fact_set=frozenset({e}))
        s3 = Situation(frozenset({
            position_literal(-l),
            argument_literal(necc_p(-e, -l), -l),
            argument_literal(hyp(-e), -e)
        }))
        s4 = cs.do(attacks_action(fact(e), -e), s3)

        expected = {
            position_literal(-l),
            argument_literal(necc_p(-e, -l), -l),
            argument_literal(hyp(-e), -e),
            attacks_literal(fact(e), -e),
        }
        actual = set(s4.state)

        self.assertSetEqual(expected, actual)

    def test_doesnt_stay_in_library_3(self):
        cs = GroupI(fact_set=frozenset({e}))
        s3 = Situation(frozenset({
            position_literal(-l),
            argument_literal(necc_p(-e, -l), -l),
            argument_literal(hyp(-e), -e),
            attacks_literal(fact(e), -e),
        }))
        s4 = cs.do(consolidate_action, s3)

        expected = {
            position_literal(-l),
            argument_literal(necc_p(-e, -l), -l),
            argument_literal(hyp(-e), -e),
            counterargument_literal(fact(e), e),
        }
        actual = set(s4.state)

        self.assertSetEqual(expected, actual)


# noinspection DuplicatedCode
class TestGroupIISheHasAnEssayToFinish(unittest.TestCase):

    def test_stays_in_library_1a(self):
        cs = GroupII(fact_set=frozenset({e, t}))
        s1 = Situation(frozenset({position_literal(l)}))
        s2 = cs.do(supports_action(suff_p(e, l), l), s1)

        expected = {
            position_literal(l),
            argument_literal(suff_p(e, l), l),
        }
        actual = set(s2.state)

        self.assertSetEqual(expected, actual)

    def test_stays_in_library_1b(self):
        cs = GroupII(fact_set=frozenset({e, t}))
        s2 = Situation(frozenset({
            position_literal(l),
            argument_literal(suff_p(e, l), l)}))
        s3 = cs.do(supports_action(fact(e), e), s2)

        expected = {
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(fact(e), e)
        }
        actual = set(s3.state)

        self.assertSetEqual(expected, actual)

    def test_stays_in_library_2a(self):
        cs = GroupII(fact_set=frozenset({e, t}))
        s3 = Situation(frozenset({
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(fact(e), e)
        }))
        s4 = cs.do(attacks_action(necc_p(-e, -l), l), s3)

        expected = {
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(fact(e), e),
            attacks_literal(necc_p(-e, -l), l),
        }
        actual = set(s4.state)

        self.assertSetEqual(expected, actual)

    def test_stays_in_library_2b(self):
        cs = GroupII(fact_set=frozenset({e, t}))
        s4 = Situation(frozenset({
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(fact(e), e),
            attacks_literal(necc_p(-e, -l), l),
        }))
        s5 = cs.do(supports_action(hyp(-e), -e), s4)

        expected = {
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(fact(e), e),
            attacks_literal(necc_p(-e, -l), l),
            supports_literal(hyp(-e), -e)
        }
        actual = set(s5.state)

        self.assertSetEqual(expected, actual)

    def test_stays_in_library_3(self):
        cs = GroupI(fact_set=frozenset({e}))
        s5 = Situation(frozenset({
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(fact(e), e),
            attacks_literal(necc_p(-e, -l), l),
            supports_literal(hyp(-e), -e)
        }))
        s6 = cs.do(defends_action(fact(e), e), s5)

        expected = {
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(fact(e), e),
            attacks_literal(necc_p(-e, -l), l),
            supports_literal(hyp(-e), -e),
            defends_literal(fact(e), e),
        }
        actual = set(s6.state)

        self.assertSetEqual(expected, actual)

    def test_stays_in_library_4(self):
        cs = GroupII(fact_set=frozenset({e, t}))
        s6 = Situation(frozenset({
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(fact(e), e),
            attacks_literal(necc_p(-e, -l), l),
            supports_literal(hyp(-e), -e),
            defends_literal(fact(e), e),
        }))
        s7 = cs.do(consolidate_action, s6)

        expected = {
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(fact(e), e),
            counterargument_literal(necc_p(-e, -l), -l),
            counterargument_literal(hyp(-e), -e),
        }
        actual = set(s7.state)

        self.assertSetEqual(expected, actual)

    def test_doesnt_stay_in_library_1a(self):
        cs = GroupII(fact_set=frozenset({e, t}))
        s1 = Situation(frozenset({position_literal(-l)}))
        s2 = cs.do(supports_action(necc_p(-e, -l), -l), s1)

        expected = {
            position_literal(-l),
            argument_literal(necc_p(-e, -l), -l),
        }
        actual = set(s2.state)

        self.assertSetEqual(expected, actual)

    def test_doesnt_stay_in_library_1b(self):
        cs = GroupII(fact_set=frozenset({e, t}))
        s2 = Situation(frozenset({
            position_literal(-l),
            argument_literal(necc_p(-e, -l), -l),
        }))
        s3 = cs.do(supports_action(hyp(-e), -e), s2)

        expected = {
            position_literal(-l),
            argument_literal(necc_p(-e, -l), -l),
            argument_literal(hyp(-e), -e)
        }
        actual = set(s3.state)

        self.assertSetEqual(expected, actual)

    def test_doesnt_stay_in_library_2(self):
        cs = GroupII(fact_set=frozenset({e, t}))
        s3 = Situation(frozenset({
            position_literal(-l),
            argument_literal(necc_p(-e, -l), -l),
            argument_literal(hyp(-e), -e)
        }))
        s4 = cs.do(attacks_action(fact(e), -e), s3)

        expected = {
            position_literal(-l),
            argument_literal(necc_p(-e, -l), -l),
            argument_literal(hyp(-e), -e),
            attacks_literal(fact(e), -e),
        }
        actual = set(s4.state)

        self.assertSetEqual(expected, actual)

    def test_doesnt_stay_in_library_3(self):
        cs = GroupII(fact_set=frozenset({e, t}))
        s3 = Situation(frozenset({
            position_literal(-l),
            argument_literal(necc_p(-e, -l), -l),
            argument_literal(hyp(-e), -e),
            attacks_literal(fact(e), -e),
        }))
        s4 = cs.do(consolidate_action, s3)

        expected = {
            position_literal(-l),
            argument_literal(necc_p(-e, -l), -l),
            argument_literal(hyp(-e), -e),
            counterargument_literal(fact(e), e),
        }
        actual = set(s4.state)

        self.assertSetEqual(expected, actual)


# noinspection DuplicatedCode
class TestGroupIIISheHasAnEssayToFinish(unittest.TestCase):

    def test_stays_in_library_1a(self):
        cs = GroupIII(fact_set=frozenset({e}))
        s1 = Situation(frozenset({position_literal(l)}))
        s2 = cs.do(supports_action(suff_p(e, l), l), s1)

        expected = {
            position_literal(l),
            argument_literal(suff_p(e, l), l),
        }
        actual = set(s2.state)

        self.assertSetEqual(expected, actual)

    def test_stays_in_library_1b(self):
        cs = GroupIII(fact_set=frozenset({e}))
        s2 = Situation(frozenset({
            position_literal(l),
            argument_literal(suff_p(e, l), l)}))
        s3 = cs.do(supports_action(fact(e), e), s2)

        expected = {
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(fact(e), e)
        }
        actual = set(s3.state)

        self.assertSetEqual(expected, actual)

    def test_stays_in_library_2a(self):
        cs = GroupIII(fact_set=frozenset({e}))
        s3 = Situation(frozenset({
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(fact(e), e)
        }))
        s4 = cs.do(attacks_action(necc_p(-o, -l), l), s3)

        expected = {
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(fact(e), e),
            attacks_literal(necc_p(-o, -l), l),
        }
        actual = set(s4.state)

        self.assertSetEqual(expected, actual)

    def test_stays_in_library_2b(self):
        cs = GroupIII(fact_set=frozenset({e}))
        s4 = Situation(frozenset({
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(fact(e), e),
            attacks_literal(necc_p(-o, -l), l),
        }))
        s5 = cs.do(supports_action(hyp(-o), -o), s4)

        expected = {
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(fact(e), e),
            attacks_literal(necc_p(-o, -l), l),
            supports_literal(hyp(-o), -o)
        }
        actual = set(s5.state)

        self.assertSetEqual(expected, actual)

    def test_stays_in_library_3(self):
        cs = GroupIII(fact_set=frozenset({e}))
        s5 = Situation(frozenset({
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(fact(e), e),
            attacks_literal(necc_p(-o, -l), l),
            supports_literal(hyp(-o), -o)
        }))
        s6 = cs.do(defends_action(hyp(o), o), s5)

        expected = {
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(fact(e), e),
            attacks_literal(necc_p(-o, -l), l),
            supports_literal(hyp(-o), -o),
            defends_literal(hyp(o), o),
        }
        actual = set(s6.state)

        self.assertSetEqual(expected, actual)

    def test_stays_in_library_4(self):
        cs = GroupIII(fact_set=frozenset({e}))
        s6 = Situation(frozenset({
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(fact(e), e),
            attacks_literal(necc_p(-o, -l), l),
            supports_literal(hyp(-o), -o),
            defends_literal(hyp(o), o)
        }))
        s7 = cs.do(consolidate_action, s6)

        expected = {
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(fact(e), e),
            counterargument_literal(necc_p(-o, -l), -l),
            counterargument_literal(hyp(-o), -o),
            argument_literal(hyp(o), o),
        }
        actual = set(s7.state)

        self.assertSetEqual(expected, actual)

    def test_doesnt_stay_in_library_1a(self):
        cs = GroupIII(fact_set=frozenset({e}))
        s1 = Situation(frozenset({position_literal(-l)}))
        s2 = cs.do(supports_action(necc_p(-o, -l), -l), s1)

        expected = {
            position_literal(-l),
            argument_literal(necc_p(-o, -l), -l),
        }
        actual = set(s2.state)

        self.assertSetEqual(expected, actual)

    def test_doesnt_stay_in_library_1b(self):
        cs = GroupIII(fact_set=frozenset({e}))
        s2 = Situation(frozenset({
            position_literal(-l),
            argument_literal(necc_p(-o, -l), -l),
        }))
        s3 = cs.do(supports_action(hyp(-o), -o), s2)

        expected = {
            position_literal(-l),
            argument_literal(necc_p(-o, -l), -l),
            argument_literal(hyp(-o), -o)
        }
        actual = set(s3.state)

        self.assertSetEqual(expected, actual)

    def test_doesnt_stay_in_library_2(self):
        cs = GroupIII(fact_set=frozenset({e}))
        s3 = Situation(frozenset({
            position_literal(-l),
            argument_literal(necc_p(-o, -l), -l),
            argument_literal(hyp(-o), -o)
        }))
        s4 = cs.do(attacks_action(suff_p(e, l), -l), s3)

        expected = {
            position_literal(-l),
            argument_literal(necc_p(-o, -l), -l),
            argument_literal(hyp(-o), -o),
            attacks_literal(suff_p(e, l), -l),
        }
        actual = set(s4.state)

        self.assertSetEqual(expected, actual)

    def test_doesnt_stay_in_library_3(self):
        cs = GroupIII(fact_set=frozenset({e}))
        s3 = Situation(frozenset({
            position_literal(-l),
            argument_literal(necc_p(-o, -l), -l),
            argument_literal(hyp(-o), -o),
            attacks_literal(suff_p(e, l), -l),
        }))
        s4 = cs.do(supports_action(fact(e), e), s3)

        expected = {
            position_literal(-l),
            argument_literal(necc_p(-o, -l), -l),
            argument_literal(hyp(-o), -o),
            attacks_literal(suff_p(e, l), -l),
            supports_literal(fact(e), e)
        }
        actual = set(s4.state)

        self.assertSetEqual(expected, actual)

    def test_doesnt_stay_in_library_4a(self):
        cs = GroupIII(fact_set=frozenset({e}))
        s4 = Situation(frozenset({
            position_literal(-l),
            argument_literal(necc_p(-o, -l), -l),
            argument_literal(hyp(-o), -o),
            attacks_literal(suff_p(e, l), -l),
            supports_literal(fact(e), e)
        }))
        s5 = cs.do(defends_action(necc_p(-o, -l), -l), s4)

        expected = {
            position_literal(-l),
            argument_literal(necc_p(-o, -l), -l),
            argument_literal(hyp(-o), -o),
            attacks_literal(suff_p(e, l), -l),
            supports_literal(fact(e), e),
            defends_literal(necc_p(-o, -l), -l)
        }
        actual = set(s5.state)

        self.assertSetEqual(expected, actual)

    def test_doesnt_stay_in_library_4b(self):
        cs = GroupIII(fact_set=frozenset({e}))
        s6 = Situation(frozenset({
            position_literal(-l),
            argument_literal(necc_p(-o, -l), -l),
            argument_literal(hyp(-o), -o),
            attacks_literal(suff_p(e, l), -l),
            supports_literal(fact(e), e),
            defends_literal(necc_p(-o, -l), -l)
        }))
        s7 = cs.do(supports_action(hyp(-o), -o), s6)

        expected = {
            position_literal(-l),
            argument_literal(necc_p(-o, -l), -l),
            argument_literal(hyp(-o), -o),
            attacks_literal(suff_p(e, l), -l),
            supports_literal(fact(e), e),
            defends_literal(necc_p(-o, -l), -l),
            supports_literal(hyp(-o), -o)
        }
        actual = set(s7.state)

        self.assertSetEqual(expected, actual)

    def test_doesnt_stay_in_library_5(self):
        cs = GroupIII(fact_set=frozenset({e}))
        s7 = Situation(frozenset({
            position_literal(-l),
            argument_literal(necc_p(-o, -l), -l),
            argument_literal(hyp(-o), -o),
            attacks_literal(suff_p(e, l), -l),
            supports_literal(fact(e), e),
            defends_literal(necc_p(-o, -l), -l),
            supports_literal(hyp(-o), -o)
        }))
        s8 = cs.do(consolidate_action, s7)

        expected = {
            position_literal(-l),
            argument_literal(necc_p(-o, -l), -l),
            argument_literal(hyp(-o), -o),
            counterargument_literal(suff_p(e, l), l),
            counterargument_literal(fact(e), e),
            argument_literal(necc_p(-o, -l), -l)  # duplicate
        }
        actual = set(s8.state)

        self.assertSetEqual(expected, actual)


# noinspection DuplicatedCode
class TestGroupISheDoesNotHaveAnEssayToFinish(unittest.TestCase):

    def test_stays_in_library_1aa(self):
        cs = GroupI(fact_set=frozenset({-e}))
        s1 = Situation(frozenset({
            position_literal(l),
        }))
        s2 = cs.do(supports_action(suff_p(e, l), l), s1)

        expected = {
            position_literal(l),
            argument_literal(suff_p(e, l), l),
        }

        actual = set(s2.state)

        self.assertSetEqual(expected, actual)

    def test_stays_in_library_1ab(self):
        cs = GroupI(fact_set=frozenset({-e}))
        s2 = Situation(frozenset({
            position_literal(l),
            argument_literal(suff_p(e, l), l),
        }))
        s3 = cs.do(supports_action(hyp(e), e), s2)

        expected = {
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(hyp(e), e),
        }

        actual = set(s3.state)

        self.assertSetEqual(expected, actual)

    def test_stays_in_library_2a(self):
        cs = GroupI(fact_set=frozenset({-e}))
        s3 = Situation(frozenset({
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(hyp(e), e),
        }))
        s4 = cs.do(attacks_action(fact(-e), e), s3)

        expected = {
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(hyp(e), e),
            attacks_literal(fact(-e), e),
        }

        actual = set(s4.state)

        self.assertSetEqual(expected, actual)

    def test_stays_in_library_3(self):
        cs = GroupI(fact_set=frozenset({-e}))
        s4 = Situation(frozenset({
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(hyp(e), e),
            attacks_literal(fact(-e), e),
        }))
        s5 = cs.do(consolidate_action, s4)

        expected = {
            position_literal(l),
            argument_literal(suff_p(e, l), l),
            argument_literal(hyp(e), e),
            counterargument_literal(fact(-e), -e)
        }

        actual = set(s5.state)

        self.assertSetEqual(expected, actual)

    def test_stays_in_library_1b(self):
        cs = GroupI(fact_set=frozenset({-e}))
        s1 = Situation(frozenset({
            position_literal(l),
        }))
        s2 = cs.do(supports_action(hyp(l), l), s1)

        expected = {
            position_literal(l),
            argument_literal(hyp(l), l),
        }

        actual = set(s2.state)

        self.assertSetEqual(expected, actual)

    def test_stays_in_library_2ba(self):
        cs = GroupI(fact_set=frozenset({-e}))
        s2 = Situation(frozenset({
            position_literal(l),
            argument_literal(hyp(l), l),
        }))
        s3 = cs.do(attacks_action(necc_p(-e, -l), l), s2)

        expected = {
            position_literal(l),
            argument_literal(hyp(l), l),
            attacks_literal(necc_p(-e, -l), l)
        }

        actual = set(s3.state)

        self.assertSetEqual(expected, actual)

    def test_stays_in_library_2bb(self):
        cs = GroupI(fact_set=frozenset({-e}))
        s3 = Situation(frozenset({
            position_literal(l),
            argument_literal(hyp(l), l),
            attacks_literal(necc_p(-e, -l), l)
        }))
        s4 = cs.do(supports_action(fact(-e), -e), s3)

        expected = {
            position_literal(l),
            argument_literal(hyp(l), l),
            attacks_literal(necc_p(-e, -l), l),
            supports_literal(fact(-e), -e)
        }

        actual = set(s4.state)

        self.assertSetEqual(expected, actual)

    def test_stays_in_library_3b(self):
        cs = GroupI(fact_set=frozenset({-e}))
        s4 = Situation(frozenset({
            position_literal(l),
            argument_literal(hyp(l), l),
            attacks_literal(necc_p(-e, -l), l),
            supports_literal(fact(-e), -e)
        }))
        s5 = cs.do(consolidate_action, s4)

        expected = {
            position_literal(l),
            argument_literal(hyp(l), l),
            counterargument_literal(necc_p(-e, -l), -l),
            counterargument_literal(fact(-e), -e)
        }

        actual = set(s5.state)

        self.assertSetEqual(expected, actual)

    def test_doesnt_stay_in_library_1a(self):
        cs = GroupI(fact_set=frozenset({-e}))
        s1 = Situation(frozenset({
            position_literal(-l),
        }))
        s2 = cs.do(supports_action(necc_p(-e, -l), -l), s1)

        expected = {
            position_literal(-l),
            argument_literal(necc_p(-e, -l), -l),
        }

        actual = set(s2.state)

        self.assertSetEqual(expected, actual)

    def test_doesnt_stay_in_library_1b(self):
        cs = GroupI(fact_set=frozenset({-e}))
        s2 = Situation(frozenset({
            position_literal(-l),
            argument_literal(necc_p(-e, -l), -l),
        }))
        s3 = cs.do(supports_action(fact(-e), -e), s2)

        expected = {
            position_literal(-l),
            argument_literal(necc_p(-e, -l), -l),
            argument_literal(fact(-e), -e),
        }

        actual = set(s3.state)

        self.assertSetEqual(expected, actual)

    def test_doesnt_stay_in_library_2a(self):
        cs = GroupI(fact_set=frozenset({-e}))
        s3 = Situation(frozenset({
            position_literal(-l),
            argument_literal(necc_p(-e, -l), -l),
            argument_literal(fact(-e), -e),
        }))
        s4 = cs.do(attacks_action(hyp(l), -l), s3)

        expected = {
            position_literal(-l),
            argument_literal(necc_p(-e, -l), -l),
            argument_literal(fact(-e), -e),
            attacks_literal(hyp(l), -l)
        }

        actual = set(s4.state)

        self.assertSetEqual(expected, actual)

    def test_doesnt_stay_in_library_3aa(self):
        cs = GroupI(fact_set=frozenset({-e}))
        s4 = Situation(frozenset({
            position_literal(-l),
            argument_literal(necc_p(-e, -l), -l),
            argument_literal(fact(-e), -e),
            attacks_literal(hyp(l), -l)
        }))
        s5 = cs.do(defends_action(necc_p(-e, -l), -l), s4)

        expected = {
            position_literal(-l),
            argument_literal(necc_p(-e, -l), -l),
            argument_literal(fact(-e), -e),
            attacks_literal(hyp(l), -l),
            defends_literal(necc_p(-e, -l), -l)
        }

        actual = set(s5.state)

        self.assertSetEqual(expected, actual)

    def test_doesnt_stay_in_library_3ab(self):
        cs = GroupI(fact_set=frozenset({-e}))
        s5 = Situation(frozenset({
            position_literal(-l),
            argument_literal(necc_p(-e, -l), -l),
            argument_literal(fact(-e), -e),
            attacks_literal(hyp(l), -l),
            defends_literal(necc_p(-e, -l), -l)
        }))
        s6 = cs.do(supports_action(fact(-e), -e), s5)

        expected = {
            position_literal(-l),
            argument_literal(necc_p(-e, -l), -l),
            argument_literal(fact(-e), -e),
            attacks_literal(hyp(l), -l),
            defends_literal(necc_p(-e, -l), -l),
            supports_literal(fact(-e), -e)
        }

        actual = set(s6.state)

        self.assertSetEqual(expected, actual)

    def test_doesnt_stay_in_library_4a(self):
        cs = GroupI(fact_set=frozenset({-e}))
        s6 = Situation(frozenset({
            position_literal(-l),
            argument_literal(necc_p(-e, -l), -l),
            argument_literal(fact(-e), -e),
            attacks_literal(hyp(l), -l),
            defends_literal(necc_p(-e, -l), -l),
            supports_literal(fact(-e), -e)
        }))
        s7 = cs.do(consolidate_action, s6)

        expected = {
            position_literal(-l),
            argument_literal(necc_p(-e, -l), -l),
            argument_literal(fact(-e), -e),
            counterargument_literal(hyp(l), l),
            argument_literal(necc_p(-e, -l), -l),  # duplicate
            argument_literal(fact(-e), -e)  # duplicate
        }

        actual = set(s7.state)

        self.assertSetEqual(expected, actual)

    def test_doesnt_stay_in_library_2b(self):
        cs = GroupI(fact_set=frozenset({-e}))
        s3 = Situation(frozenset({
            position_literal(-l),
            argument_literal(necc_p(-e, -l), -l),
            argument_literal(fact(-e), -e),
        }))
        s4 = cs.do(attacks_action(suff_p(e, l), -l), s3)

        expected = {
            position_literal(-l),
            argument_literal(necc_p(-e, -l), -l),
            argument_literal(fact(-e), -e),
            attacks_literal(suff_p(e, l), -l)
        }

        actual = set(s4.state)

        self.assertSetEqual(expected, actual)
