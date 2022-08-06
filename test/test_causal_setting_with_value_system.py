# noinspection: DuplicatedCode
import unittest

from test.simple_test_causal_setting_with_value_system import SimpleTestCausalSettingWithValueSystem, privacy, alpha_2, \
    alpha_3, safety, lit_at_0, alpha_4, alpha_5, good_condition, alpha_1, alpha_6

s0 = frozenset({lit_at_0})


class TestAttacks(unittest.TestCase):

    def test_p_pv_n_sf(self):
        c = SimpleTestCausalSettingWithValueSystem()

        expected = True
        actual = c.attacks_state(privacy, (alpha_2, alpha_3), safety, (alpha_2, alpha_3), 0, s0)

        self.assertEqual(expected, actual)

    def test_n_sf_p_pv(self):
        c = SimpleTestCausalSettingWithValueSystem()

        expected = True
        actual = c.attacks_state(safety, (alpha_2, alpha_3), privacy, (alpha_2, alpha_3), 0, s0)

        self.assertEqual(expected, actual)

    def test_p_pv_p_sf(self):
        c = SimpleTestCausalSettingWithValueSystem()

        expected = True
        actual = c.attacks_state(privacy, (alpha_2, alpha_3), safety, (alpha_2, alpha_4, alpha_5), 0, s0)

        self.assertEqual(expected, actual)

    def test_p_sf_p_pv(self):
        c = SimpleTestCausalSettingWithValueSystem()

        expected = True
        actual = c.attacks_state(safety, (alpha_2, alpha_4, alpha_5), privacy, (alpha_2, alpha_3), 0, s0)

        self.assertEqual(expected, actual)

    def test_p_pv_p_pv_1(self):
        c = SimpleTestCausalSettingWithValueSystem()

        expected = True
        actual = c.attacks_state(privacy, (alpha_2, alpha_3), privacy, (alpha_2, alpha_4, alpha_5), 0, s0)

        self.assertEqual(expected, actual)

    def test_p_pv_p_pv_2(self):
        c = SimpleTestCausalSettingWithValueSystem()

        expected = True
        actual = c.attacks_state(privacy, (alpha_2, alpha_4, alpha_5), privacy, (alpha_2, alpha_3), 0, s0)

        self.assertEqual(expected, actual)

    def test_p_pv_n_gc(self):
        c = SimpleTestCausalSettingWithValueSystem()

        expected = True
        actual = c.attacks_state(privacy, (alpha_2, alpha_4, alpha_5), good_condition, (alpha_2, alpha_4, alpha_5), 0,
                                 s0)

        self.assertEqual(expected, actual)

    def test_n_gc_p_pv(self):
        c = SimpleTestCausalSettingWithValueSystem()

        expected = True
        actual = c.attacks_state(good_condition, (alpha_2, alpha_4, alpha_5), privacy, (alpha_2, alpha_4, alpha_5), 0,
                                 s0)

        self.assertEqual(expected, actual)

    def test_p_sf_n_gc(self):
        c = SimpleTestCausalSettingWithValueSystem()

        expected = True
        actual = c.attacks_state(safety, (alpha_2, alpha_4, alpha_5), good_condition, (alpha_2, alpha_4, alpha_5), 0,
                                 s0)

        self.assertEqual(expected, actual)

    def test_n_pv_p_pv_1(self):
        c = SimpleTestCausalSettingWithValueSystem()

        expected = False
        actual = c.attacks_state(
            privacy, (alpha_1, alpha_6),
            privacy, (alpha_2, alpha_3),
            0, s0)

        self.assertEqual(expected, actual)

    def test_p_pv_n_pv_1(self):
        c = SimpleTestCausalSettingWithValueSystem()

        expected = False
        actual = c.attacks_state(
            privacy, (alpha_2, alpha_3),
            privacy, (alpha_1, alpha_6),
            0, s0)

        self.assertEqual(expected, actual)

    def test_n_pv_p_pv_2(self):
        c = SimpleTestCausalSettingWithValueSystem()

        expected = False
        actual = c.attacks_state(
            privacy, (alpha_1, alpha_6),
            privacy, (alpha_2, alpha_4, alpha_5),
            0, s0)

        self.assertEqual(expected, actual)

    def test_p_pv_n_pv_2(self):
        c = SimpleTestCausalSettingWithValueSystem()

        expected = False
        actual = c.attacks_state(
            privacy, (alpha_2, alpha_4, alpha_5),
            privacy, (alpha_1, alpha_6),
            0, s0)

        self.assertEqual(expected, actual)


