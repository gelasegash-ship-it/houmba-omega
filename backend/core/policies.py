from dataclasses import dataclass


@dataclass(frozen=True)
class OperatingPolicy:
    mode: str = "research"
    max_action_value_usd: float = 100.0
    require_confirmation_for_money: bool = True
    require_audit_for_side_effects: bool = True

    @property
    def live_enabled(self) -> bool:
        return self.mode == "live"
