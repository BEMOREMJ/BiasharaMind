import { z } from "zod";

import {
  EntityIdSchema,
  NonEmptyStringSchema,
  QuestionKeySchema,
  SectionKeySchema,
  TimestampSchema,
} from "./common";

export const V2VersionMetadataSchema = z.object({
  questionBankVersion: NonEmptyStringSchema.max(64),
  scoringVersion: NonEmptyStringSchema.max(64),
  taxonomyVersion: NonEmptyStringSchema.max(64),
  promptVersion: NonEmptyStringSchema.max(64).nullable(),
  analysisEngineVersion: NonEmptyStringSchema.max(64),
});

export const V2FreshnessStateSchema = z.enum([
  "fresh",
  "provisional",
  "stale_due_to_profile_change",
  "stale_due_to_assessment_change",
  "stale_due_to_config_change",
  "ai_interpretation_partial",
]);

export const V2RerunRequirementSchema = z.enum(["not_required", "recommended", "required"]);
export const V2RerunReasonSchema = z.enum([
  "none",
  "profile_changed",
  "assessment_changed",
  "config_version_changed",
  "ai_interpretation_incomplete",
  "snapshot_missing",
]);
export const V2AIInterpretationStatusSchema = z.enum([
  "not_requested",
  "pending",
  "complete",
  "partial",
  "failed",
  "fallback_used",
]);
export const V2DiagnosisStateSchema = z.enum(["provisional", "final"]);

export const V2LifecycleStateSchema = z.object({
  freshnessStatus: V2FreshnessStateSchema,
  rerunRequirement: V2RerunRequirementSchema,
  rerunRequired: z.boolean(),
  rerunReason: V2RerunReasonSchema,
  aiInterpretationStatus: V2AIInterpretationStatusSchema,
  diagnosisState: V2DiagnosisStateSchema,
  usableWhileStale: z.boolean(),
  staleExplanation: z.string().trim().max(280).optional().nullable(),
});

export const V2ScaleOptionSchema = z.object({
  value: NonEmptyStringSchema.max(64),
  label: NonEmptyStringSchema.max(120),
  numericValue: z.number().min(0).max(100),
  evidenceHint: z.string().trim().max(240).optional().nullable(),
});

export const V2ScaleDefinitionSchema = z.object({
  key: NonEmptyStringSchema.max(64).regex(/^[a-z0-9_]+$/),
  label: NonEmptyStringSchema.max(120),
  responseType: z.enum(["single_select", "numeric", "free_text"]),
  options: z.array(V2ScaleOptionSchema).max(10),
  minValue: z.number().min(0).max(100).optional().nullable(),
  maxValue: z.number().min(0).max(100).optional().nullable(),
  step: z.number().positive().max(100).optional().nullable(),
});

export const V2BusinessProfileEnumOptionSchema = z.object({
  value: NonEmptyStringSchema.max(64),
  label: NonEmptyStringSchema.max(120),
  description: z.string().trim().max(240).optional().nullable(),
});

export const V2BusinessProfileFieldDefinitionSchema = z.object({
  key: NonEmptyStringSchema.max(64).regex(/^[a-z0-9_]+$/),
  label: NonEmptyStringSchema.max(120),
  fieldType: z.enum(["enum", "multi_enum", "number", "string", "country_code"]),
  required: z.boolean(),
  description: z.string().trim().max(280).optional().nullable(),
  options: z.array(V2BusinessProfileEnumOptionSchema).max(20),
  minValue: z.number().int().min(0).optional().nullable(),
  maxValue: z.number().int().min(0).optional().nullable(),
  routingRelevant: z.boolean(),
});

export const V2PrimaryBusinessTypeSchema = z.enum([
  "retail",
  "food_and_hospitality",
  "services",
  "manufacturing",
  "agriculture",
  "healthcare",
  "education",
  "technology",
  "construction",
  "logistics",
  "other",
]);

export const V2CustomerTypeSchema = z.enum(["b2c", "b2b", "mixed"]);

export const V2SalesChannelSchema = z.enum([
  "walk_in",
  "whatsapp",
  "social_media",
  "phone",
  "website",
  "marketplace",
  "field_sales",
  "referrals",
]);

export const V2FulfilmentModelSchema = z.enum([
  "immediate_delivery",
  "made_to_order",
  "scheduled_service",
  "delivery_or_dispatch",
  "mixed",
]);

