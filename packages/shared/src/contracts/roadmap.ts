import { z } from "zod";

import {
  CostBandSchema,
  EffortLevelSchema,
  EntityIdSchema,
  ExpectedImpactSchema,
  NonEmptyStringSchema,
  TimestampSchema,
} from "./common";

export const RoadmapActionSchema = z.object({
  title: NonEmptyStringSchema.max(140),
  description: NonEmptyStringSchema.max(400),
  whyItMatters: NonEmptyStringSchema.max(240),
  effort: EffortLevelSchema,
  costBand: CostBandSchema,
  expectedImpact: ExpectedImpactSchema,
});

const RoadmapActionListSchema = z.array(RoadmapActionSchema).max(10);

export const RoadmapSchema = z.object({
  id: EntityIdSchema,
  analysisId: EntityIdSchema,
  days0to30: RoadmapActionListSchema,
  days31to60: RoadmapActionListSchema,
  days61to90: RoadmapActionListSchema,
  createdAt: TimestampSchema,
});

export type Roadmap = z.infer<typeof RoadmapSchema>;
export type RoadmapAction = z.infer<typeof RoadmapActionSchema>;
