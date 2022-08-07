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

position_need_compl_f = Function('position', (-need_l,))
position_need_compl_p = Predicate('position', (-need_l,))
position_need_compl_l = Literal(position_need_compl_p)

money_f = Function('money')
money_compl = Function('compl', (money_f,))
money_compl_p = Predicate('compl', (money_f,))
money_p = Predicate('money')
money_l = Literal(money_p)
money_compl_l = Literal(money_compl_p)

asks_f = Function('asks')
asks_p = Predicate('asks')
asks_l = Literal(asks_p)

buy_f = Function('buy')
buy_p = Predicate('buy')
buy_l = Literal(buy_p)

fact_need = Function('fact', (need_l,))
supports_fact_need_need = Function('supports', (fact_need, need_l))
argument_fact_need_p = Predicate('argument', (fact_need,))
argument_fact_need_l = Literal(argument_fact_need_p)


@dataclass(frozen=True, order=True, config=DataclassConfig)
class MilkCausalSetting(DialecticCausalSetting):
    pass
