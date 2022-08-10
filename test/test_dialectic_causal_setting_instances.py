from typing import FrozenSet, Mapping, Tuple

from frozendict import frozendict
from pydantic import Field
from pydantic.dataclasses import dataclass

from scpy.causal_setting.dialectic_causal_setting import DialecticCausalSetting, fact, hyp, suff_p, necc_p, suff_e, \
    necc_e, sec_suff_p, sec_necc_p, sec_suff_e, exo_e, exo_literal
from scpy.dataclass_config import DataclassConfig
from scpy.preorder import Preorder
from scpy.primitives import Function, Literal, Predicate

need_f = Function('need')
need_p = Predicate('need')
need_l = Literal(need_p)
position_need_f = Function('position', (need_l,))
position_need_p = Predicate('position', (need_l,))
position_need_l = Literal(position_need_p)

position_compl_need_f = Function('position', (-need_l,))
position_compl_need_p = Predicate('position', (-need_l,))
position_compl_need_l = Literal(position_compl_need_p)

money_f = Function('money')
money_p = Predicate('money')
money_l = Literal(money_p)

asks_f = Function('asks')
asks_p = Predicate('asks')
asks_l = Literal(asks_p)

buy_f = Function('buy')
buy_p = Predicate('buy')
buy_l = Literal(buy_p)

position_buy_f = Function('position', (buy_l,))
position_buy_p = Predicate('position', (buy_l,))
position_buy_l = Literal(position_buy_p)
position_compl_buy_f = Function('position', (-buy_l,))
position_compl_buy_p = Predicate('position', (-buy_l,))
position_compl_buy_l = Literal(position_compl_buy_p)

fact_need = Function('fact', (need_l,))
supports_fact_need_need = Function('supports', (fact_need, need_l))
supports_fact_need_need_p = Predicate('supports', (fact_need, need_l))
supports_fact_need_need_l = Literal(supports_fact_need_need_p)
argument_fact_need_need_p = Predicate('argument', (fact_need, need_l))
argument_fact_need_need_l = Literal(argument_fact_need_need_p)

necc_p_compl_money_compl_buy = Function('necc_p', (Function('cond_for', (-money_l, -buy_l)),))
argument_necc_p_compl_money_comply_buy_compl_buy_p = Predicate('argument', (necc_p_compl_money_compl_buy, -buy_l))
argument_necc_p_compl_money_compl_buy_compl_buy_l = Literal(argument_necc_p_compl_money_comply_buy_compl_buy_p)
supports_necc_p_compl_money_compl_buy_compl_buy = Function('supports', (necc_p_compl_money_compl_buy, -buy_l))

fact_compl_money = Function('fact', (-money_l,))

supports_fact_compl_money_compl_money_f = Function('supports', (fact_compl_money, -money_l))
supports_fact_compl_money_compl_money_p = Predicate('supports', (fact_compl_money, -money_l))
supports_fact_compl_money_compl_money_l = Literal(supports_fact_compl_money_compl_money_p)
argument_fact_compl_money_p = Predicate('argument', (fact_compl_money, -money_l))
argument_fact_compl_money_l = Literal(argument_fact_compl_money_p)

suff_p_need_buy = Function('suff_p', (Function('cond_for', (need_l, buy_l)),))
hyp_need = Function('hyp', (need_l,))
hyp_compl_need = Function('hyp', (-need_l,))

fact_buy = Function('fact', (buy_l,))
fact_compl_buy = Function('fact', (-buy_l,))
hyp_buy = Function('hyp', (buy_l,))
hyp_compl_buy = Function('hyp', (-buy_l,))

attacks_hyp_buy_compl_buy_f = Function('attacks', (hyp_buy, -buy_l))
attacks_hyp_buy_compl_buy_p = Predicate('attacks', (hyp_buy, -buy_l))
attacks_hyp_buy_compl_buy_l = Literal(attacks_hyp_buy_compl_buy_p)

attacks_suff_p_need_buy_compl_buy_f = Function('attacks', (suff_p_need_buy, -buy_l))
attacks_suff_p_need_buy_compl_buy_p = Predicate('attacks', (suff_p_need_buy, -buy_l))
attacks_suff_p_need_buy_compl_buy_l = Literal(attacks_suff_p_need_buy_compl_buy_p)

supports_suff_p_need_buy_buy_f = Function('supports', (suff_p_need_buy, buy_l))
supports_suff_p_need_buy_buy_p = Predicate('supports', (suff_p_need_buy, buy_l))
supports_suff_p_need_buy_buy_l = Literal(supports_suff_p_need_buy_buy_p)

argument_suff_p_need_buy_buy_f = Function('argument', (suff_p_need_buy, buy_l))
argument_suff_p_need_buy_buy_p = Predicate('argument', (suff_p_need_buy, buy_l))
argument_suff_p_need_buy_buy_l = Literal(argument_suff_p_need_buy_buy_p)

