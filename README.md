# BiasharaMind

BiasharaMind is an AI business consultant platform for SMEs. This repository is organized as a production-leaning monorepo for the web app, API, background workers, shared packages, and deployment documentation.

## Current Status

The project has moved beyond the initial scaffold and now includes an end-to-end V1 foundation across the frontend, API, shared contracts, and database layer.

Implemented so far:

- Marketing, auth, and dashboard route groups in the Next.js web app
- Shared Zod contracts and example payloads in `packages/shared`
- FastAPI domain routes for business profile, assessment, analysis, roadmap, and reports
- Deterministic V1 analysis scoring in the API layer
- Initial PostgreSQL persistence models and Alembic migration for core entities
- LangGraph worker scaffold for the future orchestration flow

Still in progress:

- Wiring the worker graph to the same deterministic scoring logic
- Real retrieval and AI generation inside the worker
- Full production auth and cross-service orchestration

## V1 Scope

V1 currently targets:

- Business profile setup
- Guided assessment capture and submission
- Deterministic scoring and analysis summaries
- Priority recommendations based on rule-based thresholds
- Roadmap and report data structures
- Assessment and analysis history foundations

## Stack

- Next.js App Router + TypeScript + Tailwind + shadcn/ui
- FastAPI + Pydantic
- PostgreSQL + Supabase
- LangGraph for orchestration
- LangChain for retrieval and tools

## Repository Map

```text
.
|-- .editorconfig
|-- .gitignore
|-- apps/
|   |-- api/
|   |-- web/
|   `-- worker/
|-- docs/
|-- infra/
|-- package.json
|-- packages/
|   |-- evals/
|   `-- shared/
|-- pnpm-workspace.yaml
|-- tsconfig.base.json
`-- .env.example
```

## Directory Notes

- `apps/web`: Next.js frontend application for marketing, auth, assessment, dashboard, roadmap, and history experiences.
- `apps/api`: FastAPI backend with domain routes, services, repositories, SQLAlchemy models, and Alembic migrations.
- `apps/worker`: LangGraph worker scaffold for assessment workflow orchestration. The graph is present, but scoring and generation nodes are still mostly placeholders.
- `packages/shared`: Cross-app schemas, contracts, and example payloads shared by the frontend and backend.
- `packages/evals`: Evaluation assets and harnesses for AI quality checks.
- `docs`: Product, architecture, and operational documentation.
- `infra`: Infrastructure and deployment configuration.

## Deterministic Scoring

Deterministic scoring is currently implemented in `apps/api/app/services/analysis_service.py`.

Today that logic includes:

- Rule-based scoring for select-answer questions
- Numeric scoring normalization for key business metrics
- Text-response scoring based on answer completeness
- Section/category score aggregation
- Overall score calculation
- Rule-based strengths, risks, and priority recommendation generation

Current implementation note:

- The deterministic scoring logic runs through the API analysis service.
- The worker node at `apps/worker/src/nodes/score_assessment.py` is still a placeholder and has not yet been updated to reuse the same rules.

## Local Setup

### JavaScript and TypeScript workspace

The repo uses `pnpm` workspaces for the frontend and shared TypeScript package.

```bash
pnpm install
```

Useful root commands:

- `pnpm dev:web`: run the Next.js frontend
- `pnpm build:web`: build the frontend
- `pnpm lint:web`: run frontend linting
- `pnpm typecheck:web`: run TypeScript checks for `apps/web`
- `pnpm typecheck:shared`: run TypeScript checks for `packages/shared`

### Python apps

The Python services remain independent for now:

- `apps/api`: FastAPI service with its own `pyproject.toml`
- `apps/worker`: LangGraph worker with its own `pyproject.toml`

Set up and run those apps in their own Python environments.

Typical app entrypoints:

```bash
uvicorn app.main:app --reload
```

```bash
python -m src.main
```

## Data Layer Progress

The API now includes an initial Alembic migration for PostgreSQL persistence covering:

- `business_profiles`
- `assessments`
- `assessment_answers`
- `analyses`
- `roadmaps`
- `reports`

This establishes the core schema for the V1 workflow even though some application flows are still using deterministic or scaffolded service logic.

## Working Areas

- `apps/web`: Next.js App Router frontend for the main product journey.
- `packages/shared`: Installable workspace package published internally as `@biasharamind/shared`.
- `apps/api` and `apps/worker`: Python projects kept separate until cross-language tooling needs justify more coordination.

## Current Tooling Scope

- `pnpm` workspace management for web and shared TypeScript code
- Shared schema package used across frontend and backend boundaries
- FastAPI service structure with domain routes, services, repositories, and persistence models
- Initial PostgreSQL migration support through Alembic
- LangGraph workflow scaffold ready for future orchestration work
- No Turbo, Nx, Docker, or CI pipeline yet
