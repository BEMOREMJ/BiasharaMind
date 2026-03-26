from fastapi import APIRouter, HTTPException, status

from app.schemas.business_profile import (
    BusinessProfileCreate,
    BusinessProfileRead,
    BusinessProfileUpdate,
)
from app.services.business_profile_service import business_profile_service


router = APIRouter()


@router.get("/business-profile", response_model=BusinessProfileRead)
def get_business_profile() -> BusinessProfileRead:
    profile = business_profile_service.get_profile()
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business profile not found",
        )
    return profile


@router.post(
    "/business-profile",
    response_model=BusinessProfileRead,
    status_code=status.HTTP_201_CREATED,
)
def create_business_profile(payload: BusinessProfileCreate) -> BusinessProfileRead:
    existing = business_profile_service.get_profile()
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Business profile already exists",
        )
    return business_profile_service.create_profile(payload)


@router.patch("/business-profile", response_model=BusinessProfileRead)
def update_business_profile(payload: BusinessProfileUpdate) -> BusinessProfileRead:
    profile = business_profile_service.update_profile(payload)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business profile not found",
        )
    return profile
