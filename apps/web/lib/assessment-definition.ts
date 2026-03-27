import type { AssessmentQuestion, AssessmentSection } from "@biasharamind/shared";

export const assessmentSections: AssessmentSection[] = [
  {
    key: "operations",
    title: "Operations",
    description: "How daily operations are currently managed.",
    order: 1,
  },
  {
    key: "sales_marketing",
    title: "Sales and Marketing",
    description: "How the business attracts and converts demand.",
    order: 2,
  },
  {
    key: "customer_management",
    title: "Customer Management",
    description: "How customer relationships and follow-up are handled.",
    order: 3,
  },
  {
    key: "finance_reporting",
    title: "Finance and Reporting",
    description: "How cash flow, reporting, and visibility are managed.",
    order: 4,
  },
  {
    key: "team_workflows",
    title: "Team Workflows",
    description: "How work ownership and team execution are organized.",
    order: 5,
  },
  {
    key: "digital_tools",
    title: "Digital Tools",
    description: "How software and digital systems support the business.",
    order: 6,
  },
  {
    key: "growth_blockers",
    title: "Growth Blockers",
    description: "What is currently slowing down growth or consistency.",
    order: 7,
  },
];

export const assessmentQuestions: AssessmentQuestion[] = [
  {
    key: "operations_process_documented",
    sectionKey: "operations",
    prompt: "How clearly are your daily operating processes documented?",
    answerType: "select",
    required: true,
    options: [
      { label: "Not documented", value: "not_documented" },
      { label: "Mostly in the owner's head", value: "owner_memory" },
      { label: "Partly documented", value: "partly_documented" },
      { label: "Well documented", value: "well_documented" },
    ],
    helpText: "Think about opening, closing, stock handling, or fulfillment routines.",
  },
  {
    key: "operations_biggest_delay",
    sectionKey: "operations",
    prompt: "What is the biggest operational delay your business faces each week?",
    answerType: "textarea",
    required: true,
    helpText: "For example: stock counts, approvals, delivery coordination, or handoffs.",
  },
  {
    key: "sales_new_customers_channel",
    sectionKey: "sales_marketing",
    prompt: "Which channel currently brings most of your new customers?",
    answerType: "select",
    required: true,
    options: [
      { label: "Walk-in or location visibility", value: "walk_in" },
      { label: "Referrals", value: "referrals" },
      { label: "Social media", value: "social_media" },
      { label: "Paid advertising", value: "paid_ads" },
      { label: "Sales outreach", value: "outreach" },
    ],
  },
  {
    key: "sales_monthly_target_confidence",
    sectionKey: "sales_marketing",
    prompt: "On a scale of 1 to 10, how confident are you in hitting next month's sales target?",
    answerType: "number",
    required: true,
    helpText: "Use 1 for very low confidence and 10 for very high confidence.",
  },
  {
    key: "customer_follow_up_frequency",
    sectionKey: "customer_management",
    prompt: "How often do you follow up with recent or repeat customers?",
    answerType: "select",
    required: true,
    options: [
      { label: "Rarely or never", value: "rarely" },
      { label: "Only when there is a problem", value: "reactive" },
      { label: "Sometimes", value: "sometimes" },
      { label: "Consistently", value: "consistently" },
    ],
  },
  {
    key: "customer_feedback_capture",
    sectionKey: "customer_management",
    prompt: "How do you currently capture customer feedback?",
    answerType: "textarea",
    required: true,
  },
  {
    key: "finance_reporting_frequency",
    sectionKey: "finance_reporting",
    prompt: "How often do you review business financial performance?",
    answerType: "select",
    required: true,
    options: [
      { label: "Hardly ever", value: "rarely" },
      { label: "Monthly", value: "monthly" },
      { label: "Weekly", value: "weekly" },
      { label: "Daily", value: "daily" },
    ],
  },
  {
    key: "finance_cash_visibility",
    sectionKey: "finance_reporting",
    prompt: "How many weeks ahead can you clearly estimate cash needs?",
    answerType: "number",
    required: true,
    helpText: "Enter a number such as 0, 2, 4, or 8.",
  },
  {
    key: "team_role_clarity",
    sectionKey: "team_workflows",
    prompt: "How clear are team roles and responsibilities today?",
    answerType: "select",
    required: true,
    options: [
      { label: "Very unclear", value: "very_unclear" },
      { label: "Somewhat unclear", value: "somewhat_unclear" },
      { label: "Mostly clear", value: "mostly_clear" },
      { label: "Very clear", value: "very_clear" },
    ],
  },
  {
    key: "team_missed_tasks_reason",
    sectionKey: "team_workflows",
    prompt: "When tasks get missed, what is usually the main reason?",
    answerType: "textarea",
    required: true,
  },
  {
    key: "tools_primary_stack",
    sectionKey: "digital_tools",
    prompt: "Which description best matches your current digital tool setup?",
    answerType: "select",
    required: true,
    options: [
      { label: "Mostly manual", value: "mostly_manual" },
      { label: "A few disconnected tools", value: "disconnected_tools" },
      { label: "Several tools with some consistency", value: "partial_system" },
      { label: "Well organized digital stack", value: "organized_stack" },
    ],
  },
  {
    key: "tools_manual_work_example",
    sectionKey: "digital_tools",
    prompt: "What manual task takes more time than it should because systems are weak?",
    answerType: "textarea",
    required: true,
  },
  {
    key: "growth_blocker_primary",
    sectionKey: "growth_blockers",
    prompt: "What is the main blocker limiting growth right now?",
    answerType: "textarea",
    required: true,
  },
  {
    key: "growth_blocker_urgency",
    sectionKey: "growth_blockers",
    prompt: "How urgent is it to solve that blocker in the next 90 days?",
    answerType: "select",
    required: true,
    options: [
      { label: "Low urgency", value: "low" },
      { label: "Moderate urgency", value: "moderate" },
      { label: "High urgency", value: "high" },
      { label: "Critical urgency", value: "critical" },
    ],
  },
];

export function getQuestionsForSection(sectionKey: AssessmentSection["key"]) {
  return assessmentQuestions.filter((question) => question.sectionKey === sectionKey);
}
