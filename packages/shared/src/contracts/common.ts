import { z } from "zod";

export const TimestampSchema = z.string().datetime({ offset: true });

export const EntityIdSchema = z
  .string()
  .min(1)
  .max(64)
  .regex(/^[a-zA-Z0-9_-]+$/, "IDs must use letters, numbers, underscores, or hyphens");

export const NonEmptyStringSchema = z.string().trim().min(1);

export const BusinessSizeBandSchema = z.enum([
  "solo",
  "micro",
  "small",
  "medium",
]);

export const RevenueBandSchema = z.enum([
  "pre_revenue",
  "under_10k_usd",
  "10k_to_50k_usd",
  "50k_to_250k_usd",
  "250k_to_1m_usd",
  "over_1m_usd",
]);

export const BudgetBandSchema = z.enum([
  "none",
  "under_500_usd_per_month",
  "500_to_2000_usd_per_month",
  "2000_to_10000_usd_per_month",
  "over_10000_usd_per_month",
]);

export const EffortLevelSchema = z.enum(["low", "medium", "high"]);

export const CostBandSchema = z.enum(["low", "medium", "high"]);

export const ExpectedImpactSchema = z.enum(["low", "medium", "high"]);

export const ScoreSchema = z.number().min(0).max(100);

export const QuestionKeySchema = z
  .string()
  .min(2)
  .max(64)
  .regex(/^[a-z0-9_]+$/, "Question keys must be snake_case");

export const SectionKeySchema = z
  .string()
  .min(2)
  .max(64)
  .regex(/^[a-z0-9_]+$/, "Section keys must be snake_case");

export const IndustrySchema = z.enum([
  "retail",
  "hospitality",
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

export const CountryCodeSchema = z
  .string()
  .length(2)
  .regex(/^[A-Z]{2}$/, "Country must be a 2-letter uppercase code");
