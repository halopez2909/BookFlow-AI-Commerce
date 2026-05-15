import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from app.domain.entities import IntegrationFlow, FlowStatus, StepStatus


def test_create_flow():
    flow = IntegrationFlow.create("batch-001")
    assert flow.batch_id == "batch-001"
    assert flow.status == FlowStatus.PENDING
    assert len(flow.steps) == 4
    step_names = [s.step_name for s in flow.steps]
    assert "inventory" in step_names
    assert "enrichment" in step_names
    assert "normalization" in step_names
    assert "catalog" in step_names


def test_flow_step_complete():
    flow = IntegrationFlow.create("batch-001")
    step = flow.get_step("inventory")
    step.start()
    assert step.status == StepStatus.RUNNING
    assert step.started_at is not None
    step.complete()
    assert step.status == StepStatus.COMPLETED
    assert step.completed_at is not None


def test_flow_step_fail():
    flow = IntegrationFlow.create("batch-001")
    step = flow.get_step("enrichment")
    step.start()
    step.fail("Connection timeout")
    assert step.status == StepStatus.FAILED
    assert step.error_message == "Connection timeout"


def test_flow_update_status_completed():
    flow = IntegrationFlow.create("batch-001")
    for step in flow.steps:
        step.start()
        step.complete()
    flow.update_status()
    assert flow.status == FlowStatus.COMPLETED


def test_flow_update_status_partial():
    flow = IntegrationFlow.create("batch-001")
    flow.steps[0].start()
    flow.steps[0].complete()
    flow.steps[1].start()
    flow.steps[1].fail("Error")
    flow.steps[2].start()
    flow.steps[2].complete()
    flow.steps[3].start()
    flow.steps[3].complete()
    flow.update_status()
    assert flow.status == FlowStatus.PARTIAL


def test_flow_update_status_failed():
    flow = IntegrationFlow.create("batch-001")
    for step in flow.steps:
        step.start()
        step.fail("Error")
    flow.update_status()
    assert flow.status == FlowStatus.FAILED


def test_get_step_returns_correct_step():
    flow = IntegrationFlow.create("batch-001")
    step = flow.get_step("normalization")
    assert step is not None
    assert step.step_name == "normalization"


def test_get_step_returns_none_for_unknown():
    flow = IntegrationFlow.create("batch-001")
    step = flow.get_step("unknown_step")
    assert step is None
