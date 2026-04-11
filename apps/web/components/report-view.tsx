"use client";

import type { ReportDocument } from "@biasharamind/shared";
import { useEffect, useState } from "react";

import { Badge } from "@/components/badge";
import { DashboardCard } from "@/components/dashboard-card";
import { PrimaryButton } from "@/components/primary-button";
import { SecondaryButton } from "@/components/secondary-button";
import { SectionHeader } from "@/components/section-header";
import { generateReport, getReport } from "@/lib/api/report";

function downloadReport(report: ReportDocument) {
  const blob = new Blob([JSON.stringify(report, null, 2)], {
    type: "application/json;charset=utf-8",
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = report.exportFileName;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

export function ReportView() {
  const [report, setReport] = useState<ReportDocument | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    async function loadReport() {
      try {
        const savedReport = await getReport();

        if (!active) {
          return;
        }

        if (savedReport) {
          setReport(savedReport);
          setStatusMessage("Loaded the current report.");
        } else {
          setStatusMessage("No report is available yet. Generate one from your saved business profile, insights, and roadmap.");
        }
      } catch (error) {
        if (!active) {
          return;
        }

        setErrorMessage(error instanceof Error ? error.message : "Failed to load the report.");
      } finally {
        if (active) {
          setIsLoading(false);
        }
      }
    }

    void loadReport();

    return () => {
      active = false;
    };
  }, []);

  async function handleGenerateReport() {
    setIsGenerating(true);
    setErrorMessage(null);
    setStatusMessage(null);

    try {
      const generatedReport = await generateReport();
      setReport(generatedReport);
      setStatusMessage("Report generated successfully.");
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Unable to generate the report.");
    } finally {
      setIsGenerating(false);
    }
  }

  return (
    <div className="dashboard-stack">
      <DashboardCard tone="hero" title="Business report">
        <div className="dashboard-stack">
          <Badge tone={report ? "success" : "default"}>
            {report ? "Report ready" : "Generate report"}
          </Badge>
          <SectionHeader
            title="Business report"
            eyebrow="Structured summary"
            description="Create a clear report that brings together your business profile, assessment insights, and roadmap in one structured view."
          />
          <div className="button-row">
            <PrimaryButton
              disabled={isLoading || isGenerating}
              onClick={handleGenerateReport}
              type="button"
            >
              {isGenerating ? "Generating report..." : report ? "Refresh report" : "Generate report"}
            </PrimaryButton>
            <SecondaryButton
              disabled={!report}
              onClick={() => {
                if (report) {
                  downloadReport(report);
                }
              }}
              type="button"
            >
              Download report (JSON)
            </SecondaryButton>
          </div>
          {(statusMessage || errorMessage) && (
            <div
              className={
                errorMessage
                  ? "status-banner status-banner--error"
                  : "status-banner status-banner--success"
              }
            >
              {errorMessage ?? statusMessage}
            </div>
          )}
        </div>
      </DashboardCard>

      {isLoading ? <DashboardCard title="Loading" description="Loading report..." /> : null}

      {!isLoading && report ? (
        <>
          <div className="dashboard-grid dashboard-grid--results">
            <DashboardCard
              title="Business summary"
              description="Core business context included in the current report."
            >
              <dl className="summary-list">
                <div>
                  <dt>Business name</dt>
                  <dd>{report.businessSummary.businessName}</dd>
                </div>
                <div>
                  <dt>Industry</dt>
                  <dd>{report.businessSummary.industry}</dd>
                </div>
                <div>
                  <dt>Country</dt>
                  <dd>{report.businessSummary.country}</dd>
                </div>
                <div>
                  <dt>Size band</dt>
                  <dd>{report.businessSummary.sizeBand}</dd>
                </div>
                <div>
                  <dt>Team size</dt>
                  <dd>{report.businessSummary.teamSize}</dd>
                </div>
                <div>
                  <dt>Main goal</dt>
                  <dd>{report.businessSummary.mainGoal}</dd>
                </div>
              </dl>
            </DashboardCard>

            <DashboardCard title="Score summary" description="Current analysis snapshot included in the report.">
              <div className="score-panel">
                <strong className="score-panel__value">{Math.round(report.overallScore)}</strong>
                <span className="score-panel__label">Overall score out of 100</span>
              </div>
              <div className="score-list">
                {report.categoryScores.map((category) => (
                  <div className="score-list__item" key={category.sectionKey}>
                    <div>
                      <strong>{category.label}</strong>
                      <p className="muted-copy">{category.sectionKey}</p>
                    </div>
                    <Badge tone="default">{`${Math.round(category.score)}`}</Badge>
                  </div>
                ))}
              </div>
            </DashboardCard>
          </div>

          <div className="dashboard-grid dashboard-grid--results">
            <DashboardCard title="Strengths" description="Top strengths captured in the report.">
              <ul className="insight-list">
                {report.strengths.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </DashboardCard>
            <DashboardCard title="Risks" description="Top risks captured in the report.">
              <ul className="insight-list">
                {report.risks.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </DashboardCard>
          </div>

          <DashboardCard title="Priorities" description="Priority recommendations included in the report.">
            <div className="priority-list">
              {report.priorities.map((priority) => (
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

          <DashboardCard title="Roadmap phases" description="Phased action summary included in the report.">
            <div className="priority-list">
              {report.roadmapPhases.map((phase) => (
                <article className="priority-list__item" key={phase.label}>
                  <div className="dashboard-stack">
                    <h3 className="card-title">{phase.label}</h3>
                    <ul className="insight-list">
                      {phase.actions.map((action) => (
                        <li key={`${phase.label}-${action.title}`}>
                          <strong>{action.title}</strong>: {action.description}
                        </li>
                      ))}
                    </ul>
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