export const V2InventoryInvolvementSchema = z.enum(["none", "light", "moderate", "heavy"]);
export const V2CreditSalesExposureSchema = z.enum(["none", "low", "moderate", "high"]);
export const V2BusinessAgeStageSchema = z.enum([
  "starting_out",
  "early_growth",
  "established",
  "mature",
]);
export const V2TeamSizeBandSchema = z.enum([
  "solo",
  "two_to_five",
  "six_to_fifteen",
  "sixteen_to_fifty",
  "over_fifty",
]);
export const V2MonthlyRevenueBandSchema = z.enum([
  "pre_revenue",
  "under_1000_usd",
  "1000_to_5000_usd",
  "5000_to_20000_usd",
  "20000_to_100000_usd",
  "over_100000_usd",
]);
export const V2SeasonalityLevelSchema = z.enum(["low", "moderate", "high"]);
export const V2PeakPeriodSchema = z.enum([
  "month_end",
  "payday_weeks",
  "weekends",
  "holiday_periods",
  "festive_season",
  "back_to_school",
  "harvest_period",
  "tourist_season",
]);
export const V2OwnerInvolvementLevelSchema = z.enum([
  "hands_on_daily",
  "involved_in_key_areas",
  "mostly_delegated",
]);
export const V2PrimaryBusinessGoalSchema = z.enum([
  "grow_sales",
  "improve_cash_flow",
  "improve_efficiency",
  "stabilize_operations",
  "increase_customer_retention",
  "prepare_to_expand",
]);
export const V2TimeCapacitySchema = z.enum(["very_limited", "limited", "moderate", "strong"]);
export const V2BudgetFlexibilitySchema = z.enum(["none", "tight", "moderate", "flexible"]);
export const V2ToolHireOpennessSchema = z.enum(["not_open", "cautiously_open", "open"]);
export const V2RecordAvailabilitySchema = z.enum([
  "minimal",
  "some_manual_records",
  "organized_manual_records",
  "current_digital_records",
]);
export const V2ComplianceSectorSensitivitySchema = z.enum(["moderate", "high"]);

export const V2ImprovementCapacitySchema = z.object({
  timeCapacity: V2TimeCapacitySchema,
  budgetFlexibility: V2BudgetFlexibilitySchema,
  toolHireOpenness: V2ToolHireOpennessSchema,
});

const V2BusinessProfileBaseObjectSchema = z.object({
  businessName: NonEmptyStringSchema.max(120),
  primaryBusinessType: V2PrimaryBusinessTypeSchema,
  mainOffer: NonEmptyStringSchema.max(240),
  customerType: V2CustomerTypeSchema,
  salesChannels: z.array(V2SalesChannelSchema).min(1).max(8),
  fulfilmentModel: V2FulfilmentModelSchema,
  inventoryInvolvement: V2InventoryInvolvementSchema,
  creditSalesExposure: V2CreditSalesExposureSchema,
  businessAgeStage: V2BusinessAgeStageSchema,
  teamSizeBand: V2TeamSizeBandSchema,
  numberOfLocations: z.number().int().min(1).max(500),
  monthlyRevenueBand: V2MonthlyRevenueBandSchema,
  seasonalityLevel: V2SeasonalityLevelSchema.optional().nullable(),
  peakPeriods: z.array(V2PeakPeriodSchema).max(8).optional().nullable(),
  ownerInvolvementLevel: V2OwnerInvolvementLevelSchema,
  primaryBusinessGoal: V2PrimaryBusinessGoalSchema,
  improvementCapacity: V2ImprovementCapacitySchema,
  recordAvailability: V2RecordAvailabilitySchema,
  complianceSectorSensitivity: V2ComplianceSectorSensitivitySchema.optional().nullable(),
});

export const V2BusinessProfileBaseSchema = V2BusinessProfileBaseObjectSchema.superRefine((value, ctx) => {
    if (value.peakPeriods && value.peakPeriods.length > 0 && !value.seasonalityLevel) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "seasonalityLevel is required when peakPeriods are provided",
        path: ["seasonalityLevel"],
      });
    }
  });

export const V2BusinessProfileCreateSchema = V2BusinessProfileBaseSchema;
export const V2BusinessProfileUpdateSchema = V2BusinessProfileBaseSchema;

