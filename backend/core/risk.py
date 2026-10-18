from .models import ActionRequest, Decision
import os

class RiskGateway:
    def __init__(self, mode=None, max_action_value_usd=None):
        # Explicit arguments support deterministic tests; environment remains the default.
        self.max_value = float(max_action_value_usd if max_action_value_usd is not None else os.getenv("MAX_ACTION_VALUE_USD", "100"))
        self.mode = mode if mode is not None else os.getenv("NOAH_MODE", "research")

    def evaluate(self, request: ActionRequest) -> Decision:
        if self.mode != "live":
            return Decision(status="blocked", reason="Live execution disabled; current mode is research.")
        if request.value_usd > self.max_value:
            return Decision(status="needs_confirmation", reason="Action exceeds configured value limit.")
        if request.requires_confirmation:
            return Decision(status="needs_confirmation", reason="Explicit confirmation required.")
        return Decision(status="approved", reason="Within configured policy.")
