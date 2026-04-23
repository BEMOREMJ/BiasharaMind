import {
  V2AnalysisRunSchema,
  type V2AnalysisRun,
} from "@biasharamind/shared";

import { apiFetch, parseJsonResponse, readErrorMessage } from "@/lib/api/request";

class AnalysisV2ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "AnalysisV2ApiError";
    this.status = status;
  }
}

export async function getAnalysisV2(): Promise<V2AnalysisRun | null> {
  const response = await apiFetch("/v2/analysis");

  if (response.status === 404) {
    return null;
  }

  let payload: unknown;

  try {
    payload = await parseJsonResponse(response);
  } catch {
    throw new AnalysisV2ApiError("Received an invalid JSON response from the API.", response.status);
  }

  if (!response.ok) {
    throw new AnalysisV2ApiError(
      readErrorMessage(payload, "Failed to load the V2 analysis."),
      response.status,
    );
  }

  return V2AnalysisRunSchema.parse(payload);
}

export async function runAnalysisV2(): Promise<V2AnalysisRun> {
  const response = await apiFetch("/v2/analysis/run", {
    method: "POST",
  });

  let payload: unknown;

  try {
    payload = await parseJsonResponse(response);
  } catch {
    throw new AnalysisV2ApiError("Received an invalid JSON response from the API.", response.status);
  }

  if (!response.ok) {
    throw new AnalysisV2ApiError(
      readErrorMessage(payload, "Failed to run the V2 analysis."),
      response.status,
    );
  }

  return V2AnalysisRunSchema.parse(payload);
}

export { AnalysisV2ApiError };
