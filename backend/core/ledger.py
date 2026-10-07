from datetime import datetime, timezone
from dataclasses import dataclass, asdict
@dataclass
class LedgerEvent:
    kind:str; amount:float; currency:str; description:str; timestamp:str
class Ledger:
    def __init__(self): self.events=[]
    def record(self,kind,amount,currency='USD',description=''):
        e=LedgerEvent(kind,amount,currency,description,datetime.now(timezone.utc).isoformat()); self.events.append(asdict(e)); return self.events[-1]
