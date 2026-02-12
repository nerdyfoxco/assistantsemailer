from .llm import get_llm_provider
from .prompts import REPLY_SYSTEM_PROMPT, REPLY_USER_PROMPT
from chapters.work.item import WorkItem
from foundation.lib.logging import StructuredLogger

logger = StructuredLogger.get_logger("brain.service")

class BrainService:
    def __init__(self):
        self.llm = get_llm_provider()

    def generate_draft(self, work_item: WorkItem, tone: str = "Professional") -> str:
        """
        Generates a draft for a given Work Item.
        Updates the Work Item state to REVIEW.
        """
        try:
            # 1. Prepare Context
            # In a real system, we'd parse the payload for body/sender
            # For v0, assuming payload has 'snippet' or raw body.
            body = work_item.payload.get('snippet', 'No content') 
            sender = "Unknown Sender" # Todo: Extract from payload

            # 2. Render Prompts
            system = REPLY_SYSTEM_PROMPT.format(tone=tone)
            user = REPLY_USER_PROMPT.format(sender=sender, body=body)

            # 3. Call LLM
            work_item.start_drafting()
            draft_text = self.llm.generate(system, user)

            # 4. Update Work Item
            work_item.draft_complete({
                "body": draft_text,
                "model": "mock", # or actual model
                "tone": tone
            })
            
            logger.info("Draft generated", work_item_id=work_item.id, tone=tone)
            return draft_text

        except Exception as e:
            logger.error("Failed to generate draft", exception=str(e), work_item_id=work_item.id)
            raise
