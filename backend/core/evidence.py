from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class Evidence:
    source: str
    url: str
    captured_at: str
    claim: str
    confidence: float

    @classmethod
    def create(cls, source: str, url: str, claim: str, confidence: float) -> "Evidence":
        if not 0 <= confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")
        return cls(source=source, url=url, captured_at=datetime.now(timezone.utc).isoformat(), claim=claim, confidence=confidence)
