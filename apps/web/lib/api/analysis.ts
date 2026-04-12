import { AnalysisSummarySchema, type AnalysisSummary } from "@biasharamind/shared";

import { apiFetch, parseJsonResponse, readErrorMessage } from "@/lib/api/request";

class AnalysisApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "AnalysisApiError";
    this.status = status;
  }
}

export async function getAnalysis(): Promise<AnalysisSummary | null> {
  const response = await apiFetch("/analysis");

  if (response.status === 404) {
    return null;
  }

  let payload: unknown;

  try {
    payload = await parseJsonResponse(response);
  } catch {
    throw new AnalysisApiError("Received an invalid JSON response from the API.", response.status);
  }

  if (!response.ok) {
    throw new AnalysisApiError(
      readErrorMessage(payload, "Failed to load insights."),
      response.status,
    );
  }

  return AnalysisSummarySchema.parse(payload);
}

export async function runAnalysis(): Promise<AnalysisSummary> {
  const response = await apiFetch("/analysis/run", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });

  let payload: unknown;

  try {
    payload = await parseJsonResponse(response);
  } catch {
    throw new AnalysisApiError("Received an invalid JSON response from the API.", response.status);
  }

  if (!response.ok) {
    throw new AnalysisApiError(
      readErrorMessage(payload, "Failed to generate insights."),
      response.status,
    );
  }

  return AnalysisSummarySchema.parse(payload);
}
