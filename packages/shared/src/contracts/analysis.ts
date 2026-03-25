import { z } from "zod";

import {
  CostBandSchema,
  EffortLevelSchema,
  EntityIdSchema,
  ExpectedImpactSchema,
  NonEmptyStringSchema,
  ScoreSchema,
  SectionKeySchema,
  TimestampSchema,
} from "./common";

export const PriorityRecommendationSchema = z.object({
  title: NonEmptyStringSchema.max(140),
  why: NonEmptyStringSchema.max(400),
  effort: EffortLevelSchema,
  costBand: CostBandSchema,
  expectedImpact: ExpectedImpactSchema,
});

export const AnalysisCategoryScoreSchema = z.object({
  sectionKey: SectionKeySchema,
  label: NonEmptyStringSchema.max(120),
  score: ScoreSchema,
});

export const AnalysisSummarySchema = z.object({
  id: EntityIdSchema,
  assessmentId: EntityIdSchema,
  overallScore: ScoreSchema,
  categoryScores: z.array(AnalysisCategoryScoreSchema).min(1).max(12),
  topStrengths: z.array(NonEmptyStringSchema.max(160)).min(1).max(5),
  topRisks: z.array(NonEmptyStringSchema.max(160)).min(1).max(5),
  topPriorities: z.array(PriorityRecommendationSchema).min(1).max(5),
  createdAt: TimestampSchema,
  modelVersion: NonEmptyStringSchema.max(64),
  workflowVersion: NonEmptyStringSchema.max(64),
});

export type AnalysisCategoryScore = z.infer<typeof AnalysisCategoryScoreSchema>;
export type AnalysisSummary = z.infer<typeof AnalysisSummarySchema>;
export type PriorityRecommendation = z.infer<typeof PriorityRecommendationSchema>;
