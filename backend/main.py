from fastapi import FastAPI
from pydantic import BaseModel
from core.models import Opportunity, ActionRequest
from core.risk import RiskGateway
from agents.opportunity import OpportunityScout
app=FastAPI(title='NOA H 1 Autonomous Engine',version='0.1.0')
risk=RiskGateway(); scout=OpportunityScout()
class RankRequest(BaseModel): opportunities:list[Opportunity]
@app.get('/health')
def health(): return {'ok':True,'mode':risk.mode,'service':'NOA H 1'}
@app.post('/opportunities/rank')
def rank(req:RankRequest): return [{'title':x.title,'category':x.category,'source':x.source,'score':x.score} for x in scout.rank(req.opportunities)]
@app.post('/risk/evaluate')
def evaluate(req:ActionRequest): return risk.evaluate(req)
