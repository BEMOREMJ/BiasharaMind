from pydantic import BaseModel, ConfigDict

from app.schemas.business_profile import to_camel


class V2BaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        str_strip_whitespace=True,
    )
