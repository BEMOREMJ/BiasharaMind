from fastapi import APIRouter, HTTPException, status

from app.core.auth import CurrentUser
from app.v2.schemas.profile import (
    BusinessProfileV2Create,
    BusinessProfileV2Read,
    BusinessProfileV2SaveResponse,
)
from app.v2.services.business_profile import get_business_profile_v2_service


router = APIRouter(prefix="/v2")


@router.get("/business-profile", response_model=BusinessProfileV2Read)
def get_business_profile_v2(current_user: CurrentUser) -> BusinessProfileV2Read:
    profile = get_business_profile_v2_service().get_profile(current_user.id)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="V2 business profile not found",
        )
    return profile


@router.put("/business-profile", response_model=BusinessProfileV2SaveResponse)
def save_business_profile_v2(
    payload: BusinessProfileV2Create,
    current_user: CurrentUser,
) -> BusinessProfileV2SaveResponse:
    return get_business_profile_v2_service().save_profile(payload, current_user.id)
