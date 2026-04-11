"use client";

import type { Roadmap, RoadmapAction } from "@biasharamind/shared";
import { useEffect, useState } from "react";

import { Badge } from "@/components/badge";
import { DashboardCard } from "@/components/dashboard-card";
import { PrimaryButton } from "@/components/primary-button";
import { SectionHeader } from "@/components/section-header";
import { generateRoadmap, getRoadmap } from "@/lib/api/roadmap";

type RoadmapPhaseProps = {
  actions: RoadmapAction[];
  description: string;
  title: string;
};

function RoadmapPhase({ actions, description, title }: RoadmapPhaseProps) {
  return (
    <DashboardCard title={title} description={description}>
      {actions.length > 0 ? (
        <div className="priority-list">
          {actions.map((action) => (
            <article className="priority-list__item" key={`${title}-${action.title}`}>
              <div className="dashboard-stack">
                <h3 className="card-title">{action.title}</h3>
                <p className="card-description">{action.description}</p>
                <p className="muted-copy">{action.whyItMatters}</p>
              </div>
              <div className="button-row">
                <Badge tone="default">{`Effort: ${action.effort}`}</Badge>
                <Badge tone="warning">{`Cost: ${action.costBand}`}</Badge>
                <Badge tone="success">{`Impact: ${action.expectedImpact}`}</Badge>
              </div>
            </article>
          ))}
        </div>
      ) : (
        <p className="muted-copy">No roadmap actions are available for this phase yet.</p>
      )}
    </DashboardCard>
  );
}

export function RoadmapView() {
  const [roadmap, setRoadmap] = useState<Roadmap | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    async function loadRoadmap() {
      try {
        const savedRoadmap = await getRoadmap();

        if (!active) {
          return;
        }

        if (savedRoadmap) {
          setRoadmap(savedRoadmap);
          setStatusMessage("Loaded the current roadmap.");
        } else {
          setStatusMessage("No roadmap is available yet. Generate one from your business insights.");
        }
      } catch (error) {
        if (!active) {
          return;
        }

        setErrorMessage(error instanceof Error ? error.message : "Failed to load the roadmap.");
      } finally {
        if (active) {
          setIsLoading(false);
        }
      }
    }

    void loadRoadmap();

    return () => {
      active = false;
    };
  }, []);

  async function handleGenerateRoadmap() {
    setIsGenerating(true);
    setErrorMessage(null);
    setStatusMessage(null);

    try {
      const generatedRoadmap = await generateRoadmap();
      setRoadmap(generatedRoadmap);
      setStatusMessage("Roadmap generated successfully.");
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Unable to generate the roadmap.");
    } finally {
      setIsGenerating(false);
    }
  }

  return (
    <div className="dashboard-stack">
      <DashboardCard tone="hero" title="30 / 60 / 90-day roadmap">
        <div className="dashboard-stack">
          <Badge tone={roadmap ? "success" : "default"}>
            {roadmap ? "Roadmap ready" : "Generate roadmap"}
          </Badge>
          <SectionHeader
            title="30 / 60 / 90-day roadmap"
            eyebrow="Action plan"
            description="Turn your top priorities into a focused execution plan with practical actions your business can work on over the next 30, 60, and 90 days."
          />
          <div className="button-row">
            <PrimaryButton
              disabled={isLoading || isGenerating}
              onClick={handleGenerateRoadmap}
              type="button"
            >
              {isGenerating ? "Generating roadmap..." : roadmap ? "Refresh roadmap" : "Generate roadmap"}
            </PrimaryButton>
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

      {isLoading ? <DashboardCard title="Loading" description="Loading roadmap..." /> : null}

      {!isLoading && roadmap ? (
        <>
          <RoadmapPhase
            actions={roadmap.days0to30}
            description="Immediate focus actions for the next 30 days."
            title="Days 0-30"
          />
          <RoadmapPhase
            actions={roadmap.days31to60}
            description="Operationalize and stabilize the next priority areas."
            title="Days 31-60"
          />
          <RoadmapPhase
            actions={roadmap.days61to90}
            description="Scale the strongest early wins into more durable execution habits."
            title="Days 61-90"
          />
        </>
      ) : null}
    </div>
  );
}
