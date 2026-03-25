import { z } from "zod";

import {
  EntityIdSchema,
  NonEmptyStringSchema,
  TimestampSchema,
} from "./common";

export const ReportFormatSchema = z.enum(["pdf", "html"]);

export const ReportMetadataSchema = z.object({
  id: EntityIdSchema,
  analysisId: EntityIdSchema,
  format: ReportFormatSchema,
  storagePath: NonEmptyStringSchema.max(240),
  createdAt: TimestampSchema,
});

export type ReportFormat = z.infer<typeof ReportFormatSchema>;
export type ReportMetadata = z.infer<typeof ReportMetadataSchema>;
