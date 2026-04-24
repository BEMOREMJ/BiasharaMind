from __future__ import annotations

from abc import ABC, abstractmethod


class InterpretationProviderError(RuntimeError):
    pass


class InterpretationProvider(ABC):
    provider_name: str = "unknown"

    @abstractmethod
    def generate_structured_json(self, *, system_prompt: str, user_prompt: str) -> str:
        raise NotImplementedError


class DisabledInterpretationProvider(InterpretationProvider):
    provider_name = "disabled"

    def generate_structured_json(self, *, system_prompt: str, user_prompt: str) -> str:
        raise InterpretationProviderError("AI interpretation provider is not configured.")