export const V2BusinessProfileReadSchema = V2BusinessProfileBaseObjectSchema.extend({
  id: EntityIdSchema,
  userId: z.string().trim().min(1).max(128),
  createdAt: TimestampSchema,
  updatedAt: TimestampSchema,
}).superRefine((value, ctx) => {
  if (value.peakPeriods && value.peakPeriods.length > 0 && !value.seasonalityLevel) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: "seasonalityLevel is required when peakPeriods are provided",
      path: ["seasonalityLevel"],
    });
  }
});

export const V2AnalysisImpactSummarySchema = z.object({
  staleAnalysisRuns: z.number().int().min(0),
  rerunRequired: z.boolean(),
  message: z.string().trim().max(240).optional().nullable(),
});

export const V2BusinessProfileSaveResponseSchema = z.object({
  profile: V2BusinessProfileReadSchema,
  analysisImpact: V2AnalysisImpactSummarySchema,
});

export const V2AssessmentStatusSchema = z.enum(["draft", "submitted"]);
export const V2AssessmentResponseKindSchema = z.enum(["answered", "unknown", "prefer_not_to_say"]);

export const V2QuestionOptionSchema = z.object({
  value: NonEmptyStringSchema.max(64),
  label: NonEmptyStringSchema.max(120),
});

export const V2QuestionAnswerSpecSchema = z.object({
  responseType: z.enum(["select", "number", "text", "textarea", "multiselect"]),
  options: z.array(V2QuestionOptionSchema).max(20),
  minValue: z.number().min(0).max(100).optional().nullable(),
  maxValue: z.number().min(0).max(100).optional().nullable(),
  step: z.number().positive().max(100).optional().nullable(),
  allowUnknown: z.boolean(),
  allowPreferNotToSay: z.boolean(),
  maxLength: z.number().int().min(1).max(4000).optional().nullable(),
  multiSelectMaxItems: z.number().int().min(1).max(12).optional().nullable(),
});

export const V2QuestionApplicabilitySchema = z.object({
  sectionId: SectionKeySchema,
  moduleId: NonEmptyStringSchema.max(64).optional().nullable(),
  triggerField: NonEmptyStringSchema.max(64).optional().nullable(),
  triggerValues: z.array(NonEmptyStringSchema.max(64)).max(20),
});

export const V2QuestionDefinitionSchema = z.object({
  questionId: QuestionKeySchema,
  prompt: NonEmptyStringSchema.max(320),
  questionType: z.enum(["select", "number", "text", "textarea", "multiselect"]),
  scaleKey: NonEmptyStringSchema.max(64).optional().nullable(),
  interpretationEnabled: z.boolean(),
  answerSpec: V2QuestionAnswerSpecSchema,
  essential: z.boolean(),
  scored: z.boolean(),
  bucket: NonEmptyStringSchema.max(64),
  helpText: z.string().trim().max(240).optional().nullable(),
  order: z.number().int().min(1).max(200),
  applicability: V2QuestionApplicabilitySchema,
  tags: z.array(NonEmptyStringSchema.max(64)).max(10),
});

export const V2SectionDefinitionSchema = z.object({
  sectionId: SectionKeySchema,
  title: NonEmptyStringSchema.max(120),
  description: NonEmptyStringSchema.max(280),
  order: z.number().int().min(1).max(20),
  isCore: z.boolean(),
  moduleId: NonEmptyStringSchema.max(64).optional().nullable(),
  questions: z.array(V2QuestionDefinitionSchema).min(1).max(40),
});

export const V2AdaptiveModuleSchema = z.object({
  moduleId: NonEmptyStringSchema.max(64),
  title: NonEmptyStringSchema.max(120),
  description: NonEmptyStringSchema.max(280),
  triggerField: NonEmptyStringSchema.max(64),
  triggerValues: z.array(NonEmptyStringSchema.max(64)).min(1).max(20),
  parentSectionKey: SectionKeySchema,
  questionIds: z.array(QuestionKeySchema).max(20),
});

export const V2AssessmentDefinitionSchema = z.object({
  businessProfileV2Id: EntityIdSchema,
  questionBankVersion: NonEmptyStringSchema.max(64),
  sections: z.array(V2SectionDefinitionSchema).min(1).max(20),
  adaptiveModules: z.array(V2AdaptiveModuleSchema).max(10),
  totalQuestions: z.number().int().min(1).max(200),
});

export const V2AssessmentAnswerValueSchema = z.union([
  z.string(),
  z.number(),
  z.array(z.string()),
  z.null(),
]);

