
import logging
import json
from typing import Optional, Any, List
from pydantic import BaseModel, Field
from spine.chapters.mind.llm_client import LLMClient
from spine.chapters.mind.context import ContextBuilder
from spine.db.models import Email

logger = logging.getLogger(__name__)

class ActionType:
    REPLY = "REPLY"
    ARCHIVE = "ARCHIVE"
    IGNORE = "IGNORE"
    ESCALATE = "ESCALATE"

class Decision(BaseModel):
    """Structured Output from the Mind."""
    action: str = Field(..., description="Action to take: REPLY, ARCHIVE, IGNORE, ESCALATE")
    reasoning: str = Field(..., description="Brief explanation of why this action was chosen.")
    draft_body: Optional[str] = Field(None, description="If REPLY, the body of the email draft.")
    tags: List[str] = Field(default_factory=list, description="Suggested tags for the email.")

SYSTEM_PROMPT = """
You are the "Mind" of an advanced Email Assistant.
Your goal is to process incoming emails and decide the best course of action.
You are acting on behalf of a busy professional.

AVAILABLE ACTIONS:
- REPLY: The email requires a response. Write a professional, concise draft.
- ARCHIVE: The email is transactional, informational, or spam. No action needed.
- IGNORE: The email is irrelevant but maybe not spam.
- ESCALATE: The email is urgent, critical, or requires complex human intervention beyond a draft.

OUTPUT FORMAT:
You MUST respond with valid JSON matching this schema:
{
  "action": "REPLY" | "ARCHIVE" | "IGNORE" | "ESCALATE",
  "reasoning": "string",
  "draft_body": "string | null",
  "tags": ["string"]
}

RULES:
1. If the email is a newsletter, receipt, or notification -> ARCHIVE.
2. If the email is a personal question or work request -> REPLY.
3. If the email mentions "URGENT", "ASAP" -> ESCALATE (unless simple).
4. Be concise in reasoning.
"""

class Strategist:
    """
    UMP-70-03: The Strategist.
    Orchestrates Context to Decisions.
    """
    def __init__(self, llm_client: LLMClient, context_builder: ContextBuilder):
        self.llm = llm_client
        self.context = context_builder

    async def decide(self, user_id: str, email: Email, creds: Any) -> Decision:
        """
        The Core Loop: Email -> Context -> LLM -> Decision.
        """
        try:
            # 1. Build Context (The Senses)
            ctx = await self.context.build(user_id, email, creds)
            
            # 2. Formulate Prompt (The Thought)
            prompt = (
                f"Analyze this email:\n"
                f"{ctx.to_system_prompt_addition()}\n"
                f"What should I do?"
            )
            
            # 3. Think (The Synapse)
            # We ask for JSON specifically
            raw_response = await self.llm.think(prompt, SYSTEM_PROMPT)
            
            # 4. Parse (The Understanding)
            return self._parse_json(raw_response)
            
        except Exception as e:
            logger.error(f"Strategist failed for {email.id}: {e}")
            # Fail Safe: Escalate on error
            return Decision(
                action=ActionType.ESCALATE,
                reasoning=f"Internal Error: {str(e)}",
                tags=["error"]
            )

    def _parse_json(self, response: str) -> Decision:
        """Robust JSON parsing from LLM output."""
        try:
            # Strip markdown code blocks if present (common LLM artifact)
            clean_resp = response.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_resp)
            return Decision(**data)
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse LLM JSON: {response}")
            # Fallback
            return Decision(
                action=ActionType.ESCALATE,
                reasoning="Failed to parse LLM response format.",
                tags=["parse_error"]
            )
