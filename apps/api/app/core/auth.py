import json
from typing import Annotated
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from app.core.config import get_settings


class AuthenticatedUser(BaseModel):
    id: str
    email: str | None = None


security = HTTPBearer(auto_error=False)


def _build_user_request(access_token: str) -> Request:
    settings = get_settings()

    if not settings.supabase_url or not settings.supabase_service_role_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Supabase auth verification is not configured on the API.",
        )

    return Request(
        url=f"{settings.supabase_url.rstrip('/')}/auth/v1/user",
        headers={
            "Authorization": f"Bearer {access_token}",
            "apikey": settings.supabase_service_role_key,
        },
        method="GET",
    )


def _resolve_user_from_token(access_token: str) -> AuthenticatedUser:
    request = _build_user_request(access_token)

    try:
        with urlopen(request, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        if exc.code in {401, 403}:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired authentication token.",
            ) from exc

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to validate the authentication token with Supabase.",
        ) from exc
    except (TimeoutError, URLError, json.JSONDecodeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to validate the authentication token with Supabase.",
        ) from exc

    user_id = payload.get("id")
    email = payload.get("email")

    if not isinstance(user_id, str) or not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Supabase did not return a valid authenticated user.",
        )

    return AuthenticatedUser(
        id=user_id,
        email=email if isinstance(email, str) else None,
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> AuthenticatedUser:
    if credentials is None or credentials.scheme.lower() != "bearer" or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
        )

    return _resolve_user_from_token(credentials.credentials)


CurrentUser = Annotated[AuthenticatedUser, Depends(get_current_user)]
