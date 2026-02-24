"""Outreach Generator — Creates personalized outreach messages using AI."""

from typing import Optional
from sqlalchemy.orm import Session

from app.models.stakeholder import Stakeholder
from app.models.company import Company
from app.models.outreach_message import OutreachMessage
from app.services.ai_engine import ai_engine
from app.services.profiling import profiling_service


MESSAGE_TYPES = {
    "initial_connect": {
        "description": "First connection request or cold outreach",
        "max_length": 300,  # LinkedIn connection note limit
        "framework": "Hook → Relevance → Soft Ask",
    },
    "follow_up": {
        "description": "Follow up after connection accepted or no reply",
        "max_length": 1000,
        "framework": "Callback → Value → Question",
    },
    "value_share": {
        "description": "Share an insight, article, or relevant content",
        "max_length": 1000,
        "framework": "Context → Insight → Connection to Their World → Soft CTA",
    },
    "meeting_request": {
        "description": "Ask for a meeting or call",
        "max_length": 1000,
        "framework": "Recap Relationship → Specific Value → Clear Ask → Easy Out",
    },
}

TONE_INSTRUCTIONS = {
    "professional": "Write in a professional, consultative tone. Be respectful of their time. Sound like a peer, not a seller.",
    "casual": "Write in a warm, conversational tone. Keep it light and genuine. Avoid corporate jargon.",
    "thought_leader": "Write as a thought leader sharing insights. Lead with industry knowledge. Position yourself as an expert who can help.",
}


class OutreachGenerator:
    """Generates personalized outreach messages for 1-to-1 and 1-to-many campaigns."""

    SYSTEM_PROMPT = """You are an expert SAP sales copywriter who creates highly personalized
outreach messages. Your messages consistently achieve 30%+ reply rates because they:

1. Lead with genuine relevance to the recipient, not the sender
2. Reference specific details about the person or their company
3. Provide value (insight, benchmark, idea) before asking for anything
4. Sound human, not templated — no "I hope this finds you well"
5. Have a clear but soft call-to-action
6. Are concise — every word earns its place

You NEVER:
- Use generic openers ("I came across your profile")
- Lead with your company or what you sell
- Use excessive exclamation marks or emojis
- Write walls of text
- Sound desperate or pushy
- Use buzzwords without substance

SAP solutions you can reference:
- SAP Business AI — Embedded AI across business processes
- SAP S/4HANA Cloud — Next-gen ERP
- SAP BTP — Business Technology Platform
- SAP SuccessFactors — HR/HCM
- SAP Ariba — Procurement
- SAP Signavio — Process intelligence
- SAP Analytics Cloud — Planning & BI
- SAP Integration Suite — System integration
- RISE with SAP / GROW with SAP — Transformation bundles"""

    async def generate_message(
        self,
        stakeholder: Stakeholder,
        company: Optional[Company],
        message_type: str = "initial_connect",
        channel: str = "linkedin_message",
        tone: str = "professional",
        sap_solutions: list[str] = None,
        custom_context: str = None,
        provider: str = "claude",
    ) -> dict:
        """Generate a single personalized outreach message."""
        context = profiling_service._build_context(stakeholder, company)
        msg_config = MESSAGE_TYPES.get(message_type, MESSAGE_TYPES["initial_connect"])
        tone_instruction = TONE_INSTRUCTIONS.get(tone, TONE_INSTRUCTIONS["professional"])

        prompt = f"""Write a {message_type.replace('_', ' ')} message for this stakeholder.

{context}

MESSAGE REQUIREMENTS:
- Channel: {channel}
- Max length: {msg_config['max_length']} characters
- Framework: {msg_config['framework']}
- Tone: {tone_instruction}
{f'- SAP solutions to reference (subtly): {", ".join(sap_solutions)}' if sap_solutions else '- Reference SAP solutions only if naturally relevant'}
{f'- Additional context: {custom_context}' if custom_context else ''}

Return as JSON:
{{
    "subject": "email subject line (only if channel is email, otherwise null)",
    "body": "the message body",
    "personalization_context": "brief note on what you personalized and why",
    "sap_solutions_referenced": ["list of SAP solutions mentioned or implied"]
}}"""

        result = await ai_engine.generate_json(prompt, self.SYSTEM_PROMPT, provider, max_tokens=1500)
        result["ai_model_used"] = provider
        result["message_type"] = message_type
        result["channel"] = channel
        return result

    async def generate_variant(
        self,
        stakeholder: Stakeholder,
        company: Optional[Company],
        original_message: dict,
        provider: str = "claude",
    ) -> dict:
        """Generate an A/B variant of an existing message."""
        context = profiling_service._build_context(stakeholder, company)

        prompt = f"""Here's an outreach message that was written for this stakeholder:

ORIGINAL MESSAGE:
{original_message.get('body', '')}

{context}

Write a DIFFERENT version of this message. Change the:
- Opening hook (use a completely different angle)
- Value proposition framing
- Call to action style

Keep the same general intent and length, but make it distinct enough for A/B testing.

Return as JSON:
{{
    "subject": "email subject (null for LinkedIn)",
    "body": "the variant message body",
    "personalization_context": "what's different about this variant",
    "sap_solutions_referenced": ["solutions referenced"]
}}"""

        result = await ai_engine.generate_json(prompt, self.SYSTEM_PROMPT, provider)
        result["ai_model_used"] = provider
        result["variant"] = "B"
        return result

    async def generate_sequence(
        self,
        stakeholder: Stakeholder,
        company: Optional[Company],
        steps: list[dict],
        channel: str = "linkedin_message",
        tone: str = "professional",
        provider: str = "claude",
    ) -> list[dict]:
        """Generate a full multi-touch outreach sequence."""
        context = profiling_service._build_context(stakeholder, company)
        tone_instruction = TONE_INSTRUCTIONS.get(tone, TONE_INSTRUCTIONS["professional"])

        step_descriptions = []
        for i, step in enumerate(steps):
            step_type = step.get("type", "follow_up")
            delay = step.get("delay_days", 3)
            step_descriptions.append(f"Step {i+1} ({step_type}, +{delay} days)")

        prompt = f"""Create a multi-touch outreach sequence for this stakeholder.

{context}

SEQUENCE PLAN:
{chr(10).join(step_descriptions)}

Channel: {channel}
Tone: {tone_instruction}

Each message should build on the previous one, escalating engagement naturally.
Step 1 should be a connection/introduction.
Subsequent steps should add value, share insights, and eventually request a meeting.
NEVER repeat yourself or reference previous messages explicitly (assume they may not have read them).

Return as JSON:
{{
    "sequence": [
        {{
            "step": 1,
            "type": "initial_connect",
            "subject": null,
            "body": "message text",
            "personalization_context": "what was personalized",
            "sap_solutions_referenced": []
        }},
        ...
    ]
}}"""

        result = await ai_engine.generate_json(
            prompt, self.SYSTEM_PROMPT, provider, max_tokens=4000
        )
        return result.get("sequence", [])


outreach_generator = OutreachGenerator()
