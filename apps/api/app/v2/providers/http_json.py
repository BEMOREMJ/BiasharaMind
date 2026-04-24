from __future__ import annotations

import json
from typing import Any
from urllib import error, request

from app.v2.providers.base import InterpretationProvider, InterpretationProviderError


class OpenAICompatibleInterpretationProvider(InterpretationProvider):
    provider_name = "openai_compatible"

    def __init__(self, *, endpoint: str, api_key: str, model: str, timeout_seconds: int = 20) -> None:
        self.endpoint = endpoint
        self.api_key = api_key
        self.model = model
        self.timeout_seconds = timeout_seconds

    def generate_structured_json(self, *, system_prompt: str, user_prompt: str) -> str:
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0,
        }
        http_request = request.Request(
            self.endpoint,
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        try:
            with request.urlopen(http_request, timeout=self.timeout_seconds) as response:
                payload: dict[str, Any] = json.loads(response.read().decode("utf-8"))
        except error.URLError as exc:
            raise InterpretationProviderError(f"Provider request failed: {exc.reason}") from exc
        except json.JSONDecodeError as exc:
            raise InterpretationProviderError("Provider returned invalid JSON payload.") from exc

        choices = payload.get("choices")
        if not isinstance(choices, list) or not choices:
            raise InterpretationProviderError("Provider response did not include choices.")
        message = choices[0].get("message", {})
        content = message.get("content")
        if isinstance(content, list):
            parts = [item.get("text", "") for item in content if isinstance(item, dict)]
            content = "".join(parts).strip()
        if not isinstance(content, str) or not content.strip():
            raise InterpretationProviderError("Provider response did not include usable message content.")
        return content.strip()
