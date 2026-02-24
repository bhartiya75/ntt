from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "SAP Sales Outreach Engine"
    database_url: str = "sqlite:///./sap_outreach.db"

    # AI API Keys
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None

    # AI Model Config
    claude_model: str = "claude-sonnet-4-20250514"
    openai_model: str = "gpt-4o"

    # Ollama (Local LLM) Config
    ollama_base_url: str = "http://localhost:11434/v1"
    ollama_model: str = "qwen2.5:7b"

    # Default AI provider: "ollama", "claude", or "openai"
    default_ai_provider: str = "ollama"

    # Enrichment APIs
    apollo_api_key: Optional[str] = None

    # Auth
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