attacks_necc_p_compl_money_comply_buy_buy_f = Function('attacks', (necc_p_compl_money_compl_buy, buy_l))
attacks_necc_p_compl_money_comply_buy_buy_p = Predicate('attacks', (necc_p_compl_money_compl_buy, buy_l))
attacks_necc_p_compl_money_compl_buy_buy_l = Literal(attacks_necc_p_compl_money_comply_buy_buy_p)

hyp_money = Function('hyp', (money_l,))
hyp_compl_money = Function('hyp', (-money_l,))

defends_hyp_money_money_f = Function('defends', (hyp_money, money_l))
defends_hyp_money_money_p = Predicate('defends', (hyp_money, money_l))
defends_hyp_money_money_l = Literal(defends_hyp_money_money_p)

supports_hyp_money_money_f = Function('supports', (hyp_money, money_l))
supports_hyp_money_money_p = Predicate('supports', (hyp_money, money_l))
supports_hyp_money_money_l = Literal(supports_hyp_money_money_p)

supports_hyp_compl_money_compl_money_f = Function('supports', (hyp_compl_money, -money_l))
supports_hyp_compl_money_compl_money_p = Predicate('supports', (hyp_compl_money, -money_l))
supports_hyp_compl_money_compl_money_l = Literal(supports_hyp_compl_money_compl_money_p)

counterargument_suff_p_need_buy_buy_f = Function('counterargument', (suff_p_need_buy, buy_l))
counterargument_suff_p_need_buy_buy_p = Predicate('counterargument', (suff_p_need_buy, buy_l))
counterargument_suff_p_need_buy_buy_l = Literal(counterargument_suff_p_need_buy_buy_p)

counterargument_fact_need_need_f = Function('counterargument', (fact_need, need_l))
counterargument_fact_need_need_p = Predicate('counterargument', (fact_need, need_l))
counterargument_fact_need_need_l = Literal(counterargument_fact_need_need_p)

counterargument_necc_p_compl_money_compl_buy_compl_buy_f = Function('counterargument',
                                                                    (necc_p_compl_money_compl_buy, -buy_l))
counterargument_necc_p_compl_money_compl_buy_compl_buy_p = Predicate('counterargument',
                                                                     (necc_p_compl_money_compl_buy, -buy_l))
counterargument_necc_p_compl_money_compl_buy_compl_buy_l = Literal(
    counterargument_necc_p_compl_money_compl_buy_compl_buy_p)

counterargument_hyp_compl_money_compl_money_f = Function('counterargument', (hyp_compl_money, -money_l))
counterargument_hyp_compl_money_compl_money_p = Predicate('counterargument', (hyp_compl_money, -money_l))
counterargument_hyp_compl_money_compl_money_l = Literal(counterargument_hyp_compl_money_compl_money_p)

argument_hyp_money_money_f = Function('argument', (hyp_money, money_l))
argument_hyp_money_money_p = Predicate('argument', (hyp_money, money_l))
argument_hyp_money_money_l = Literal(argument_hyp_money_money_p)

fact_compl_need = Function('fact', (-need_l,))


@dataclass(frozen=True, order=True, config=DataclassConfig)
class MilkCausalSetting(DialecticCausalSetting):
    pass


e_p = Predicate('e')
e = Literal(e_p)
l_p = Predicate('l')
l = Literal(l_p)
o_p = Predicate('o')
o = Literal(o_p)
t_p = Predicate('t')
t = Literal(t_p)

argument_scheme = {fact(lit): (frozenset(), frozenset({lit})) for lit in (e, l, o, t)} | {
    fact(-lit): (frozenset(), frozenset({-lit})) for lit in (e, l, o, t)} | {hyp(lit): (frozenset(), frozenset({lit}))
                                                                             for lit in (e, l, o, t)} | {
                      hyp(-lit): (frozenset(), frozenset({-lit})) for lit in (e, l, o, t)} | {
                      suff_p(e, l): (frozenset({e}), (frozenset({l}))),
                      suff_p(t, l): (frozenset({t}), (frozenset({l}))),
                      necc_p(-o, -l): (frozenset({-o}), (frozenset({-l}))),
                      necc_p(-e, -l): (frozenset({-e}), (frozenset({-l}))),
                      suff_e(l, t): (frozenset({l}), (frozenset({t}))),
                      suff_e(l, e): (frozenset({l}), (frozenset({e}))),
                      necc_e(-l, -e): (frozenset({-l}), (frozenset({-e}))),
                      necc_e(-l, -o): (frozenset({-l}), (frozenset({-o}))),
                      sec_suff_p(-l, -e): (frozenset({-l}), (frozenset({-e}))),
                      sec_suff_p(-l, -t): (frozenset({-l}), (frozenset({-t}))),
                      sec_necc_p(l, o): (frozenset({l}), (frozenset({o}))),
                      sec_necc_p(l, e): (frozenset({l}), (frozenset({e}))),
                      sec_suff_e(-l, -e): (frozenset({-l}), (frozenset({-e}))),
                      sec_suff_e(-l, -t): (frozenset({-l}), (frozenset({-t}))),
                  } | {
                      exo_e(lit): (frozenset({lit}), (frozenset({exo_literal(lit)}))) for lit in (e, l, o, t)
                  }

