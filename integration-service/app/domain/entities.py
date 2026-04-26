from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from enum import Enum
import uuid


class StepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class FlowStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    PARTIAL = "partial"
    FAILED = "failed"


@dataclass
class FlowStep:
    step_name: str
    status: StepStatus = StepStatus.PENDING
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def start(self):
        self.status = StepStatus.RUNNING
        self.started_at = datetime.utcnow()

    def complete(self):
        self.status = StepStatus.COMPLETED
        self.completed_at = datetime.utcnow()

    def fail(self, error: str):
        self.status = StepStatus.FAILED
        self.error_message = error
        self.completed_at = datetime.utcnow()


@dataclass
class IntegrationFlow:
    id: str
    batch_id: str
    status: FlowStatus
    steps: List[FlowStep]
    created_at: datetime
    updated_at: datetime
    total_books: int = 0
    processed_books: int = 0
    failed_books: int = 0

    @staticmethod
    def create(batch_id: str) -> 'IntegrationFlow':
        now = datetime.utcnow()
        steps = [
            FlowStep(step_name="inventory"),
            FlowStep(step_name="enrichment"),
            FlowStep(step_name="normalization"),
            FlowStep(step_name="catalog"),
        ]
        return IntegrationFlow(
            id=str(uuid.uuid4()),
            batch_id=batch_id,
            status=FlowStatus.PENDING,
            steps=steps,
            created_at=now,
            updated_at=now,
        )

    def get_step(self, name: str) -> Optional[FlowStep]:
        return next((s for s in self.steps if s.step_name == name), None)

    def update_status(self):
        statuses = [s.status for s in self.steps]
        if all(s == StepStatus.COMPLETED for s in statuses):
            self.status = FlowStatus.COMPLETED
        elif any(s == StepStatus.FAILED for s in statuses):
            completed = sum(1 for s in statuses if s == StepStatus.COMPLETED)
            self.status = FlowStatus.PARTIAL if completed > 0 else FlowStatus.FAILED
        elif any(s == StepStatus.RUNNING for s in statuses):
            self.status = FlowStatus.RUNNING
        self.updated_at = datetime.utcnow()
