from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from pydantic import ValidationError

from app.v2.prompts.interpretation import (
    INTERPRETATION_SYSTEM_PROMPT,
    build_text_interpretation_prompt,
)
from app.v2.providers import get_interpretation_provider
from app.v2.providers.base import InterpretationProvider, InterpretationProviderError
from app.v2.schemas.explainability import ConfidenceLimitation, EvidenceGap, ExplainabilitySnapshot
from app.v2.schemas.interpretation import (
    ContradictionFlag,
    ContradictionSeverity,
    EvidenceSpecificity,
    EvidenceStrength,
    InterpretationConfidence,
    InterpretationFallbackResult,
    SeverityHint,
    TextInterpretationInput,
    TextInterpretationOutput,
)
from app.v2.schemas.lifecycle import AIInterpretationStatus
from app.v2.schemas.meta import CURRENT_V2_VERSION_METADATA
from app.v2.schemas.snapshots import TextInterpretationSnapshot


@dataclass
class InterpretationQuestionContext:
    question_id: str
    section_id: str
    prompt: str
    question_type: str
    answer_text: str
    tags: list[str]
    business_profile_context: dict[str, str | int | float | list[str]]
    structured_context: list[dict[str, str | int | float | list[str] | None]]


def _strip_code_fences(raw: str) -> str:
    text = raw.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 3:
            text = "\n".join(lines[1:-1]).strip()
    return text


