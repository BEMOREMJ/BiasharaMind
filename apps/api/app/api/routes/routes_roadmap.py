from fastapi import APIRouter, HTTPException, status

from app.core.auth import CurrentUser
from app.schemas.roadmap import RoadmapRead
from app.services.roadmap_service import roadmap_service


router = APIRouter()


@router.get("/roadmap", response_model=RoadmapRead)
def get_roadmap(current_user: CurrentUser) -> RoadmapRead:
    roadmap = roadmap_service.get_roadmap(current_user.id)
    if roadmap is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Roadmap not found",
        )
    return roadmap


@router.post("/roadmap/generate", response_model=RoadmapRead)
def generate_roadmap(current_user: CurrentUser) -> RoadmapRead:
    roadmap = roadmap_service.generate_roadmap(current_user.id)
    if roadmap is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis summary not found",
        )
    return roadmap
