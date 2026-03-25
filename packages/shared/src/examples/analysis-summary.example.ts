import { AnalysisSummarySchema, type AnalysisSummary } from "../contracts/analysis";

export const exampleAnalysisSummary: AnalysisSummary = AnalysisSummarySchema.parse({
  id: "analysis_001",
  assessmentId: "assessment_001",
  overallScore: 58,
  categoryScores: [
    { sectionKey: "strategy", label: "Strategy", score: 61 },
    { sectionKey: "sales_operations", label: "Sales Operations", score: 49 },
    { sectionKey: "finance", label: "Finance", score: 63 },
    { sectionKey: "people", label: "People", score: 55 },
  ],
  topStrengths: [
    "The business has a clear core product focus and stable local demand.",
    "Digital payments are already accepted, reducing cash handling friction.",
    "The owner reviews sales trends regularly, even if reporting is manual.",
  ],
  topRisks: [
    "Customer follow-up is inconsistent, leading to missed repeat sales.",
    "Sales and stock tracking rely on manual tools that are hard to trust at scale.",
    "Staff responsibilities are not clearly documented, slowing execution.",
  ],
  topPriorities: [
    {
      title: "Standardize weekly sales and stock reporting",
      why: "A single reporting routine will make it easier to spot product gaps and act earlier.",
      effort: "medium",
      costBand: "low",
      expectedImpact: "high",
    },
    {
      title: "Set up a repeat-customer follow-up process",
      why: "A lightweight follow-up rhythm can improve retention without major ad spend.",
      effort: "low",
      costBand: "low",
      expectedImpact: "high",
    },
    {
      title: "Clarify owner and staff operating roles",
      why: "Clear accountability reduces delays and makes daily operations less dependent on one person.",
      effort: "medium",
      costBand: "low",
      expectedImpact: "medium",
    },
  ],
  createdAt: "2026-03-18T18:30:00+00:00",
  modelVersion: "gpt-5.1",
  workflowVersion: "analysis_v1",
});