export const V2AssessmentAnswerPayloadSchema = z.object({
  questionId: QuestionKeySchema,
  answerType: z.enum(["select", "number", "text", "textarea", "multiselect"]),
  responseKind: V2AssessmentResponseKindSchema,
  value: V2AssessmentAnswerValueSchema.optional().nullable(),
}).superRefine((value, ctx) => {
  if (value.responseKind === "answered" && (value.value === null || value.value === undefined)) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: "answered responses require a value",
      path: ["value"],
    });
  }

  if (value.responseKind !== "answered" && value.value !== null && value.value !== undefined) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: "unknown and prefer_not_to_say responses cannot include a value",
      path: ["value"],
    });
  }
});

export const V2AssessmentWritePayloadSchema = z.object({
  answers: z.array(V2AssessmentAnswerPayloadSchema).max(200),
});

export const V2AssessmentAnswerReadSchema = z.object({
  questionId: QuestionKeySchema,
  sectionId: SectionKeySchema,
  moduleId: NonEmptyStringSchema.max(64).optional().nullable(),
  answerType: z.enum(["select", "number", "text", "textarea", "multiselect"]),
  responseKind: V2AssessmentResponseKindSchema,
  value: V2AssessmentAnswerValueSchema.optional().nullable(),
  isSufficientAnswer: z.boolean().optional().nullable(),
  orderIndex: z.number().int().min(0).max(500).optional().nullable(),
});

export const V2AssessmentReadSchema = z.object({
  id: EntityIdSchema,
  businessProfileV2Id: EntityIdSchema.optional().nullable(),
  questionBankVersion: NonEmptyStringSchema.max(64),
  status: V2AssessmentStatusSchema,
  completenessHint: z.string().trim().max(64).optional().nullable(),
  latestDefinitionSnapshot: z.record(z.any()).optional().nullable(),
  startedAt: TimestampSchema,
  submittedAt: TimestampSchema.optional().nullable(),
  answers: z.array(V2AssessmentAnswerReadSchema).max(200),
});

export const V2AssessmentSaveResponseSchema = z.object({
  assessment: V2AssessmentReadSchema,
  analysisImpact: V2AnalysisImpactSummarySchema,
});

export const V2HealthStatusSchema = z.enum([
  "strong_and_controlled",
  "stable_but_constrained",
  "vulnerable",
  "fragile",
  "critical",
]);

export const V2CoverageLabelSchema = z.enum([
  "high_coverage",
  "good_coverage",
  "partial_coverage",
  "low_coverage",
]);

export const V2ConfidenceLabelSchema = z.enum([
  "high_confidence",
  "moderate_confidence",
  "low_confidence",
]);

export const V2BucketScoreSchema = z.object({
  bucket: NonEmptyStringSchema.max(32),
  score: z.number().min(0).max(100),
  contributingQuestionCount: z.number().int().min(0).max(100),
});

export const V2SectionScoreSchema = z.object({
  sectionId: SectionKeySchema,
  title: NonEmptyStringSchema.max(120),
  score: z.number().min(0).max(100),
  bucketScores: z.array(V2BucketScoreSchema).max(3),
  completeness: z.number().min(0).max(100),
  completenessLabel: V2CoverageLabelSchema,
  evidenceConfidence: z.number().min(0).max(100),
  moduleContributionScore: z.number().min(0).max(100).optional().nullable(),
  moduleContributionWeight: z.number().min(0).max(1).optional().nullable(),
});

export const V2CompletenessSummarySchema = z.object({
  overall: z.number().min(0).max(100),
  label: V2CoverageLabelSchema,
  essentialAnsweredSufficiently: z.number().int().min(0).max(500),
  essentialApplicable: z.number().int().min(0).max(500),
  optionalAnsweredSufficiently: z.number().int().min(0).max(500),
  optionalApplicable: z.number().int().min(0).max(500),
});

export const V2EvidenceConfidenceSummarySchema = z.object({
  score: z.number().min(0).max(100),
  label: V2ConfidenceLabelSchema,
  specificity: z.number().min(0).max(100),
  quantification: z.number().min(0).max(100),
  internalConsistency: z.number().min(0).max(100),
  corroboration: z.number().min(0).max(100),
  keyLimitations: z.array(NonEmptyStringSchema.max(320)).max(20),
});

export const V2StatusCapResultSchema = z.object({
  code: NonEmptyStringSchema.max(64),
  label: NonEmptyStringSchema.max(160),
  cappedStatus: V2HealthStatusSchema,
  reason: NonEmptyStringSchema.max(320),
});

