"use client";

import { type V2AnalysisRun, type V2SectionScore } from "@biasharamind/shared";
import { useEffect, useMemo, useState } from "react";

import { Badge } from "@/components/badge";
import { DashboardCard } from "@/components/dashboard-card";
import { PrimaryButton } from "@/components/primary-button";
import { SectionHeader } from "@/components/section-header";
import { SecondaryButton } from "@/components/secondary-button";
import { AnalysisV2ApiError, getAnalysisV2, runAnalysisV2 } from "@/lib/api/analysis-v2";

function titleize(value: string): string {
  return value
    .replace(/_/g, " ")
    .replace(/\b\w/g, (segment) => segment.toUpperCase());
}

function formatScore(value: number): string {
  return value.toFixed(1);
}

function formatStatus(value: string): string {
  return titleize(value);
}

function sectionTone(score: number): "success" | "warning" | "error" | "default" {
  if (score >= 80) {
    return "success";
  }
  if (score >= 50) {
    return "warning";
  }
  if (score < 35) {
    return "error";
  }
  return "default";
}

function lifecycleTone(analysis: V2AnalysisRun): "success" | "warning" | "default" {
  if (analysis.lifecycle.freshnessStatus === "fresh" && analysis.lifecycle.diagnosisState === "final") {
    return "success";
  }
  if (analysis.lifecycle.freshnessStatus === "provisional") {
    return "warning";
  }
  return "default";
}

function SectionScoreCard({ section }: { section: V2SectionScore }) {
  return (
    <div className="score-list__item">
      <div className="results-v2-section__header">
        <div>
          <strong>{section.title}</strong>
          <p className="muted-copy">
            {section.completenessLabel.replace(/_/g, " ")} with evidence confidence {formatScore(section.evidenceConfidence)}.
          </p>
        </div>
        <Badge tone={sectionTone(section.score)}>{formatScore(section.score)}</Badge>
      </div>
      <div className="results-v2-buckets">
        {section.bucketScores.map((bucket) => (
          <div className="stat-chip" key={`${section.sectionId}-${bucket.bucket}`}>
            <strong>{formatScore(bucket.score)}</strong>
            <span>{titleize(bucket.bucket)}</span>
          </div>
        ))}
      </div>
      {section.moduleContributionScore !== null && section.moduleContributionScore !== undefined ? (
        <div className="status-banner">
          Adaptive module contribution: {formatScore(section.moduleContributionScore)} at {(section.moduleContributionWeight ?? 0) * 100}% of the parent section blend.
        </div>
      ) : null}
    </div>
  );
}

