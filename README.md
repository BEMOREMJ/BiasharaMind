# BiasharaMind

BiasharaMind is an AI business consultant platform for SMEs. This repository is organized as a production-leaning monorepo for the web app, API, background workers, shared packages, and deployment documentation.

## Scope

V1 includes:

- User authentication
- Business profile setup
- Guided assessment
- Rule-based scoring
- AI-assisted priorities and roadmap generation
- Reports and history

## Stack

- Next.js App Router + TypeScript + Tailwind + shadcn/ui
- FastAPI + Pydantic
- PostgreSQL + Supabase
- LangGraph for orchestration
- LangChain for retrieval and tools

## Repository Map

```text
.
|-- apps/
|   |-- api/
|   |-- web/
|   `-- worker/
|-- docs/
|-- infra/
|-- packages/
|   |-- evals/
|   `-- shared/
`-- .env.example
```

## Directory Notes

- `apps/web`: Next.js frontend application.
- `apps/api`: FastAPI service for core backend APIs.
- `apps/worker`: Background jobs and orchestration runtime.
- `packages/shared`: Cross-app types, schemas, and utilities.
- `packages/evals`: Evaluation assets and harnesses for AI quality checks.
- `docs`: Product, architecture, and operational documentation.
- `infra`: Infrastructure and deployment configuration.

## Next Steps

- Add workspace tooling and package management configuration.
- Initialize app-specific build and runtime setup.
- Define shared contracts before implementing business logic.
