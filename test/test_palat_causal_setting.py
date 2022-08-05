# noinspection DuplicatedCode
import unittest

from scpy.causal_setting.palat_causal_setting import PalatCausalSetting
from scpy.function.function import Function
from scpy.literal.literal import Literal
from scpy.predicate.predicate import Predicate

a_pred = Predicate('a')
b_pred = Predicate('b')
c_pred = Predicate('c')

a_lit = Literal(a_pred)
b_lit = Literal(b_pred)
c_lit = Literal(c_pred)

test_fluents = frozenset({a_pred, b_pred, c_pred})
test_actions = frozenset({
    Function('public_announcement', ()),
    Function('public_test', ()),
    Function('public_assignment', ())
})


class TestConstructor(unittest.TestCase):

    def test_create_simple(self):
        t = PalatCausalSetting()


class TestPoss(unittest.TestCase):

    def test_simple(self):
        t = PalatCausalSetting()
