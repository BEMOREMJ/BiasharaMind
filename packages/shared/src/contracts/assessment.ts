import { z } from "zod";

import {
  EntityIdSchema,
  NonEmptyStringSchema,
  QuestionKeySchema,
  ScoreSchema,
  SectionKeySchema,
  TimestampSchema,
} from "./common";

export const AssessmentStatusSchema = z.enum([
  "not_started",
  "in_progress",
  "submitted",
  "analyzed",
]);

export const AssessmentAnswerTypeSchema = z.enum([
  "single_select",
  "multi_select",
  "boolean",
  "number",
  "text",
]);

export const AssessmentOptionSchema = z.object({
  label: NonEmptyStringSchema.max(100),
  value: NonEmptyStringSchema.max(100),
});

export const AssessmentSectionSchema = z.object({
  key: SectionKeySchema,
  title: NonEmptyStringSchema.max(120),
  description: NonEmptyStringSchema.max(280),
  order: z.number().int().min(1).max(50),
});

export const AssessmentQuestionSchema = z
  .object({
    key: QuestionKeySchema,
    sectionKey: SectionKeySchema,
    prompt: NonEmptyStringSchema.max(320),
    answerType: AssessmentAnswerTypeSchema,
    required: z.boolean(),
    options: z.array(AssessmentOptionSchema).max(12).optional(),
    helpText: z.string().trim().max(240).optional(),
  })
  .superRefine((value, ctx) => {
    const optionsRequired =
      value.answerType === "single_select" || value.answerType === "multi_select";

    if (optionsRequired && (!value.options || value.options.length === 0)) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "Options are required for select-based questions",
        path: ["options"],
      });
    }

    if (!optionsRequired && value.options && value.options.length > 0) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "Options are only allowed for select-based questions",
        path: ["options"],
      });
    }
  });

const AnswerScalarValueSchema = z.union([
  z.boolean(),
  z.number(),
  z.string().trim().min(1).max(500),
]);

export const AssessmentAnswerValueSchema = z.union([
  AnswerScalarValueSchema,
  z.array(z.string().trim().min(1).max(100)).min(1).max(12),
]);

export const AssessmentAnswerSchema = z
  .object({
    questionKey: QuestionKeySchema,
    sectionKey: SectionKeySchema,
    answerType: AssessmentAnswerTypeSchema,
    value: AssessmentAnswerValueSchema,
  })
  .superRefine((value, ctx) => {
    const isArray = Array.isArray(value.value);
    const isString = typeof value.value === "string";
    const isNumber = typeof value.value === "number";
    const isBoolean = typeof value.value === "boolean";

    if (value.answerType === "multi_select" && !isArray) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "multi_select answers must use an array of values",
        path: ["value"],
      });
    }

    if (value.answerType === "single_select" && !isString) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "single_select answers must use a single string value",
        path: ["value"],
      });
    }

    if (value.answerType === "text" && !isString) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "text answers must use a string value",
        path: ["value"],
      });
    }

    if (value.answerType === "number" && !isNumber) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "number answers must use a numeric value",
        path: ["value"],
      });
    }

    if (value.answerType === "boolean" && !isBoolean) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "boolean answers must use a boolean value",
        path: ["value"],
      });
    }
  });

export const AssessmentSchema = z.object({
  id: EntityIdSchema,
  businessId: EntityIdSchema,
  status: AssessmentStatusSchema,
  version: NonEmptyStringSchema.max(32),
  startedAt: TimestampSchema,
  submittedAt: TimestampSchema.nullable(),
  sections: z.array(AssessmentSectionSchema).min(1).max(12),
});

export const AssessmentCategoryScoreSchema = z.object({
  sectionKey: SectionKeySchema,
  label: NonEmptyStringSchema.max(120),
  score: ScoreSchema,
});

export type Assessment = z.infer<typeof AssessmentSchema>;
export type AssessmentAnswer = z.infer<typeof AssessmentAnswerSchema>;
export type AssessmentAnswerType = z.infer<typeof AssessmentAnswerTypeSchema>;
export type AssessmentCategoryScore = z.infer<typeof AssessmentCategoryScoreSchema>;
export type AssessmentOption = z.infer<typeof AssessmentOptionSchema>;
export type AssessmentQuestion = z.infer<typeof AssessmentQuestionSchema>;
export type AssessmentSection = z.infer<typeof AssessmentSectionSchema>;
export type AssessmentStatus = z.infer<typeof AssessmentStatusSchema>;