argument_for = {}
for arg in argument_scheme:
    if isinstance(arg.arguments[0], Function):
        argument_for[arg.arguments[0].arguments[1]] = arg

conflict_relation: Preorder = Preorder.from_tuples(
    *(
        *((fact(lit), fact(-lit)) for lit in (e, l, o, t)),
        *((hyp(lit), hyp(-lit)) for lit in (e, l, o, t)),
        *((arg1, arg2) for arg1 in argument_scheme for arg2 in argument_scheme if
          isinstance(arg1.arguments[0], Function) and len(arg1.arguments[0].arguments) > 1 and
          isinstance(arg2.arguments[0], Function) and len(arg2.arguments[0].arguments) > 1 and
          isinstance(arg1.arguments[0].arguments[1], Literal) and isinstance(arg2.arguments[0].arguments[1],
                                                                             Literal) and
          -(arg1.arguments[0].arguments[1]) == arg2.arguments[0].arguments[1]),
        (suff_e(l, e), suff_e(l, t)),

        (sec_suff_e(-l, -e), necc_e(-l, -e)),
        (sec_suff_e(-l, -e), necc_e(-l, -o)),
        (sec_suff_e(-l, -t), necc_e(-l, -e)),
        (sec_suff_e(-l, -t), necc_e(-l, -o)),

        (necc_e(-l, -e), necc_e(-l, -o)),
        (necc_e(-l, -e), sec_suff_e(-l, -e)),
        (necc_e(-l, -e), sec_suff_e(-l, -t)),
        (necc_e(-l, -o), sec_suff_e(-l, -e)),
        (necc_e(-l, -o), sec_suff_e(-l, -t)),

        *((exo_e(l), expl) for expl in (
            fact(l), hyp(l),
            *(explanation for explanation in argument_scheme.keys()
              if len(explanation.arguments) == 2 and explanation.arguments[1] == l)
        )),
        *((exo_e(-l), expl) for expl in (
            fact(-l), hyp(-l),
            *(explanation for explanation in argument_scheme.keys()
              if len(explanation.arguments) == 2 and explanation.arguments[1] == -l)
        )),
    ), symmetry=True
)

strength_preorder: Preorder = Preorder.from_tuples(
    *(
        *((fact(lit), fact(-lit)) for lit in (e, l, o, t)),
        *((fact(-lit), fact(lit)) for lit in (e, l, o, t)),
        *((hyp(lit), hyp(-lit)) for lit in (e, l, o, t)),
        *((hyp(-lit), hyp(lit)) for lit in (e, l, o, t)),
        *((hyp(lit), fact(-lit)) for lit in (e, l, o, t)),
        *((hyp(-lit), fact(lit)) for lit in (e, l, o, t)),
        *((arg, fact(-arg.arguments[0].arguments[1])) for arg in argument_scheme if
          isinstance(arg.arguments[0], Function) and
          len(arg.arguments[0].arguments) > 1 and
          isinstance(arg.arguments[0].arguments[1], Literal)
          ),
        *((arg1, arg2) for arg1 in argument_scheme for arg2 in argument_scheme
          if conflict_relation.is_similar(arg1, arg2) and
          arg1.symbol == 'suff_p' and arg2.symbol == 'necc_p'
          )
    ), transitivity=True
)


# print(strength_preorder)


@dataclass(frozen=True, order=True, config=DataclassConfig)
class Library(DialecticCausalSetting):
    argument_scheme: Mapping[Function, Tuple[FrozenSet[Literal], FrozenSet[Literal]]] = Field(
        default=frozendict(argument_scheme))
    conflict_relation: Preorder = Field(default=conflict_relation)
    strength_preorder: Preorder = Field(default=strength_preorder)


@dataclass(frozen=True, order=True, config=DataclassConfig)
class GroupI(Library):
    awareness_set: FrozenSet[Predicate] = Field(default=frozenset({e_p, l_p}))


@dataclass(frozen=True, order=True, config=DataclassConfig)
class GroupII(Library):
    awareness_set: FrozenSet[Predicate] = Field(default=frozenset({e_p, l_p, t_p}))


@dataclass(frozen=True, order=True, config=DataclassConfig)
class GroupIII(Library):
    awareness_set: FrozenSet[Predicate] = Field(default=frozenset({e_p, l_p, o_p}))
