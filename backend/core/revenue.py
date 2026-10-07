from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class RevenueEvent:
    source: str
    amount: float
    currency: str
    kind: str
    recorded_at: str

    @classmethod
    def create(cls, source: str, amount: float, currency: str, kind: str) -> "RevenueEvent":
        if amount < 0:
            raise ValueError("amount must be non-negative")
        return cls(source, amount, currency, kind, datetime.now(timezone.utc).isoformat())

@dataclass
class RevenueMetrics:
    gross: float = 0.0
    costs: float = 0.0
    events: int = 0

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
