from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.domain.entities import StepStatus, FlowStatus


class FlowStepResponse(BaseModel):
    step_name: str
    status: StepStatus
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class IntegrationFlowResponse(BaseModel):
    id: str
    batch_id: str
    status: FlowStatus
    steps: List[FlowStepResponse]
    created_at: datetime
    updated_at: datetime
    total_books: int
    processed_books: int
    failed_books: int

    class Config:
        from_attributes = True


class TriggerResponse(BaseModel):
    flow_id: str
    batch_id: str
    status: FlowStatus
    message: str
    steps: List[FlowStepResponse]
