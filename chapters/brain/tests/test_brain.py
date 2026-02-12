import pytest
from chapters.brain.service import BrainService
from chapters.brain.llm import MockLLM
from chapters.work.item import WorkItem, WorkItemState

def test_brain_generate_draft():
    # Setup
    item = WorkItem("t1", "msg1", {"snippet": "Hello world"})
    brain = BrainService(llm=MockLLM())

    # Execute
    draft = brain.generate_draft(item, tone="Casual")

    # Verify
    assert draft == "This is a mocked AI response for testing."
    assert item.state == WorkItemState.REVIEW
    assert item.draft_context['body'] == draft
    assert item.draft_context['tone'] == "Casual"

def test_brain_state_enforcement():
    # Setup
    item = WorkItem("t1", "msg1", {})
    # Manually set to wrong state
    item.state = WorkItemState.CLOSED
    
    brain = BrainService(llm=MockLLM())

    # Verify Logic Error
    with pytest.raises(ValueError):
        brain.generate_draft(item)
