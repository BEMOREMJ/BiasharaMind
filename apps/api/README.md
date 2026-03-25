# apps/api

Minimal FastAPI backend scaffold for BiasharaMind.

## Included

- FastAPI application entrypoint
- Central API router registration
- Environment-driven settings
- Health endpoint
- Placeholder route modules for businesses, assessments, analyses, and reports
- Starter folders for schemas, models, services, repositories, and core utilities

## Run

Install dependencies in this app environment, then start with:

```bash
uvicorn app.main:app --reload
```

## Notes

- No database integration, authentication, or business logic is implemented yet.
- Route handlers return simple stub payloads so the service can start cleanly.
- The structure is intended to support future domain services and persistence layers without restructuring.
