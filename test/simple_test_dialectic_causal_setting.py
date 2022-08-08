from pydantic.dataclasses import dataclass

from scpy.causal_setting.dialectic_causal_setting import DialecticCausalSetting
from scpy.dataclass_config import DataclassConfig
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


@dataclass(frozen=True, order=True, config=DataclassConfig)
class MilkCausalSetting(DialecticCausalSetting):
    pass
