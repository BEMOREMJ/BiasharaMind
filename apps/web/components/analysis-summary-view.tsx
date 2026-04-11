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
          setStatusMessage("Loaded the latest insights.");
        } else {
          setStatusMessage("No insights are available yet. Generate insights from your saved assessment.");
        }
      } catch (error) {
        if (!active) {
          return;
        }

        setErrorMessage(error instanceof Error ? error.message : "Failed to load insights.");
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

  async function handleGenerateInsights() {
    setIsRunning(true);
    setErrorMessage(null);
    setStatusMessage(null);

    try {
      const summary = await runAnalysis();
      setAnalysis(summary);
      setStatusMessage("Insights generated successfully.");
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Unable to generate insights.");
    } finally {
      setIsRunning(false);
    }
  }

  return (
    <div className="dashboard-stack">
      <DashboardCard tone="hero" title="Assessment results">
        <div className="dashboard-stack">
          <Badge tone={analysis ? "success" : "default"}>
            {analysis ? "Insights ready" : "Generate insights"}
          </Badge>
          <SectionHeader
            title="Assessment results"
            eyebrow="Business insights"
            description="Turn your completed assessment into a clear view of where your business is doing well, where there may be risk, and what needs attention first."
          />
          <div className="button-row">
            <PrimaryButton
              disabled={isLoading || isRunning}
              onClick={handleGenerateInsights}
              type="button"
            >
              {isRunning ? "Generating insights..." : analysis ? "Refresh insights" : "Generate insights"}
            </PrimaryButton>
          </div>
          {(statusMessage || errorMessage) && (
            <div className={errorMessage ? "status-banner status-banner--error" : "status-banner status-banner--success"}>
              {errorMessage ?? statusMessage}
            </div>
          )}
        </div>
      </DashboardCard>

      {isLoading ? <DashboardCard title="Loading" description="Loading insights..." /> : null}

      {!isLoading && analysis ? (
        <>
          <div className="dashboard-grid dashboard-grid--results">
            <DashboardCard
              title="Overall score"
              description="BiasharaMind uses your saved assessment responses to generate a structured summary of strengths, risks, and business priorities."
            >
              <div className="score-panel">
                <strong className="score-panel__value">{Math.round(analysis.overallScore)}</strong>
                <span className="score-panel__label">Overall business score out of 100</span>
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
                    <Badge tone={scoreTone(category.score)}>{`${Math.round(category.score)}`}</Badge>
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
            description="Priority areas to focus on first based on your assessment responses."
          >
            <div className="priority-list">
              {analysis.topPriorities.map((priority) => (
                <article className="priority-list__item" key={priority.title}>
                  <div className="dashboard-stack">
                    <h3 className="card-title">{priority.title}</h3>
                    <p className="card-description">{priority.why}</p>
                  </div>
                  <div className="button-row">
                    <Badge tone="default">{`Effort: ${priority.effort}`}</Badge>
                    <Badge tone="warning">{`Cost: ${priority.costBand}`}</Badge>
                    <Badge tone="success">{`Impact: ${priority.expectedImpact}`}</Badge>
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