export function ResultsV2View() {
  const [analysis, setAnalysis] = useState<V2AnalysisRun | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isRunning, setIsRunning] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const staleNotice = useMemo(() => {
    if (!analysis?.lifecycle.rerunRequired) {
      return null;
    }
    return "Your assessment or business context changed. Future V2 analysis should be rerun to reflect the latest inputs.";
  }, [analysis]);

  useEffect(() => {
    let active = true;

    async function loadAnalysis() {
      try {
        const result = await getAnalysisV2();
        if (!active) {
          return;
        }
        setAnalysis(result);
        setStatusMessage(
          result
            ? "Loaded the latest persisted V2 deterministic analysis."
            : "No V2 analysis has been run yet. When your V2 profile and submitted V2 assessment are ready, run analysis here.",
        );
      } catch (error) {
        if (!active) {
          return;
        }
        setErrorMessage(error instanceof Error ? error.message : "Failed to load the V2 analysis.");
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
    setStatusMessage(null);
    setErrorMessage(null);

    try {
      const result = await runAnalysisV2();
      setAnalysis(result);
      setStatusMessage("V2 deterministic analysis completed and was saved successfully.");
    } catch (error) {
      if (error instanceof AnalysisV2ApiError && error.status === 409) {
        setErrorMessage(error.message);
      } else {
        setErrorMessage(error instanceof Error ? error.message : "Unable to run the V2 analysis.");
      }
    } finally {
      setIsRunning(false);
    }
  }

  return (
    <div className="dashboard-stack">
      <DashboardCard tone="hero" title="Results V2">
        <div className="dashboard-stack">
          <Badge tone={analysis ? lifecycleTone(analysis) : "default"}>
            {analysis ? formatStatus(analysis.lifecycle.freshnessStatus) : "Not run yet"}
          </Badge>
          <SectionHeader
            title="Results V2"
            eyebrow="Slice 4"
            description="This view shows the deterministic V2 health score, status, coverage, confidence, and explainability stored in the latest V2 analysis run."
          />
          <div className="button-row">
            <PrimaryButton disabled={isLoading || isRunning} onClick={handleRunAnalysis} type="button">
              {isRunning ? "Running analysis..." : analysis ? "Run analysis again" : "Run V2 analysis"}
            </PrimaryButton>
            <SecondaryButton href="/assessment-v2">Review V2 assessment</SecondaryButton>
            <SecondaryButton href="/business-v2">Review V2 profile</SecondaryButton>
          </div>
          {statusMessage ? <div className="status-banner status-banner--success">{statusMessage}</div> : null}
          {staleNotice ? <div className="status-banner status-banner--warning">{staleNotice}</div> : null}
          {errorMessage ? (
            <div className="status-stack">
              <div className="status-banner status-banner--error">{errorMessage}</div>
              {errorMessage.includes("business profile") ? (
                <PrimaryButton href="/business-v2">Complete V2 business profile</PrimaryButton>
              ) : null}
              {errorMessage.includes("assessment") ? (
                <PrimaryButton href="/assessment-v2">Complete V2 assessment</PrimaryButton>
              ) : null}
            </div>
          ) : null}
        </div>
      </DashboardCard>

      {isLoading ? (
        <DashboardCard title="Loading analysis">
          <p className="muted-copy">Reading the latest V2 analysis...</p>
        </DashboardCard>
      ) : null}

      {!isLoading && analysis ? (
        <>
          <div className="dashboard-grid dashboard-grid--results">
            <DashboardCard title="Overall health" description="Deterministic V2 score and current status band.">
              <div className="score-panel">
                <strong className="score-panel__value">{formatScore(analysis.summary.overallHealthScore)}</strong>
                <span className="score-panel__label">{formatStatus(analysis.summary.overallStatus)}</span>
              </div>
              <div className="stats-row">
                <div className="stat-chip">
                  <strong>{formatScore(analysis.summary.completeness.overall)}</strong>
                  <span>Completeness</span>
                </div>
                <div className="stat-chip">
                  <strong>{formatScore(analysis.summary.evidenceConfidence.score)}</strong>
                  <span>Evidence confidence</span>
                </div>
                <div className="stat-chip">
                  <strong>{analysis.summary.activeCriticalRiskCount}</strong>
                  <span>Active critical risks</span>
                </div>
              </div>
            </DashboardCard>

            <DashboardCard title="Lifecycle" description="Freshness, rerun state, and diagnosis confidence.">
              <dl className="summary-list">
                <div>
                  <dt>Freshness</dt>
                  <dd>{formatStatus(analysis.lifecycle.freshnessStatus)}</dd>
                </div>
                <div>
                  <dt>Diagnosis state</dt>
                  <dd>{formatStatus(analysis.lifecycle.diagnosisState)}</dd>
                </div>
                <div>
                  <dt>Rerun required</dt>
                  <dd>{analysis.lifecycle.rerunRequired ? "Yes" : "No"}</dd>
                </div>
                <div>
                  <dt>Rerun reason</dt>
                  <dd>{formatStatus(analysis.lifecycle.rerunReason)}</dd>
                </div>
                <div>
                  <dt>Version set</dt>
                  <dd>{analysis.metadata.analysisEngineVersion}</dd>
                </div>
              </dl>
            </DashboardCard>
          </div>

          <DashboardCard title="Section scores" description="Core V2 section scores with bucket composition and adaptive module blend where applicable.">
            <div className="score-list">
              {analysis.summary.sectionScores.map((section) => (
                <SectionScoreCard key={section.sectionId} section={section} />
              ))}
            </div>
          </DashboardCard>

          <div className="dashboard-grid dashboard-grid--results">
            <DashboardCard title="Status caps" description="Caps are applied after overall score calculation.">
              {analysis.summary.capsApplied.length > 0 ? (
                <div className="score-list">
                  {analysis.summary.capsApplied.map((cap) => (
                    <div className="score-list__item" key={cap.code}>
                      <div>
                        <strong>{cap.label}</strong>
                        <p className="muted-copy">{cap.reason}</p>
                      </div>
                      <Badge tone="warning">{formatStatus(cap.cappedStatus)}</Badge>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="muted-copy">No status caps were applied to this run.</p>
              )}
            </DashboardCard>

            <DashboardCard title="Coverage and confidence" description="Deterministic completeness and evidence-confidence limitations.">
              <dl className="summary-list">
                <div>
                  <dt>Coverage label</dt>
                  <dd>{formatStatus(analysis.summary.completeness.label)}</dd>
                </div>
                <div>
                  <dt>Confidence label</dt>
                  <dd>{formatStatus(analysis.summary.evidenceConfidence.label)}</dd>
                </div>
                <div>
                  <dt>Essential answers</dt>
                  <dd>
                    {analysis.summary.completeness.essentialAnsweredSufficiently}/
                    {analysis.summary.completeness.essentialApplicable}
                  </dd>
                </div>
                <div>
                  <dt>Optional answers</dt>
                  <dd>
                    {analysis.summary.completeness.optionalAnsweredSufficiently}/
                    {analysis.summary.completeness.optionalApplicable}
                  </dd>
                </div>
              </dl>
              <ul className="list-copy">
                {analysis.summary.evidenceConfidence.keyLimitations.map((limitation) => (
                  <li key={limitation}>{limitation}</li>
                ))}
              </ul>
            </DashboardCard>
          </div>

          <DashboardCard title="Explainability" description="These deterministic hints are stored alongside the score for later UI expansion.">
            <div className="dashboard-grid dashboard-grid--results">
              <div>
                <h3 className="profile-section__title">Score drivers</h3>
                <ul className="list-copy">
                  {analysis.explainability.scoreDrivers.map((driver) => (
                    <li key={driver.code}>{driver.detail}</li>
                  ))}
                </ul>
              </div>
              <div>
                <h3 className="profile-section__title">Missing or weak evidence</h3>
                <ul className="list-copy">
                  {analysis.explainability.missingOrWeakEvidence.map((gap, index) => (
                    <li key={`${gap.area}-${index}`}>{gap.detail}</li>
                  ))}
                </ul>
              </div>
            </div>
          </DashboardCard>
        </>
      ) : null}
    </div>
  );
}
