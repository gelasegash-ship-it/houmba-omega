from backend.core.models import Opportunity, ActionRequest
from backend.core.risk import RiskGateway


def test_opportunity_score_is_bounded():
    opportunity = Opportunity(title="AI automation for SMEs", category="automation", source="seed", demand=90, margin=85, speed=80, cost=20, competition=30, risk=15, defensibility=60)
    assert 0 <= opportunity.score <= 100
    assert opportunity.score > 70


def test_risk_gateway_blocks_non_live_mode():
    gateway = RiskGateway(mode="research", max_action_value_usd=100)
    decision = gateway.evaluate(ActionRequest(action="charge_customer", value_usd=10))
    assert decision.status == "blocked"


def test_risk_gateway_requires_confirmation_above_limit():
    gateway = RiskGateway(mode="live", max_action_value_usd=100)
    decision = gateway.evaluate(ActionRequest(action="purchase", value_usd=101))
    assert decision.status == "needs_confirmation"


def test_risk_gateway_allows_low_risk_live_action():
    gateway = RiskGateway(mode="live", max_action_value_usd=100)
    decision = gateway.evaluate(ActionRequest(action="publish_listing", value_usd=10))
    assert decision.status == "approved"
