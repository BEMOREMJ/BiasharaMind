import {
  AssessmentAnswerSchema,
  type AssessmentAnswer,
} from "../contracts/assessment";

export const exampleAssessmentAnswers: AssessmentAnswer[] = [
  AssessmentAnswerSchema.parse({
    questionKey: "operations_process_documented",
    sectionKey: "operations",
    answerType: "select",
    value: "partly_documented",
  }),
  AssessmentAnswerSchema.parse({
    questionKey: "sales_monthly_target_confidence",
    sectionKey: "sales_marketing",
    answerType: "number",
    value: 6,
  }),
  AssessmentAnswerSchema.parse({
    questionKey: "customer_feedback_capture",
    sectionKey: "customer_management",
    answerType: "textarea",
    value: "Most feedback is collected informally over WhatsApp and in-store conversations.",
  }),
  AssessmentAnswerSchema.parse({
    questionKey: "finance_reporting_frequency",
    sectionKey: "finance_reporting",
    answerType: "select",
    value: "monthly",
  }),
  AssessmentAnswerSchema.parse({
    questionKey: "growth_blocker_primary",
    sectionKey: "growth_blockers",
    answerType: "text",
    value: "Manual coordination across sales, stock, and follow-up makes it hard to scale consistently.",
  }),
];
