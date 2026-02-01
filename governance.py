
from datetime import datetime

class GovernanceGuardrails:
    def __init__(self):
        self.max_autonomous_actions_per_hour = 5
        self.high_risk_actions = {"DISABLE_PAYMENT_METHOD"}
        self.action_log = []

    def allow(self, decision):
        now = datetime.now()
        last_hour = [a for a in self.action_log if (now-a).seconds<3600]

        if len(last_hour)>=self.max_autonomous_actions_per_hour:
            return False,"Rate limit exceeded"

        if decision.action_type.value in self.high_risk_actions:
            return False,"High-risk action requires approval"

        self.action_log.append(now)
        return True,"Allowed"
