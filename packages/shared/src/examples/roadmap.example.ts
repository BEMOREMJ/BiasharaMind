import { RoadmapSchema, type Roadmap } from "../contracts/roadmap";

export const exampleRoadmap: Roadmap = RoadmapSchema.parse({
  id: "roadmap_001",
  analysisId: "analysis_001",
  days0to30: [
    {
      title: "Create a weekly sales and stock review sheet",
      description: "Move current handwritten and spreadsheet tracking into one standard weekly review template.",
      whyItMatters: "The business needs one reliable view of what is selling and where stock breaks occur.",
      effort: "medium",
      costBand: "low",
      expectedImpact: "high",
    },
    {
      title: "Define a repeat-customer outreach list",
      description: "List top past customers and assign a simple WhatsApp follow-up cadence.",
      whyItMatters: "Retention can improve revenue faster than acquiring entirely new buyers.",
      effort: "low",
      costBand: "low",
      expectedImpact: "high",
    },
  ],
  days31to60: [
    {
      title: "Introduce simple role ownership for daily operations",
      description: "Document who owns purchasing, daily sales closing, and stock reconciliation.",
      whyItMatters: "Clear operating ownership reduces missed tasks and owner bottlenecks.",
      effort: "medium",
      costBand: "low",
      expectedImpact: "medium",
    },
  ],
  days61to90: [
    {
      title: "Review margin by top product lines",
      description: "Use eight weeks of cleaner sales data to compare product volume against margin contribution.",
      whyItMatters: "Better product decisions improve profit quality, not just revenue volume.",
      effort: "medium",
      costBand: "low",
      expectedImpact: "high",
    },
  ],
  createdAt: "2026-03-18T19:00:00+00:00",
});
