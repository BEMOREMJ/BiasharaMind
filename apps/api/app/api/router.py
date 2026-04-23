from fastapi import APIRouter

from app.api.routes import (
    routes_analysis,
    routes_assessment,
    routes_analyses,
    routes_assessments,
    routes_business_profile,
    routes_business_profile_v2,
    routes_businesses,
    routes_health,
    routes_report,
    routes_roadmap,
    routes_reports,
)


api_router = APIRouter()
api_router.include_router(routes_health.router, tags=["health"])
api_router.include_router(routes_analysis.router, tags=["analysis"])
api_router.include_router(routes_assessment.router, tags=["assessment"])
api_router.include_router(routes_business_profile.router, tags=["business-profile"])
api_router.include_router(routes_business_profile_v2.router, tags=["business-profile-v2"])
api_router.include_router(routes_report.router, tags=["report"])
api_router.include_router(routes_roadmap.router, tags=["roadmap"])
api_router.include_router(routes_businesses.router, prefix="/businesses", tags=["businesses"])
api_router.include_router(
    routes_assessments.router,
    prefix="/assessments",
    tags=["assessments"],
)
api_router.include_router(routes_analyses.router, prefix="/analyses", tags=["analyses"])
api_router.include_router(routes_reports.router, prefix="/reports", tags=["reports"])
