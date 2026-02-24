"""AI Engine — Unified interface for Claude and OpenAI for stakeholder analysis and outreach."""

from typing import Optional
import json
import anthropic
import openai

from app.config import settings


class AIEngine:
    """Handles all AI-powered analysis using Claude (primary) or OpenAI (secondary)."""

    def __init__(self):
        self._claude_client = None
        self._openai_client = None

    @property
    def claude(self) -> anthropic.Anthropic:
        if self._claude_client is None:
            self._claude_client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        return self._claude_client

    @property
    def openai_client(self) -> openai.OpenAI:
        if self._openai_client is None:
            self._openai_client = openai.OpenAI(api_key=settings.openai_api_key)
        return self._openai_client

    async def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        provider: str = "claude",
        max_tokens: int = 2000,
        temperature: float = 0.7,
    ) -> str:
        """Generate text using the specified AI provider."""
        if provider == "claude":
            return await self._generate_claude(prompt, system_prompt, max_tokens, temperature)
        elif provider == "openai":
            return await self._generate_openai(prompt, system_prompt, max_tokens, temperature)
        else:
            raise ValueError(f"Unknown AI provider: {provider}")

    async def _generate_claude(
        self, prompt: str, system_prompt: str, max_tokens: int, temperature: float
    ) -> str:
        message = self.claude.messages.create(
            model=settings.claude_model,
            max_tokens=max_tokens,
            system=system_prompt if system_prompt else "You are an expert SAP sales strategist and business analyst.",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        return message.content[0].text

    async def _generate_openai(
        self, prompt: str, system_prompt: str, max_tokens: int, temperature: float
    ) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        else:
            messages.append({
                "role": "system",
                "content": "You are an expert SAP sales strategist and business analyst.",
            })
        messages.append({"role": "user", "content": prompt})

        response = self.openai_client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content

    async def generate_json(
        self,
        prompt: str,
        system_prompt: str = "",
        provider: str = "claude",
        max_tokens: int = 2000,
    ) -> dict:
        """Generate a structured JSON response."""
        json_instruction = (
            "\n\nRespond ONLY with valid JSON. No markdown, no code fences, no explanation."
        )
        result = await self.generate(
            prompt + json_instruction,
            system_prompt,
            provider,
            max_tokens,
            temperature=0.3,
        )
        # Clean up potential markdown fences
        result = result.strip()
        if result.startswith("```"):
            result = result.split("\n", 1)[1]
        if result.endswith("```"):
            result = result.rsplit("```", 1)[0]
        result = result.strip()
        return json.loads(result)


# Singleton
ai_engine = AIEngine()
