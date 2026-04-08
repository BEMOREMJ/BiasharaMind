import { z } from "zod";

import { AnalysisCategoryScoreSchema, PriorityRecommendationSchema } from "./analysis";
import { EntityIdSchema, NonEmptyStringSchema, TimestampSchema } from "./common";
import { RoadmapActionSchema } from "./roadmap";

export const ReportFormatSchema = z.enum(["json", "html", "pdf"]);

export const ReportMetadataSchema = z.object({
  id: EntityIdSchema,
  analysisId: EntityIdSchema,
  format: ReportFormatSchema,
  storagePath: NonEmptyStringSchema.max(240),
  createdAt: TimestampSchema,
});

export const ReportBusinessSummarySchema = z.object({
  businessName: NonEmptyStringSchema.max(120),
  industry: NonEmptyStringSchema.max(80),
  country: NonEmptyStringSchema.max(2),
  sizeBand: NonEmptyStringSchema.max(40),
  teamSize: z.number().int().min(1).max(10000),
  mainGoal: NonEmptyStringSchema.max(240),
});

export const ReportRoadmapPhaseSchema = z.object({
  label: NonEmptyStringSchema.max(40),
  actions: z.array(RoadmapActionSchema).max(10),
});

export const ReportDocumentSchema = ReportMetadataSchema.extend({
  businessSummary: ReportBusinessSummarySchema,
  overallScore: z.number().min(0).max(100),
  categoryScores: z.array(AnalysisCategoryScoreSchema).min(1).max(12),
  strengths: z.array(NonEmptyStringSchema.max(160)).min(1).max(5),
  risks: z.array(NonEmptyStringSchema.max(160)).min(1).max(5),
  priorities: z.array(PriorityRecommendationSchema).min(1).max(5),
  roadmapPhases: z.array(ReportRoadmapPhaseSchema).min(1).max(3),
  exportFileName: NonEmptyStringSchema.max(120),
});

export type ReportBusinessSummary = z.infer<typeof ReportBusinessSummarySchema>;
export type ReportDocument = z.infer<typeof ReportDocumentSchema>;
export type ReportFormat = z.infer<typeof ReportFormatSchema>;
export type ReportMetadata = z.infer<typeof ReportMetadataSchema>;
export type ReportRoadmapPhase = z.infer<typeof ReportRoadmapPhaseSchema>;
