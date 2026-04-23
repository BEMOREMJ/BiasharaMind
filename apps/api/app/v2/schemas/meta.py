from pydantic import Field

from app.v2.common import V2BaseModel


class V2VersionMetadata(V2BaseModel):
    question_bank_version: str = Field(min_length=1, max_length=64)
    scoring_version: str = Field(min_length=1, max_length=64)
    taxonomy_version: str = Field(min_length=1, max_length=64)
    prompt_version: str | None = Field(default=None, max_length=64)
    analysis_engine_version: str = Field(min_length=1, max_length=64)


CURRENT_V2_VERSION_METADATA = V2VersionMetadata(
    question_bank_version="v2.0.0",
    scoring_version="v2.0.0-placeholder",
    taxonomy_version="v2.0.0",
    prompt_version="v2.0.0-interpretation-placeholder",
    analysis_engine_version="v2.0.0-foundation",
)
