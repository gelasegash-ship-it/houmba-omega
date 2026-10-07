from backend.core.models import Opportunity

SEED_OPPORTUNITIES = [
    Opportunity(title="AI sales agent for small businesses", category="B2B automation", source="seed", demand=92, margin=88, speed=90, cost=25, competition=55, risk=25, defensibility=65),
    Opportunity(title="AI customer-support automation", category="B2B automation", source="seed", demand=90, margin=82, speed=92, cost=20, competition=60, risk=20, defensibility=60),
    Opportunity(title="Vertical micro-SaaS operated by agents", category="SaaS", source="seed", demand=84, margin=90, speed=70, cost=35, competition=65, risk=25, defensibility=78),
    Opportunity(title="Agentic-commerce optimization service", category="commerce", source="seed", demand=86, margin=80, speed=72, cost=30, competition=45, risk=30, defensibility=72),
    Opportunity(title="Business intelligence and pricing alerts", category="data", source="seed", demand=80, margin=86, speed=68, cost=30, competition=48, risk=25, defensibility=74),
]