class TestDefeats(unittest.TestCase):

    def test_p_pv_n_sf(self):
        c = SimpleTestCausalSettingWithValueSystem()

        expected = False
        actual = c.defeats_state(
            privacy, (alpha_2, alpha_3),
            safety, (alpha_2, alpha_3),
            0, s0)

        self.assertEqual(expected, actual)

    def test_n_sf_p_pv(self):
        c = SimpleTestCausalSettingWithValueSystem()

        expected = True
        actual = c.defeats_state(
            safety, (alpha_2, alpha_3),
            privacy, (alpha_2, alpha_3),
            0, s0)

        self.assertEqual(expected, actual)

    def test_p_pv_p_sf(self):
        c = SimpleTestCausalSettingWithValueSystem()

        expected = False
        actual = c.defeats_state(
            privacy, (alpha_2, alpha_3),
            safety, (alpha_2, alpha_4, alpha_5),
            0, s0)

        self.assertEqual(expected, actual)

    def test_p_sf_p_pv(self):
        c = SimpleTestCausalSettingWithValueSystem()

        expected = True
        actual = c.defeats_state(
            safety, (alpha_2, alpha_4, alpha_5),
            privacy, (alpha_2, alpha_3),
            0, s0)

        self.assertEqual(expected, actual)

    def test_p_pv_p_pv_1(self):
        c = SimpleTestCausalSettingWithValueSystem()

        expected = True
        actual = c.defeats_state(
            privacy, (alpha_2, alpha_3),
            privacy, (alpha_2, alpha_4, alpha_5),
            0, s0)

        self.assertEqual(expected, actual)

    def test_p_pv_p_pv_2(self):
        c = SimpleTestCausalSettingWithValueSystem()

        expected = True
        actual = c.defeats_state(
            privacy, (alpha_2, alpha_4, alpha_5),
            privacy, (alpha_2, alpha_3),
            0, s0)

        self.assertEqual(expected, actual)

    def test_p_pv_n_gc(self):
        c = SimpleTestCausalSettingWithValueSystem()

        expected = False
        actual = c.defeats_state(
            privacy, (alpha_2, alpha_4, alpha_5),
            good_condition, (alpha_2, alpha_4, alpha_5),
            0, s0)

        self.assertEqual(expected, actual)

    def test_n_gc_p_pv(self):
        c = SimpleTestCausalSettingWithValueSystem()

        expected = True
        actual = c.defeats_state(
            good_condition, (alpha_2, alpha_4, alpha_5),
            privacy, (alpha_2, alpha_4, alpha_5),
            0, s0)

        self.assertEqual(expected, actual)

    def test_p_sf_n_gc(self):
        c = SimpleTestCausalSettingWithValueSystem()

        expected = True
        actual = c.defeats_state(
            safety, (alpha_2, alpha_4, alpha_5),
            good_condition, (alpha_2, alpha_4, alpha_5),
            0, s0)

        self.assertEqual(expected, actual)

    def test_n_pv_p_pv_1(self):
        c = SimpleTestCausalSettingWithValueSystem()

        expected = False
        actual = c.defeats_state(
            privacy, (alpha_1, alpha_6),
            privacy, (alpha_2, alpha_3),
            0, s0)

        self.assertEqual(expected, actual)

    def test_p_pv_n_pv_1(self):
        c = SimpleTestCausalSettingWithValueSystem()

        expected = False
        actual = c.defeats_state(
            privacy, (alpha_2, alpha_3),
            privacy, (alpha_1, alpha_6),
            0, s0)

        self.assertEqual(expected, actual)

    def test_n_pv_p_pv_2(self):
        c = SimpleTestCausalSettingWithValueSystem()

        expected = False
        actual = c.defeats_state(
            privacy, (alpha_1, alpha_6),
            privacy, (alpha_2, alpha_4, alpha_5),
            0, s0)

        self.assertEqual(expected, actual)

    def test_p_pv_n_pv_2(self):
        c = SimpleTestCausalSettingWithValueSystem()

        expected = False
        actual = c.defeats_state(
            privacy, (alpha_2, alpha_4, alpha_5),
            privacy, (alpha_1, alpha_6),
            0, s0)

        self.assertEqual(expected, actual)
