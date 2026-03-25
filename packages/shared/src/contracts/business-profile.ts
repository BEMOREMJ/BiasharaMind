import { z } from "zod";

import {
  BudgetBandSchema,
  BusinessSizeBandSchema,
  CountryCodeSchema,
  EntityIdSchema,
  IndustrySchema,
  NonEmptyStringSchema,
  RevenueBandSchema,
  TimestampSchema,
} from "./common";

export const BusinessProfileSchema = z.object({
  id: EntityIdSchema,
  userId: EntityIdSchema,
  businessName: NonEmptyStringSchema.max(120),
  industry: IndustrySchema,
  country: CountryCodeSchema,
  sizeBand: BusinessSizeBandSchema,
  yearsOperating: z.number().int().min(0).max(100),
  revenueBand: RevenueBandSchema,
  teamSize: z.number().int().min(1).max(10000),
  mainGoal: NonEmptyStringSchema.max(240),
  budgetBand: BudgetBandSchema,
  currentTools: z.array(NonEmptyStringSchema.max(80)).max(20),
  createdAt: TimestampSchema,
  updatedAt: TimestampSchema,
});

export type BusinessProfile = z.infer<typeof BusinessProfileSchema>;
