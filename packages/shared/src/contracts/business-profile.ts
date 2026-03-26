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

export const BusinessProfileInputSchema = BusinessProfileSchema.omit({
  id: true,
  userId: true,
  createdAt: true,
  updatedAt: true,
});

export const BusinessProfileCreateSchema = BusinessProfileInputSchema;

export const BusinessProfileUpdateSchema = BusinessProfileInputSchema.partial().refine(
  (value) => Object.keys(value).length > 0,
  {
    message: "At least one business profile field must be provided for updates",
  },
);

export type BusinessProfile = z.infer<typeof BusinessProfileSchema>;
export type BusinessProfileCreate = z.infer<typeof BusinessProfileCreateSchema>;
export type BusinessProfileInput = z.infer<typeof BusinessProfileInputSchema>;
export type BusinessProfileUpdate = z.infer<typeof BusinessProfileUpdateSchema>;