export const V2AnalysisScoreSummarySchema = z.object({
  overallHealthScore: z.number().min(0).max(100),
  overallStatus: V2HealthStatusSchema,
  sectionScores: z.array(V2SectionScoreSchema).max(20),
  completeness: V2CompletenessSummarySchema,
  evidenceConfidence: V2EvidenceConfidenceSummarySchema,
  activeCriticalRiskCount: z.number().int().min(0).max(100),
  capsApplied: z.array(V2StatusCapResultSchema).max(10),
});

export const V2IssueTagSchema = z.object({
  code: NonEmptyStringSchema.max(64),
  label: NonEmptyStringSchema.max(120),
  confidence: z.number().min(0).max(1),
});

export const V2RootCauseTagSchema = z.object({
  code: NonEmptyStringSchema.max(64),
  label: NonEmptyStringSchema.max(120),
  confidence: z.number().min(0).max(1),
});

export const V2ContradictionFlagSchema = z.object({
  code: NonEmptyStringSchema.max(64),
  detail: NonEmptyStringSchema.max(320),
  severity: z.enum(["low", "medium", "high"]),
  sourceRefs: z.array(NonEmptyStringSchema.max(120)).max(10),
});

export const V2InterpretationFallbackSchema = z.object({
  used: z.boolean(),
  reason: z.string().trim().max(200).optional().nullable(),
  partial: z.boolean(),
  recoverable: z.boolean(),
});

export const V2TextInterpretationOutputSchema = z.object({
  questionKey: QuestionKeySchema,
  sectionKey: SectionKeySchema,
  summary: z.string().trim().max(500).optional().nullable(),
  issueTags: z.array(V2IssueTagSchema).max(10),
  rootCauseTags: z.array(V2RootCauseTagSchema).max(10),
  affectedDimensions: z.array(NonEmptyStringSchema.max(64)).max(10),
  severityHint: z.enum(["low", "medium", "high", "critical"]).optional().nullable(),
  contradictionFlags: z.array(V2ContradictionFlagSchema).max(10),
  evidenceSpecificity: z.enum(["low", "medium", "high"]).optional().nullable(),
  evidenceStrength: z.enum(["weak", "mixed", "strong"]).optional().nullable(),
  interpretationConfidence: z.enum(["low", "medium", "high"]).optional().nullable(),
  evidenceSnippets: z.array(z.string().trim().max(240)).max(5),
  fallback: V2InterpretationFallbackSchema,
});

export const V2TextInterpretationInputSchema = z.object({
  questionKey: QuestionKeySchema,
  sectionKey: SectionKeySchema,
  answerText: z.string().trim().min(1).max(4000),
  businessProfileContext: z.record(z.any()),
  sourceRef: z.string().trim().max(120).optional().nullable(),
});

export const V2TextInterpretationSnapshotSchema = z.object({
  status: V2AIInterpretationStatusSchema,
  promptVersion: z.string().trim().max(64).optional().nullable(),
  providerName: z.string().trim().max(64).optional().nullable(),
  inputs: z.array(V2TextInterpretationInputSchema).max(200),
  outputs: z.array(V2TextInterpretationOutputSchema).max(200),
});

export const V2ScoreDriverSchema = z.object({
  code: NonEmptyStringSchema.max(64),
  label: NonEmptyStringSchema.max(140),
  direction: NonEmptyStringSchema.max(20),
  detail: NonEmptyStringSchema.max(320),
  evidenceRefs: z.array(NonEmptyStringSchema.max(120)).max(10),
});

export const V2AppliedCapSchema = z.object({
  code: NonEmptyStringSchema.max(64),
  label: NonEmptyStringSchema.max(140),
  reason: NonEmptyStringSchema.max(320),
  cappedTo: z.number().min(0).max(100).optional().nullable(),
});

export const V2EvidenceGapSchema = z.object({
  area: NonEmptyStringSchema.max(140),
  detail: NonEmptyStringSchema.max(320),
  severity: NonEmptyStringSchema.max(20),
});

export const V2ConfidenceLimitationSchema = z.object({
  code: NonEmptyStringSchema.max(64),
  detail: NonEmptyStringSchema.max(320),
  impact: NonEmptyStringSchema.max(200),
});

