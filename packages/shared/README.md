# packages/shared

Framework-agnostic shared contracts for BiasharaMind V1.

## Purpose

This package defines stable data contracts used across services:

- Frontend uses the schemas and inferred types to drive forms, client-side validation, and typed API consumption.
- Backend uses the same schemas to validate request and response payloads at service boundaries.
- Worker services use the contracts for orchestration inputs, analysis outputs, roadmap generation, and report metadata.

## Conventions

- Zod schemas are the source of truth.
- TypeScript types are inferred from schemas and exported alongside them.
- Domain files are organized by business area instead of one large shared file.
- Enum-like fields are constrained explicitly to keep V1 payloads stable.
- Optional and nullable fields are used intentionally; most persisted V1 entities require explicit values.

## Layout

```text
src/
|-- contracts/
|   |-- analysis.ts
|   |-- assessment.ts
|   |-- business-profile.ts
|   |-- common.ts
|   |-- report.ts
|   `-- roadmap.ts
|-- examples/
|   |-- analysis-summary.example.ts
|   |-- assessment-answers.example.ts
|   |-- business-profile.example.ts
|   `-- roadmap.example.ts
`-- index.ts
```

## Usage

Import from the package entrypoint:

```ts
import {
  BusinessProfileSchema,
  type BusinessProfile,
  exampleBusinessProfile,
} from "@biasharamind/shared";
```

Parse external input with schemas and pass inferred types through application code.
