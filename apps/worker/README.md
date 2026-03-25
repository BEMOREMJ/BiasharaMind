# apps/worker

Minimal LangGraph worker scaffold for BiasharaMind.

## Included

- Worker package structure for orchestration code
- Typed workflow state for the V1 business assessment flow
- A single happy-path LangGraph definition
- Placeholder nodes for validation, normalization, retrieval, scoring, insights, prioritization, roadmap creation, and persistence
- Minimal environment-driven settings

## Run

Install dependencies in this app environment, then import or execute the worker entrypoint:

```bash
python -m src.main
```

## Notes

- No real retrieval, scoring, AI generation, or persistence logic is implemented yet.
- The graph is intentionally linear and typed to support future business workflow expansion.
- External task queues and service integrations are intentionally out of scope at this stage.