export const V2PriorityRationaleSchema = z.object({
  priorityCode: NonEmptyStringSchema.max(64),
  summary: NonEmptyStringSchema.max(320),
  contributingIssueCodes: z.array(NonEmptyStringSchema.max(64)).max(10),
  contributingRiskCodes: z.array(NonEmptyStringSchema.max(64)).max(10),
});

export const V2WatchlistRationaleSchema = z.object({
  watchlistCode: NonEmptyStringSchema.max(64),
  summary: NonEmptyStringSchema.max(320),
  triggerCondition: NonEmptyStringSchema.max(200),
});

export const V2ExplainabilitySchema = z.object({
  scoreDrivers: z.array(V2ScoreDriverSchema).max(20),
  capsApplied: z.array(V2AppliedCapSchema).max(20),
  missingOrWeakEvidence: z.array(V2EvidenceGapSchema).max(20),
  confidenceLimitations: z.array(V2ConfidenceLimitationSchema).max(20),
  priorityRationales: z.array(V2PriorityRationaleSchema).max(20),
  watchlistRationales: z.array(V2WatchlistRationaleSchema).max(20),
});

export const V2CriticalRiskSchema = z.object({
  code: NonEmptyStringSchema.max(64),
  title: NonEmptyStringSchema.max(160),
  severity: NonEmptyStringSchema.max(32),
  evidenceQuestionIds: z.array(QuestionKeySchema).max(20),
  evidenceSummary: NonEmptyStringSchema.max(320),
  recommendedActionFamilies: z.array(NonEmptyStringSchema.max(64)).max(10),
});

export const V2IssueCandidateSchema = z.object({
  issueCode: NonEmptyStringSchema.max(64),
  title: NonEmptyStringSchema.max(160),
  dimension: NonEmptyStringSchema.max(64),
  evidenceQuestionIds: z.array(QuestionKeySchema).max(20),
  evidenceSummary: NonEmptyStringSchema.max(400),
  severityScore: z.number().min(0).max(100),
  urgencyScore: z.number().min(0).max(100),
  impactScore: z.number().min(0).max(100),
  feasibilityScore: z.number().min(0).max(100),
  leverageScore: z.number().min(0).max(100),
  confidenceScore: z.number().min(0).max(100),
  criticalRiskLinks: z.array(NonEmptyStringSchema.max(64)).max(10),
  recommendedActionFamily: NonEmptyStringSchema.max(64),
  dependencies: z.array(NonEmptyStringSchema.max(200)).max(10),
  goalFitAdjustment: z.number().min(0.8).max(1.2),
  priorityScore: z.number().min(0).max(100),
  adjustedPriorityScore: z.number().min(0).max(120),
});

export const V2PriorityItemSchema = z.object({
  issueCode: NonEmptyStringSchema.max(64),
  title: NonEmptyStringSchema.max(160),
  recommendedActionFamily: NonEmptyStringSchema.max(64),
  adjustedPriorityScore: z.number().min(0).max(120),
  whySelected: NonEmptyStringSchema.max(400),
  sequencingNotes: z.array(NonEmptyStringSchema.max(240)).max(8),
  dependencies: z.array(NonEmptyStringSchema.max(200)).max(10),
  criticalRiskLinks: z.array(NonEmptyStringSchema.max(64)).max(10),
  suggestedSuccessMetrics: z.array(NonEmptyStringSchema.max(200)).max(6),
});

export const V2WatchlistItemSchema = z.object({
  issueCode: NonEmptyStringSchema.max(64),
  title: NonEmptyStringSchema.max(160),
  recommendedActionFamily: NonEmptyStringSchema.max(64),
  adjustedPriorityScore: z.number().min(0).max(120),
  watchlistReason: NonEmptyStringSchema.max(320),
  criticalRiskLinks: z.array(NonEmptyStringSchema.max(64)).max(10),
});

export const V2DiagnosisSummarySchema = z.object({
  strongestAreas: z.array(NonEmptyStringSchema.max(160)).max(3),
  weakestAreas: z.array(NonEmptyStringSchema.max(160)).max(3),
  primaryBottleneck: z.string().trim().max(160).optional().nullable(),
  topConstraints: z.array(NonEmptyStringSchema.max(160)).max(5),
  rootCausePatterns: z.array(NonEmptyStringSchema.max(240)).max(5),
});

export const V2RoadmapInputItemSchema = z.object({
  issueCode: NonEmptyStringSchema.max(64),
  actionFamily: NonEmptyStringSchema.max(64),
  dependencies: z.array(NonEmptyStringSchema.max(200)).max(10),
  feasibilityContext: NonEmptyStringSchema.max(320),
  suggestedSuccessMetrics: z.array(NonEmptyStringSchema.max(200)).max(6),
  sequencingNotes: z.array(NonEmptyStringSchema.max(240)).max(8),
});

