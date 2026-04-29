from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.domain.schemas import TriggerResponse, IntegrationFlowResponse, FlowStepResponse
from app.infrastructure.repositories import IntegrationFlowRepositoryPostgres
from app.infrastructure.database import get_db
from app.application.use_cases import TriggerEnrichmentFlow, GetFlowStatus, GetAllFlows
from typing import List

router = APIRouter(prefix="/integration", tags=["integration"])


@router.post("/trigger/{batch_id}", response_model=TriggerResponse, status_code=201)
async def trigger_flow(batch_id: str, db: Session = Depends(get_db)):
    try:
        repository = IntegrationFlowRepositoryPostgres(db)
        use_case = TriggerEnrichmentFlow(repository)
        flow = await use_case.execute(batch_id)
        return TriggerResponse(
            flow_id=flow.id,
            batch_id=flow.batch_id,
            status=flow.status,
            message=f"Flow completed with status: {flow.status.value}",
            steps=[
                FlowStepResponse(
                    step_name=s.step_name,
                    status=s.status,
                    error_message=s.error_message,
                    started_at=s.started_at,
                    completed_at=s.completed_at,
                ) for s in flow.steps
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{batch_id}", response_model=IntegrationFlowResponse)
def get_status(batch_id: str, db: Session = Depends(get_db)):
    try:
        repository = IntegrationFlowRepositoryPostgres(db)
        use_case = GetFlowStatus(repository)
        flow = use_case.execute(batch_id)
        if not flow:
            raise HTTPException(status_code=404, detail="Flow not found for this batch_id")
        return IntegrationFlowResponse(
            id=flow.id,
            batch_id=flow.batch_id,
            status=flow.status,
            steps=[
                FlowStepResponse(
                    step_name=s.step_name,
                    status=s.status,
                    error_message=s.error_message,
                    started_at=s.started_at,
                    completed_at=s.completed_at,
                ) for s in flow.steps
            ],
            created_at=flow.created_at,
            updated_at=flow.updated_at,
            total_books=flow.total_books,
            processed_books=flow.processed_books,
            failed_books=flow.failed_books,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/flows", response_model=List[IntegrationFlowResponse])
def get_all_flows(db: Session = Depends(get_db)):
    try:
        repository = IntegrationFlowRepositoryPostgres(db)
        use_case = GetAllFlows(repository)
        flows = use_case.execute()
        return [
            IntegrationFlowResponse(
                id=f.id,
                batch_id=f.batch_id,
                status=f.status,
                steps=[
                    FlowStepResponse(
                        step_name=s.step_name,
                        status=s.status,
                        error_message=s.error_message,
                        started_at=s.started_at,
                        completed_at=s.completed_at,
                    ) for s in f.steps
                ],
                created_at=f.created_at,
                updated_at=f.updated_at,
                total_books=f.total_books,
                processed_books=f.processed_books,
                failed_books=f.failed_books,
            ) for f in flows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
def health():
    return {"status": "ok", "service": "integration-service"}
