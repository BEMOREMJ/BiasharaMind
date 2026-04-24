import json
from typing import Any


INTERPRETATION_SYSTEM_PROMPT = """
You are an experienced SME business diagnostic interpreter.
Stay grounded only in the provided business profile, question metadata, text answer, and supporting structured answers.
Do not invent facts.
Do not assign raw health scores.
Do not change deterministic scoring.
Return strict JSON only.
Be conservative when tagging issues, root causes, severity, specificity, evidence strength, and contradictions.
""".strip()


def build_text_interpretation_prompt(payload: dict[str, Any]) -> str:
    schema_hint = {
        "question_key": "string",
        "section_key": "string",
        "summary": "short string",
        "issue_tags": [{"code": "string", "label": "string", "confidence": 0.0}],
        "root_cause_tags": [{"code": "string", "label": "string", "confidence": 0.0}],
        "affected_dimensions": ["string"],
        "severity_hint": "low|medium|high|critical|null",
        "contradiction_flags": [{"code": "string", "detail": "string", "severity": "low|medium|high", "source_refs": ["string"]}],
        "evidence_specificity": "low|medium|high|null",
        "evidence_strength": "weak|mixed|strong|null",
        "interpretation_confidence": "low|medium|high|null",
        "evidence_snippets": ["short grounded quote or paraphrase"],
    }
    return "\n".join(
        [
            "Interpret this single V2 text answer conservatively and return one JSON object.",
            "Required output schema:",
            json.dumps(schema_hint, indent=2, ensure_ascii=True),
            "Input payload:",
            json.dumps(payload, indent=2, ensure_ascii=True),
        ]
    )
