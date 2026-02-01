
from typing import Optional, Dict
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class PaymentStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    PENDING = "pending"


class PaymentSignal:
    """
    Tolerant signal model.
    ALL non-core fields optional.
    Safe for UI + simulator.
    """

    def __init__(
        self,
        transaction_id: str,
        amount: float = 0.0,
        currency: str = "USD",
        status: str = PaymentStatus.SUCCESS,
        latency_ms: float = 0.0,
        error_code: Optional[str] = None,
        timestamp: float = 0.0,
        payment_method: Optional[str] = None,
        processor: Optional[str] = None,
        issuer_bank: Optional[str] = None,
        **kwargs
    ):
        self.transaction_id = transaction_id
        self.amount = amount
        self.currency = currency
        self.status = str(status)
        self.latency_ms = latency_ms
        self.error_code = error_code
        self.timestamp = timestamp
        self.payment_method = payment_method
        self.processor = processor
        self.issuer_bank = issuer_bank


class AgentMemory:
    def __init__(self):
        self.recent_signals = []


class PaymentObserver:
    def __init__(self, memory: AgentMemory):
        self.memory = memory
        self.signals = []

    async def observe(self, signal: PaymentSignal):
        self.signals.append(signal)
        self.memory.recent_signals.append(signal)

    def calculate_metrics(self) -> Dict:
        total = len(self.signals)

        if total == 0:
            return {
                "total_volume": 0,
                "success_count": 0,
                "failure_count": 0,
                "success_rate": 0.0,
                "failure_rate": 0.0,
                "avg_latency": 0.0,
                "retry_rate": 0.0,
            }

        success = sum(1 for s in self.signals if s.status == "success")
        failure = sum(1 for s in self.signals if s.status == "failure")

        return {
            "total_volume": total,
            "success_count": success,
            "failure_count": failure,
            "success_rate": success / total,
            "failure_rate": failure / total,
            "avg_latency": sum(s.latency_ms for s in self.signals) / total,
            "retry_rate": 0.0,
        }


class PaymentOpsAgent:
    def __init__(self):
        self.memory = AgentMemory()
        self.observer = PaymentObserver(self.memory)
        self.running = False

    async def process_payment_signal(self, signal: PaymentSignal):
        await self.observer.observe(signal)

    def start(self):
        self.running = True

    def stop(self):
        self.running = False
