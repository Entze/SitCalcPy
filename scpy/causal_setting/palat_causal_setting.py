from typing import Union

from frozendict import frozendict  # type: ignore
from pydantic.dataclasses import dataclass

from scpy.action.action import Action
from scpy.causal_setting.epistemic_causal_setting import EpistemicCausalSetting
from scpy.formula.evaluable_formula import EvaluableFormula
from scpy.function.function import Function
from scpy.situation.epistemic_situation import EpistemicSituation
from scpy.situation.situation import Situation
from scpy.state.state import State


@dataclass(frozen=True, order=True)
class PalatCausalSetting(EpistemicCausalSetting):

    def do_state(self, action: Action, state: State) -> State:
        if action.symbol == 'public_announcement':
            return state
        elif action.symbol == 'public_test':
            return state
        else:
            assert action.symbol == 'public_assignment'
            assert len(action.arguments)
            assert isinstance(action.arguments[0], Function)
            # TODO
            # For every fluent p and for every assignment every p := psi: If psi evaluates to True
            # or
            # If p was already true and not at least one of the assignments holds
            pass
        pass

    def do(self, action: Action, situation: EpistemicSituation) -> EpistemicSituation:
        if action.symbol == 'public_announcement':
            assert len(action.arguments) == 2
            assert isinstance(action.arguments[0], EvaluableFormula)
            state_ = self.do_state(action, situation.state)
            announcement: EvaluableFormula = action.arguments[0]
            knowledge_relation = situation.knowledge_relation
            knowledge_relation_ = frozendict(
                {agent:
                    frozendict({
                        k_state: log_probability for k_state, log_probability in relation.items() if
                        announcement.evaluate(k_state)
                    }) for agent, relation in knowledge_relation.items()}
            )
            situation_ = EpistemicSituation(state=state_,
                                            previous_action=action,
                                            previous_situation=situation,
                                            knowledge_relation=knowledge_relation_)
            return situation_
        if action.symbol == 'public_test':
            assert len(action.arguments) == 2
            assert isinstance(action.arguments[0], EvaluableFormula)
            state_ = self.do_state(action, situation.state)
            test: EvaluableFormula = action.arguments[0]
            knowledge_relation = situation.knowledge_relation
            knowledge_relation_ = frozendict(
                {agent:
                    frozendict({
                        k_state: log_probability for k_state, log_probability in relation.items() if
                        test.evaluate(k_state) == test.evaluate(situation.state)
                    }) for agent, relation in knowledge_relation.items()}
            )
            situation_ = EpistemicSituation(state=state_,
                                            previous_action=action,
                                            previous_situation=situation,
                                            knowledge_relation=knowledge_relation_)
            return situation_
        if action.symbol == 'public_assignment':
            pass
        pass

    def __poss_agnostic(self, action: Action, s: Union[State, Situation]) -> bool:
        if action.symbol == 'public_announcement':
            if not action.arguments:
                return False
            if not isinstance(action.arguments[0], EvaluableFormula):
                return False
            announcement: EvaluableFormula = action.arguments[0]
            res = announcement.evaluate(s)
            if res == 'Inconclusive':
                return False
            return res
        elif action.symbol == 'public_test':
            return True
        elif action.symbol == 'public_assignment':
            return True
        else:
            return False

    def poss_state(self, action: Action, state: State) -> bool:
        return action in self.actions and self.__poss_agnostic(action, state)

    def poss(self, action: Action, situation: EpistemicSituation) -> bool:
        return action in self.actions and self.__poss_agnostic(action, situation)
