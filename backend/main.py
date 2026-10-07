from fastapi import FastAPI
from pydantic import BaseModel

from backend.agents.opportunity import OpportunityScout
from backend.agents.venture import VentureBuilder
from backend.core.models import Opportunity, ActionRequest
from backend.core.opportunities import SEED_OPPORTUNITIES
from backend.core.revenue import RevenueEvent, RevenueMetrics
from backend.core.risk import RiskGateway

app = FastAPI(title="NOA H 1 Autonomous Engine", version="0.2.0")
risk = RiskGateway()
scout = OpportunityScout()
venture_builder = VentureBuilder()
revenue = RevenueMetrics()


class RankRequest(BaseModel):
    opportunities: list[Opportunity]


@app.get("/health")
def health():
    return {"ok": True, "mode": risk.mode, "service": "NOA H 1", "version": app.version}


@app.get("/opportunities/seed")
def seed_opportunities():
    return [
        {
            "title": item.title,
            "category": item.category,
            "source": item.source,
            "score": item.score,
        }
        for item in scout.rank(SEED_OPPORTUNITIES)
    ]


@app.post("/opportunities/rank")
def rank(req: RankRequest):
    return [
        {
            "title": item.title,
            "category": item.category,
            "source": item.source,
            "score": item.score,
        }
        for item in scout.rank(req.opportunities)
    ]


@app.post("/venture/experiment")
def experiment(opportunity: Opportunity):
    return venture_builder.design(opportunity)


@app.post("/revenue/record")
def record_revenue(event: RevenueEvent):
    revenue.add(event)
    return {"recorded": True, "metrics": metrics()}


@app.get("/revenue/metrics")
def metrics():
    return {
        "gross": revenue.gross,
        "costs": revenue.costs,
        "net": revenue.net,
        "margin": revenue.margin,
        "events": revenue.events,
    }


@app.post("/risk/evaluate")
def evaluate(req: ActionRequest):
    return risk.evaluate(req)
