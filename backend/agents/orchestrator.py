from dataclasses import dataclass
from typing import Iterable

from backend.agents.opportunity import OpportunityScout
from backend.core.models import Opportunity


@dataclass
class OpportunityPlan:
    objective: str
    ranked: list[Opportunity]
    next_actions: list[str]


class RevenueOrchestrator:
    """Deterministic orchestration layer; an LLM can be attached later without changing contracts."""

    def __init__(self) -> None:
        self.scout = OpportunityScout()

    def build_plan(self, objective: str, opportunities: Iterable[Opportunity]) -> OpportunityPlan:
        ranked = self.scout.rank(opportunities)
        actions: list[str] = []
        if ranked:
            actions.append("Validate the top opportunity with current evidence and customer interviews.")
            actions.append("Create a smallest sellable offer and a measurable acquisition experiment.")
            actions.append("Record revenue, cost, conversion and retention before scaling.")
        else:
            actions.append("Collect fresh market evidence before committing resources.")
        return OpportunityPlan(objective=objective, ranked=ranked, next_actions=actions)
