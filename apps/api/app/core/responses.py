from typing import Any


def stub_list_response(message: str) -> dict[str, Any]:
    return {"items": [], "message": message}
