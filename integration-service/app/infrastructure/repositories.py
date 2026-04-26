from typing import Optional, List
from sqlalchemy.orm import Session
from app.domain.entities import IntegrationFlow, FlowStep, StepStatus, FlowStatus
from app.domain.repositories import IntegrationFlowRepository
from app.infrastructure.models import IntegrationFlowModel
from datetime import datetime


class IntegrationFlowRepositoryPostgres(IntegrationFlowRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, flow: IntegrationFlow) -> IntegrationFlow:
        steps_data = [
            {
                "step_name": s.step_name,
                "status": s.status.value,
                "error_message": s.error_message,
                "started_at": s.started_at.isoformat() if s.started_at else None,
                "completed_at": s.completed_at.isoformat() if s.completed_at else None,
            }
            for s in flow.steps
        ]
        existing = self.db.query(IntegrationFlowModel).filter(
            IntegrationFlowModel.id == flow.id
        ).first()
        if existing:
            existing.status = flow.status.value
            existing.steps = steps_data
            existing.updated_at = flow.updated_at
            existing.total_books = flow.total_books
            existing.processed_books = flow.processed_books
            existing.failed_books = flow.failed_books
            self.db.commit()
            self.db.refresh(existing)
        else:
            model = IntegrationFlowModel(
                id=flow.id,
                batch_id=flow.batch_id,
                status=flow.status.value,
                steps=steps_data,
                created_at=flow.created_at,
                updated_at=flow.updated_at,
                total_books=flow.total_books,
                processed_books=flow.processed_books,
                failed_books=flow.failed_books,
            )
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
        return flow

    def find_by_id(self, flow_id: str) -> Optional[IntegrationFlow]:
        model = self.db.query(IntegrationFlowModel).filter(
            IntegrationFlowModel.id == flow_id
        ).first()
        return self._to_entity(model) if model else None

    def find_by_batch_id(self, batch_id: str) -> Optional[IntegrationFlow]:
        model = self.db.query(IntegrationFlowModel).filter(
            IntegrationFlowModel.batch_id == batch_id
        ).order_by(IntegrationFlowModel.created_at.desc()).first()
        return self._to_entity(model) if model else None

    def find_all(self) -> List[IntegrationFlow]:
        models = self.db.query(IntegrationFlowModel).order_by(
            IntegrationFlowModel.created_at.desc()
        ).all()
        return [self._to_entity(m) for m in models]

    def _to_entity(self, model: IntegrationFlowModel) -> IntegrationFlow:
        steps = []
        for s in model.steps:
            step = FlowStep(step_name=s["step_name"])
            step.status = StepStatus(s["status"])
            step.error_message = s.get("error_message")
            if s.get("started_at"):
                step.started_at = datetime.fromisoformat(s["started_at"])
            if s.get("completed_at"):
                step.completed_at = datetime.fromisoformat(s["completed_at"])
            steps.append(step)
        return IntegrationFlow(
            id=model.id,
            batch_id=model.batch_id,
            status=FlowStatus(model.status),
            steps=steps,
            created_at=model.created_at,
            updated_at=model.updated_at,
            total_books=model.total_books,
            processed_books=model.processed_books,
            failed_books=model.failed_books,
        )
