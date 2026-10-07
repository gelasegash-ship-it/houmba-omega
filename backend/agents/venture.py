from dataclasses import dataclass

from backend.core.models import Opportunity


@dataclass(frozen=True)
class VentureExperiment:
    offer: str
    target_customer: str
    validation_channel: str
    success_metric: str
    max_budget_usd: float


class VentureBuilder:
    """Creates the smallest bounded experiment before a venture is scaled."""

    def design(self, opportunity: Opportunity) -> VentureExperiment:
        return VentureExperiment(
            offer=f"Pilot: {opportunity.title}",
            target_customer="A clearly defined business segment with the problem described by the opportunity.",
            validation_channel="Direct outreach + landing page + measurable call-to-action",
            success_metric="At least 3 qualified prospects or 1 paid pilot before expansion.",
            max_budget_usd=min(50.0, max(10.0, opportunity.cost)),
        )
