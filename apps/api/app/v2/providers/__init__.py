from app.core.config import get_settings
from app.v2.providers.base import DisabledInterpretationProvider, InterpretationProvider
from app.v2.providers.http_json import OpenAICompatibleInterpretationProvider


def get_interpretation_provider() -> InterpretationProvider:
    settings = get_settings()
    if settings.ai_interpretation_provider == "openai_compatible":
        if (
            settings.ai_interpretation_endpoint
            and settings.ai_interpretation_api_key
            and settings.ai_interpretation_model
        ):
            return OpenAICompatibleInterpretationProvider(
                endpoint=settings.ai_interpretation_endpoint,
                api_key=settings.ai_interpretation_api_key,
                model=settings.ai_interpretation_model,
                timeout_seconds=settings.ai_interpretation_timeout_seconds,
            )
    return DisabledInterpretationProvider()
