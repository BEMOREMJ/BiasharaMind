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

export const AssessmentAnswerTypeSchema = z.enum(["text", "number", "select", "textarea"]);

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
    const needsOptions = value.answerType === "select";

    if (needsOptions && (!value.options || value.options.length === 0)) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "Options are required for select questions",
        path: ["options"],
      });
    }

    if (!needsOptions && value.options && value.options.length > 0) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "Options are only allowed for select questions",
        path: ["options"],
      });
    }
  });

export const AssessmentAnswerValueSchema = z.union([
  z.string().trim().min(1).max(2000),
  z.number(),
]);

export const AssessmentAnswerSchema = z
  .object({
    questionKey: QuestionKeySchema,
    sectionKey: SectionKeySchema,
    answerType: AssessmentAnswerTypeSchema,
    value: AssessmentAnswerValueSchema,
  })
  .superRefine((value, ctx) => {
    const isString = typeof value.value === "string";
    const isNumber = typeof value.value === "number";

    if ((value.answerType === "text" || value.answerType === "textarea" || value.answerType === "select") && !isString) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "This answer type must use a string value",
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
  });

export const AssessmentSchema = z.object({
  id: EntityIdSchema,
  businessId: EntityIdSchema,
  status: AssessmentStatusSchema,
  version: NonEmptyStringSchema.max(32),
  startedAt: TimestampSchema,
  submittedAt: TimestampSchema.nullable(),
  sections: z.array(AssessmentSectionSchema).min(1).max(12),
  answers: z.array(AssessmentAnswerSchema).max(100),
});

export const AssessmentCreateSchema = z.object({
  version: NonEmptyStringSchema.max(32),
  sections: z.array(AssessmentSectionSchema).min(1).max(12),
  answers: z.array(AssessmentAnswerSchema).max(100),
});

export const AssessmentUpdateSchema = z
  .object({
    status: AssessmentStatusSchema.optional(),
    sections: z.array(AssessmentSectionSchema).min(1).max(12).optional(),
    answers: z.array(AssessmentAnswerSchema).max(100).optional(),
  })
  .refine((value) => Object.keys(value).length > 0, {
    message: "At least one assessment field must be provided for updates",
  });

export const AssessmentSubmitSchema = z.object({
  answers: z.array(AssessmentAnswerSchema).max(100),
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
export type AssessmentCreate = z.infer<typeof AssessmentCreateSchema>;
export type AssessmentOption = z.infer<typeof AssessmentOptionSchema>;
export type AssessmentQuestion = z.infer<typeof AssessmentQuestionSchema>;
export type AssessmentSection = z.infer<typeof AssessmentSectionSchema>;
export type AssessmentStatus = z.infer<typeof AssessmentStatusSchema>;
export type AssessmentSubmit = z.infer<typeof AssessmentSubmitSchema>;
export type AssessmentUpdate = z.infer<typeof AssessmentUpdateSchema>;