export const V2RoadmapInputPackageSchema = z.object({
  selectedActionFamilies: z.array(NonEmptyStringSchema.max(64)).max(10),
  dependencies: z.array(NonEmptyStringSchema.max(200)).max(20),
  feasibilityContext: z.array(NonEmptyStringSchema.max(320)).max(10),
  suggestedSuccessMetrics: z.array(NonEmptyStringSchema.max(200)).max(12),
  sequencingNotes: z.array(NonEmptyStringSchema.max(240)).max(12),
  items: z.array(V2RoadmapInputItemSchema).max(5),
});

export const V2AnalysisRunSchema = z.object({
  id: EntityIdSchema,
  analysisFamily: NonEmptyStringSchema.max(64),
  metadata: V2VersionMetadataSchema,
  lifecycle: V2LifecycleStateSchema,
  summary: V2AnalysisScoreSummarySchema,
  criticalRisks: z.array(V2CriticalRiskSchema).max(10),
  diagnosis: V2DiagnosisSummarySchema,
  issueCandidates: z.array(V2IssueCandidateSchema).max(20),
  topPriorities: z.array(V2PriorityItemSchema).max(3),
  watchlist: z.array(V2WatchlistItemSchema).max(2),
  roadmapInputs: V2RoadmapInputPackageSchema,
  textInterpretation: V2TextInterpretationSnapshotSchema,
  explainability: V2ExplainabilitySchema,
  createdAt: TimestampSchema,
});

export const V2SnapshotMetadataSchema = z.object({
  metadata: V2VersionMetadataSchema,
  lifecycle: V2LifecycleStateSchema,
  sourceEntities: z.object({
    analysisRunId: z.string().trim().max(64).optional().nullable(),
    userId: z.string().trim().max(128).optional().nullable(),
    businessProfileId: z.string().trim().max(64).optional().nullable(),
    assessmentId: z.string().trim().max(64).optional().nullable(),
  }),
});

export const V2SnapshotEnvelopeSchema = V2SnapshotMetadataSchema.extend({
  businessProfile: z.object({
    values: z.record(z.union([z.string(), z.number().int(), z.array(z.string())])),
  }),
  assessmentSubmission: z.object({
    sections: z.array(SectionKeySchema).max(20),
    answers: z
      .array(
        z.object({
          questionKey: QuestionKeySchema,
          sectionKey: SectionKeySchema,
          answerType: NonEmptyStringSchema.max(32),
          value: z.union([z.string(), z.number(), z.array(z.string())]),
        }),
      )
      .max(200),
  }),
  textInterpretation: z.object({
    outputs: z.array(V2TextInterpretationOutputSchema).max(200),
  }),
  explainability: V2ExplainabilitySchema,
});

