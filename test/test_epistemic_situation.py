# noinspection DuplicatedCode
import math
import unittest

from frozendict import frozendict

from scpy.function.function import Function
from scpy.literal.literal import Literal
from scpy.predicate.predicate import Predicate
from scpy.situation.epistemic_situation import EpistemicSituation
from test.simple_test_epistempic_causal_setting import SimpleTestEpistemicCausalSetting


class TestConstructor(unittest.TestCase):

    def test_create_simple(self):
        a_pred = Predicate('a')
        a_lit = Literal(a_pred)
        b_pred = Predicate('b')
        b_lit = Literal(b_pred)
        c_pred = Predicate('c')
        c_lit = Literal(c_pred)
        state0 = frozenset({a_lit, b_lit})
        state1 = frozenset({a_lit, c_lit})
        state2 = frozenset({b_lit, c_lit})
        agent1 = 1
        agent2 = 2
        knowledge_relation = frozendict({
            agent1: frozendict({state0: 0.5, state1: 0.0, state2: 0.0}),
            agent2: frozendict({state0: 0.0, state1: 0.0, state2: 0.5}),
        })

        s0 = EpistemicSituation(state0, knowledge_relation=knowledge_relation)


class TestDo(unittest.TestCase):

    def test_shake(self):
        a_pred = Predicate('a')
        a_lit = Literal(a_pred)
        b_pred = Predicate('b')
        b_lit = Literal(b_pred)
        c_pred = Predicate('c')
        c_lit = Literal(c_pred)
        agent1 = 0
        agent2 = 1
        state0 = frozenset({a_lit, b_lit})
        state0a = frozenset({a_lit})
        state0b = frozenset({b_lit})
        state1 = frozenset({a_lit, c_lit})
        state1a = frozenset({a_lit})
        state1c = frozenset({c_lit})
        state2 = frozenset({b_lit, c_lit})
        state2b = frozenset({b_lit})
        state2c = frozenset({c_lit})
        knowledge_relation = frozendict({
            agent1: frozendict({state0: math.log(2 / 4), state1: math.log(1 / 4), state2: math.log(1 / 4)}),
            agent2: frozendict({state0: math.log(1 / 5), state1: math.log(1 / 5), state2: math.log(3 / 5)}),
        })

        s0 = EpistemicSituation(state0, knowledge_relation=knowledge_relation)

        t = SimpleTestEpistemicCausalSetting()

        s1 = t.do(t.tick(agent1, Function('shake')), s0)

        actual = {key: dict(value) for key, value in s1.knowledge_relation.items()}
        expected = {
            agent1: {
                state0: math.log(2 / 4) + math.log(1 / 2),
                state1: math.log(1 / 4) + math.log(1 / 2),
                state2: math.log(1 / 4) + math.log(1 / 2),
                state0a: math.log(2 / 4) + math.log(1 / 2) + math.log(1 / 2),
                state0b: math.log(2 / 4) + math.log(1 / 2) + math.log(1 / 2),
                state1a: math.log(1 / 4) + math.log(1 / 2) + math.log(1 / 2),
                state1c: math.log(1 / 4) + math.log(1 / 2) + math.log(1 / 2),
                state2b: math.log(1 / 4) + math.log(1 / 2) + math.log(1 / 2),
                state2c: math.log(1 / 4) + math.log(1 / 2) + math.log(1 / 2),
            },
            agent2: {
                state0: math.log(1 / 5) + math.log(1 / 2),
                state1: math.log(1 / 5) + math.log(1 / 2),
                state2: math.log(3 / 5) + math.log(1 / 2),
                state0a: math.log(1 / 5) + math.log(1 / 2) + math.log(1 / 2),
                state0b: math.log(1 / 5) + math.log(1 / 2) + math.log(1 / 2),
                state1a: math.log(1 / 5) + math.log(1 / 2) + math.log(1 / 2),
                state1c: math.log(1 / 5) + math.log(1 / 2) + math.log(1 / 2),
                state2b: math.log(3 / 5) + math.log(1 / 2) + math.log(1 / 2),
                state2c: math.log(3 / 5) + math.log(1 / 2) + math.log(1 / 2),
            }
        }

        self.assertDictEqual(expected, actual)

    def test_look(self):
        a_pred = Predicate('a')
        a_lit = Literal(a_pred)
        b_pred = Predicate('b')
        b_lit = Literal(b_pred)
        c_pred = Predicate('c')
        c_lit = Literal(c_pred)
        agent1 = 0
        agent2 = 1
        state0 = frozenset({a_lit, b_lit})
        state1 = frozenset({a_lit, c_lit})
        state2 = frozenset({b_lit, c_lit})
        knowledge_relation = frozendict({
            agent1: frozendict({state0: math.log(2 / 4), state1: math.log(1 / 4), state2: math.log(1 / 4)}),
            agent2: frozendict({state0: math.log(1 / 5), state1: math.log(1 / 5), state2: math.log(3 / 5)}),
        })

        s0 = EpistemicSituation(state0, knowledge_relation=knowledge_relation)

        t = SimpleTestEpistemicCausalSetting()

        s1 = t.do(t.tick(agent1, Function('look')), s0)

        actual = {key: dict(value) for key, value in s1.knowledge_relation.items()}
        expected = {
            agent1: {
                state0: 0.0,
                state1: float('-inf'),
                state2: float('-inf')
            },
            agent2: {
                state0: math.log(1 / 5),
                state1: math.log(1 / 5),
                state2: math.log(3 / 5),
            }
        }

        self.assertDictEqual(expected, actual)
