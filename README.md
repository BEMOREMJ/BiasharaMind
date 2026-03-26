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

- `apps/web`: Next.js frontend application.
- `apps/api`: FastAPI service for core backend APIs.
- `apps/worker`: Background jobs and orchestration runtime.
- `packages/shared`: Cross-app types, schemas, and utilities.
- `packages/evals`: Evaluation assets and harnesses for AI quality checks.
- `docs`: Product, architecture, and operational documentation.
- `infra`: Infrastructure and deployment configuration.

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

Set up and run those apps in their own Python environments. They are intentionally not managed by the root JS workspace.

## Working Areas

- `apps/web`: Next.js App Router frontend. This is the only app currently connected to the root workspace.
- `packages/shared`: Installable workspace package published internally as `@biasharamind/shared`.
- `apps/api` and `apps/worker`: Python projects kept separate until cross-language tooling needs justify more coordination.

## Current Tooling Scope

- Minimal `pnpm` workspace management for web and shared TypeScript code
- Root ignore and editor settings for consistent local development
- Lightweight package linking between `apps/web` and `packages/shared`
- No Turbo, Nx, Docker, CI, or cross-language orchestration tooling yet
