import {
  AssessmentAnswerSchema,
  type AssessmentAnswer,
} from "../contracts/assessment";

export const exampleAssessmentAnswers: AssessmentAnswer[] = [
  AssessmentAnswerSchema.parse({
    questionKey: "sales_tracking_method",
    sectionKey: "sales_operations",
    answerType: "single_select",
    value: "paper_and_spreadsheet",
  }),
  AssessmentAnswerSchema.parse({
    questionKey: "customer_follow_up_consistency",
    sectionKey: "sales_operations",
    answerType: "number",
    value: 2,
  }),
  AssessmentAnswerSchema.parse({
    questionKey: "uses_digital_payments",
    sectionKey: "finance",
    answerType: "boolean",
    value: true,
  }),
  AssessmentAnswerSchema.parse({
    questionKey: "current_growth_blockers",
    sectionKey: "strategy",
    answerType: "multi_select",
    value: ["limited_marketing", "manual_reporting", "unclear_staff_roles"],
  }),
  AssessmentAnswerSchema.parse({
    questionKey: "owner_priority_for_next_quarter",
    sectionKey: "strategy",
    answerType: "text",
    value: "Build a predictable weekly sales process and improve stock visibility.",
  }),
];
