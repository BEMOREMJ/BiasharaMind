from pydantic import BaseModel


class StubListResponse(BaseModel):
    items: list[dict[str, str]]
    message: str
