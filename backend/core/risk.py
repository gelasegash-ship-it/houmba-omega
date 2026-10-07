from .models import ActionRequest, Decision
import os
class RiskGateway:
    def __init__(self):
        self.max_value=float(os.getenv('MAX_ACTION_VALUE_USD','100')); self.mode=os.getenv('NOAH_MODE','research')
    def evaluate(self, request: ActionRequest)->Decision:
        if self.mode!='live': return Decision(status='blocked',reason='Live execution disabled; current mode is research.')
        if request.value_usd>self.max_value: return Decision(status='needs_confirmation',reason='Action exceeds configured value limit.')
        if request.requires_confirmation: return Decision(status='needs_confirmation',reason='Explicit confirmation required.')
        return Decision(status='approved',reason='Within configured policy.')