export type V2AIInterpretationStatus = z.infer<typeof V2AIInterpretationStatusSchema>;
export type V2AnalysisImpactSummary = z.infer<typeof V2AnalysisImpactSummarySchema>;
export type V2AnalysisRun = z.infer<typeof V2AnalysisRunSchema>;
export type V2AnalysisScoreSummary = z.infer<typeof V2AnalysisScoreSummarySchema>;
export type V2AssessmentAnswerPayload = z.infer<typeof V2AssessmentAnswerPayloadSchema>;
export type V2AssessmentAnswerRead = z.infer<typeof V2AssessmentAnswerReadSchema>;
export type V2AssessmentAnswerValue = z.infer<typeof V2AssessmentAnswerValueSchema>;
export type V2AssessmentDefinition = z.infer<typeof V2AssessmentDefinitionSchema>;
export type V2AssessmentRead = z.infer<typeof V2AssessmentReadSchema>;
export type V2AssessmentResponseKind = z.infer<typeof V2AssessmentResponseKindSchema>;
export type V2AssessmentSaveResponse = z.infer<typeof V2AssessmentSaveResponseSchema>;
export type V2AssessmentStatus = z.infer<typeof V2AssessmentStatusSchema>;
export type V2AssessmentWritePayload = z.infer<typeof V2AssessmentWritePayloadSchema>;
export type V2AdaptiveModule = z.infer<typeof V2AdaptiveModuleSchema>;
export type V2BucketScore = z.infer<typeof V2BucketScoreSchema>;
export type V2BudgetFlexibility = z.infer<typeof V2BudgetFlexibilitySchema>;
export type V2BusinessAgeStage = z.infer<typeof V2BusinessAgeStageSchema>;
export type V2BusinessProfileCreate = z.infer<typeof V2BusinessProfileCreateSchema>;
export type V2BusinessProfileFieldDefinition = z.infer<typeof V2BusinessProfileFieldDefinitionSchema>;
export type V2BusinessProfileRead = z.infer<typeof V2BusinessProfileReadSchema>;
export type V2BusinessProfileSaveResponse = z.infer<typeof V2BusinessProfileSaveResponseSchema>;
export type V2BusinessProfileUpdate = z.infer<typeof V2BusinessProfileUpdateSchema>;
export type V2CompletenessSummary = z.infer<typeof V2CompletenessSummarySchema>;
export type V2ComplianceSectorSensitivity = z.infer<typeof V2ComplianceSectorSensitivitySchema>;
export type V2ConfidenceLabel = z.infer<typeof V2ConfidenceLabelSchema>;
export type V2CriticalRisk = z.infer<typeof V2CriticalRiskSchema>;
export type V2CustomerType = z.infer<typeof V2CustomerTypeSchema>;
export type V2CoverageLabel = z.infer<typeof V2CoverageLabelSchema>;
export type V2DiagnosisSummary = z.infer<typeof V2DiagnosisSummarySchema>;
export type V2EvidenceConfidenceSummary = z.infer<typeof V2EvidenceConfidenceSummarySchema>;
export type V2Explainability = z.infer<typeof V2ExplainabilitySchema>;
export type V2FreshnessState = z.infer<typeof V2FreshnessStateSchema>;
export type V2HealthStatus = z.infer<typeof V2HealthStatusSchema>;
export type V2ImprovementCapacity = z.infer<typeof V2ImprovementCapacitySchema>;
export type V2IssueCandidate = z.infer<typeof V2IssueCandidateSchema>;
export type V2LifecycleState = z.infer<typeof V2LifecycleStateSchema>;
export type V2PrimaryBusinessGoal = z.infer<typeof V2PrimaryBusinessGoalSchema>;
export type V2PrimaryBusinessType = z.infer<typeof V2PrimaryBusinessTypeSchema>;
export type V2PriorityItem = z.infer<typeof V2PriorityItemSchema>;
export type V2QuestionAnswerSpec = z.infer<typeof V2QuestionAnswerSpecSchema>;
export type V2QuestionApplicability = z.infer<typeof V2QuestionApplicabilitySchema>;
export type V2QuestionDefinition = z.infer<typeof V2QuestionDefinitionSchema>;
export type V2QuestionOption = z.infer<typeof V2QuestionOptionSchema>;
export type V2RecordAvailability = z.infer<typeof V2RecordAvailabilitySchema>;
export type V2RoadmapInputItem = z.infer<typeof V2RoadmapInputItemSchema>;
export type V2RoadmapInputPackage = z.infer<typeof V2RoadmapInputPackageSchema>;
export type V2SalesChannel = z.infer<typeof V2SalesChannelSchema>;
export type V2SectionDefinition = z.infer<typeof V2SectionDefinitionSchema>;
export type V2SectionScore = z.infer<typeof V2SectionScoreSchema>;
export type V2SnapshotEnvelope = z.infer<typeof V2SnapshotEnvelopeSchema>;
export type V2SnapshotMetadata = z.infer<typeof V2SnapshotMetadataSchema>;
export type V2StatusCapResult = z.infer<typeof V2StatusCapResultSchema>;
export type V2TeamSizeBand = z.infer<typeof V2TeamSizeBandSchema>;
export type V2TextInterpretationOutput = z.infer<typeof V2TextInterpretationOutputSchema>;
export type V2TextInterpretationInput = z.infer<typeof V2TextInterpretationInputSchema>;
export type V2TextInterpretationSnapshot = z.infer<typeof V2TextInterpretationSnapshotSchema>;
export type V2TimeCapacity = z.infer<typeof V2TimeCapacitySchema>;
export type V2ToolHireOpenness = z.infer<typeof V2ToolHireOpennessSchema>;
export type V2VersionMetadata = z.infer<typeof V2VersionMetadataSchema>;
export type V2WatchlistItem = z.infer<typeof V2WatchlistItemSchema>;
