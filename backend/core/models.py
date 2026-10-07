from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime, timezone

class Opportunity(BaseModel):
    title: str
    category: str
    source: str
    observed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    demand: float = Field(ge=0, le=100)
    margin: float = Field(ge=0, le=100)
    speed: float = Field(ge=0, le=100)
    cost: float = Field(ge=0, le=100)
    competition: float = Field(ge=0, le=100)
    risk: float = Field(ge=0, le=100)
    defensibility: float = Field(ge=0, le=100)
    @property
    def score(self) -> float:
        return round((self.demand*.25+self.margin*.20+self.speed*.15+self.defensibility*.10+(100-self.cost)*.10+(100-self.competition)*.10+(100-self.risk)*.10),2)

class ActionRequest(BaseModel):
    action: str
    value_usd: float = Field(default=0, ge=0)
    requires_confirmation: bool = True
    reason: str

class Decision(BaseModel):
    status: Literal['approved','needs_confirmation','blocked']
    reason: str
