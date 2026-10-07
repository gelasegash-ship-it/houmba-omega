from datetime import datetime, timezone

from pydantic import BaseModel, Field


class RevenueEvent(BaseModel):
    source: str
    amount: float = Field(ge=0)
    currency: str = "USD"
    kind: str
    recorded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class RevenueMetrics:
    def __init__(self) -> None:
        self.gross = 0.0
        self.costs = 0.0
        self.events = 0

    @property
    def net(self) -> float:
        return self.gross - self.costs

    @property
    def margin(self) -> float:
        return 0.0 if self.gross == 0 else self.net / self.gross

    def add(self, event: RevenueEvent) -> None:
        self.events += 1
        if event.kind in {"sale", "subscription", "payout_in"}:
            self.gross += event.amount
        elif event.kind in {"cost", "refund", "payout_out"}:
            self.costs += event.amount
