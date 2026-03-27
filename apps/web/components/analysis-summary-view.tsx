"use client";

import type { AnalysisSummary } from "@biasharamind/shared";
import { useEffect, useState } from "react";

import { Badge } from "@/components/badge";
import { DashboardCard } from "@/components/dashboard-card";
import { PrimaryButton } from "@/components/primary-button";
import { SectionHeader } from "@/components/section-header";
import { getAnalysis, runAnalysis } from "@/lib/api/analysis";

function scoreTone(score: number): "success" | "warning" | "error" {
  if (score >= 70) {
    return "success";
  }

  if (score >= 50) {
    return "warning";
  }

  return "error";
}

export function AnalysisSummaryView() {
  const [analysis, setAnalysis] = useState<AnalysisSummary | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isRunning, setIsRunning] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    async function loadAnalysis() {
      try {
        const summary = await getAnalysis();

        if (!active) {
          return;
        }

        if (summary) {
          setAnalysis(summary);
          setStatusMessage("Loaded the latest analysis summary.");
        } else {
          setStatusMessage("No analysis summary exists yet. Run analysis from the saved assessment.");
        }
      } catch (error) {
        if (!active) {
          return;
        }

        setErrorMessage(
          error instanceof Error ? error.message : "Failed to load the analysis summary.",
        );
      } finally {
        if (active) {
          setIsLoading(false);
        }
      }
    }

    void loadAnalysis();

    return () => {
      active = false;
    };
  }, []);

  async function handleRunAnalysis() {
    setIsRunning(true);
    setErrorMessage(null);
    setStatusMessage(null);

    try {
      const summary = await runAnalysis();
      setAnalysis(summary);
      setStatusMessage("Analysis summary generated successfully.");
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Unable to run analysis.");
    } finally {
      setIsRunning(false);
    }
  }

  return (
    <div className="dashboard-stack">
      <DashboardCard tone="hero" title="Results">
        <div className="dashboard-stack">
          <Badge tone={analysis ? "success" : "default"}>
            {analysis ? "Analysis summary ready" : "Run analysis"}
          </Badge>
          <SectionHeader
            title="Assessment results"
            eyebrow="Rule-based scoring"
            description="Generate a deterministic summary from the saved assessment. The current V1 logic uses explicit scoring rules and stable threshold-based strengths, risks, and priorities."
          />
          <div className="button-row">
            <PrimaryButton disabled={isLoading || isRunning} onClick={handleRunAnalysis} type="button">
              {isRunning ? "Running analysis..." : analysis ? "Re-run analysis" : "Run analysis"}
            </PrimaryButton>
          </div>
          {(statusMessage || errorMessage) && (
            <div className={errorMessage ? "status-banner status-banner--error" : "status-banner status-banner--success"}>
              {errorMessage ?? statusMessage}
            </div>
          )}
        </div>
      </DashboardCard>

      {isLoading ? <DashboardCard title="Loading" description="Loading analysis summary..." /> : null}

      {!isLoading && analysis ? (
        <>
          <div className="dashboard-grid dashboard-grid--results">
            <DashboardCard title="Overall score" description="The current overall rule-based maturity score.">
              <div className="score-panel">
                <strong className="score-panel__value">{Math.round(analysis.overallScore)}</strong>
                <span className="score-panel__label">Overall score out of 100</span>
              </div>
            </DashboardCard>

            <DashboardCard
              title="Category scores"
              description="Each category score is derived directly from the saved assessment answers."
            >
              <div className="score-list">
                {analysis.categoryScores.map((category) => (
                  <div className="score-list__item" key={category.sectionKey}>
                    <div>
                      <strong>{category.label}</strong>
                      <p className="muted-copy">{category.sectionKey}</p>
                    </div>
                    <Badge tone={scoreTone(category.score)}>
                      {Math.round(category.score)}
                    </Badge>
                  </div>
                ))}
              </div>
            </DashboardCard>
          </div>

          <div className="dashboard-grid dashboard-grid--results">
            <DashboardCard title="Top strengths" description="Highest-scoring category takeaways.">
              <ul className="insight-list">
                {analysis.topStrengths.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </DashboardCard>

            <DashboardCard title="Top risks" description="Lowest-scoring category takeaways.">
              <ul className="insight-list">
                {analysis.topRisks.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </DashboardCard>
          </div>

          <DashboardCard
            title="Top priorities"
            description="Priority recommendations are mapped from the lowest-scoring categories using deterministic rules."
          >
            <div className="priority-list">
              {analysis.topPriorities.map((priority) => (
                <article className="priority-list__item" key={priority.title}>
                  <div className="dashboard-stack">
                    <h3 className="card-title">{priority.title}</h3>
                    <p className="card-description">{priority.why}</p>
                  </div>
                  <div className="button-row">
                    <Badge tone="default">Effort: {priority.effort}</Badge>
                    <Badge tone="warning">Cost: {priority.costBand}</Badge>
                    <Badge tone="success">Impact: {priority.expectedImpact}</Badge>
                  </div>
                </article>
              ))}
            </div>
          </DashboardCard>
        </>
      ) : null}
    </div>
  );
}