class AITextInterpretationService:
    def __init__(self, provider: InterpretationProvider | None = None) -> None:
        self.provider = provider or get_interpretation_provider()

    def build_inputs(
        self,
        *,
        profile: Any,
        assessment: Any,
        question_map: dict[str, Any],
    ) -> list[InterpretationQuestionContext]:
        answers_by_id = {answer.question_id: answer for answer in assessment.answers}
        profile_context = profile.model_dump(mode="json", by_alias=False)
        contexts: list[InterpretationQuestionContext] = []

        for question_id, question in question_map.items():
            answer = answers_by_id.get(question_id)
            if answer is None or not answer.is_sufficient_answer or answer.response_kind != "answered":
                continue
            if question.question_type not in {"text", "textarea"}:
                continue
            if not getattr(question, "interpretation_enabled", False):
                continue
            if not isinstance(answer.value, str) or len(answer.value.strip()) < 8:
                continue

            structured_context: list[dict[str, str | int | float | list[str] | None]] = []
            for supporting_answer in assessment.answers:
                if supporting_answer.question_id == question_id:
                    continue
                supporting_question = question_map.get(supporting_answer.question_id)
                if supporting_question is None:
                    continue
                same_section = supporting_answer.section_id == answer.section_id
                risk_question = supporting_answer.section_id == "critical_risk_checks"
                if same_section or risk_question:
                    structured_context.append(
                        {
                            "question_id": supporting_answer.question_id,
                            "section_id": supporting_answer.section_id,
                            "question_type": supporting_question.question_type,
                            "response_kind": supporting_answer.response_kind,
                            "value": supporting_answer.value,
                        }
                    )

            contexts.append(
                InterpretationQuestionContext(
                    question_id=question_id,
                    section_id=answer.section_id,
                    prompt=getattr(question, "prompt", question_id),
                    question_type=question.question_type,
                    answer_text=answer.value.strip(),
                    tags=list(getattr(question, "tags", [])),
                    business_profile_context=profile_context,
                    structured_context=structured_context,
                )
            )
        return contexts

    def _fallback_output(self, context: InterpretationQuestionContext, reason: str, *, partial: bool) -> TextInterpretationOutput:
        normalized_reason = reason.strip()[:200] if reason else "interpretation_fallback"
        return TextInterpretationOutput(
            question_key=context.question_id,
            section_key=context.section_id,
            summary=None,
            fallback=InterpretationFallbackResult(
                used=True,
                reason=normalized_reason,
                partial=partial,
                recoverable=True,
            ),
        )

    def _parse_output(self, raw: str, context: InterpretationQuestionContext) -> TextInterpretationOutput:
        try:
            payload = json.loads(_strip_code_fences(raw))
        except json.JSONDecodeError as exc:
            raise InterpretationProviderError("Provider returned invalid JSON.") from exc
        output = TextInterpretationOutput.model_validate(payload)
        if output.question_key != context.question_id or output.section_key != context.section_id:
            raise InterpretationProviderError("Provider returned mismatched question identity.")
        return output

    def interpret(
        self,
        *,
        profile: Any,
        assessment: Any,
        question_map: dict[str, Any],
    ) -> TextInterpretationSnapshot:
        contexts = self.build_inputs(profile=profile, assessment=assessment, question_map=question_map)
        if not contexts:
            return TextInterpretationSnapshot(
                status=AIInterpretationStatus.NOT_REQUESTED,
                prompt_version=CURRENT_V2_VERSION_METADATA.prompt_version,
                provider_name=self.provider.provider_name,
            )

        outputs: list[TextInterpretationOutput] = []
        success_count = 0

        for context in contexts:
            if len(context.answer_text.strip()) < 20:
                outputs.append(self._fallback_output(context, "insufficient_text_detail", partial=True))
                continue

            prompt_payload = {
                "question_key": context.question_id,
                "section_key": context.section_id,
                "question_prompt": context.prompt,
                "question_tags": context.tags,
                "answer_text": context.answer_text,
                "business_profile_context": context.business_profile_context,
                "supporting_structured_answers": context.structured_context,
            }
            user_prompt = build_text_interpretation_prompt(prompt_payload)
            try:
                raw = self.provider.generate_structured_json(
                    system_prompt=INTERPRETATION_SYSTEM_PROMPT,
                    user_prompt=user_prompt,
                )
                outputs.append(self._parse_output(raw, context))
                success_count += 1
            except (InterpretationProviderError, ValidationError, Exception) as exc:
                outputs.append(self._fallback_output(context, str(exc), partial=True))

        if success_count == len(outputs):
            status = AIInterpretationStatus.COMPLETE
        elif success_count == 0:
            status = AIInterpretationStatus.FALLBACK_USED
        else:
            status = AIInterpretationStatus.PARTIAL

        return TextInterpretationSnapshot(
            status=status,
            prompt_version=CURRENT_V2_VERSION_METADATA.prompt_version,
            provider_name=self.provider.provider_name,
            inputs=[
                TextInterpretationInput(
                    question_key=item.question_id,
                    section_key=item.section_id,
                    answer_text=item.answer_text,
                    business_profile_context=item.business_profile_context,
                    source_ref=f"assessment_answer:{item.question_id}",
                )
                for item in contexts
            ],
            outputs=outputs,
        )

    def apply_to_explainability(
        self,
        explainability: ExplainabilitySnapshot,
        snapshot: TextInterpretationSnapshot,
    ) -> ExplainabilitySnapshot:
        for output in snapshot.outputs:
            if output.fallback.used and output.fallback.reason:
                explainability.confidence_limitations.append(
                    ConfidenceLimitation(
                        code=f"interpretation_{output.question_key}_fallback",
                        detail=f"AI interpretation fallback for {output.question_key}: {output.fallback.reason}.",
                        impact="Reduces interpretation-derived confidence and leaves text evidence partially unresolved.",
                    )
                )
            if output.evidence_specificity == EvidenceSpecificity.LOW:
                explainability.missing_or_weak_evidence.append(
                    EvidenceGap(
                        area=output.question_key,
                        detail="The text evidence is too generic to strongly support diagnostic interpretation.",
                        severity="medium",
                    )
                )
            if output.evidence_strength == EvidenceStrength.WEAK:
                explainability.missing_or_weak_evidence.append(
                    EvidenceGap(
                        area=output.question_key,
                        detail="The text evidence is weakly grounded and should be treated cautiously.",
                        severity="medium",
                    )
                )
            for contradiction in output.contradiction_flags:
                explainability.confidence_limitations.append(
                    ConfidenceLimitation(
                        code=contradiction.code,
                        detail=contradiction.detail,
                        impact="Introduces contradiction risk between narrative answers and structured evidence.",
                    )
                )
        return explainability


_ai_text_interpretation_service: AITextInterpretationService | None = None


def get_ai_text_interpretation_service() -> AITextInterpretationService:
    global _ai_text_interpretation_service
    if _ai_text_interpretation_service is None:
        _ai_text_interpretation_service = AITextInterpretationService()
    return _ai_text_interpretation_service
