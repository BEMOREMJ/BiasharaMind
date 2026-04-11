import { AnalysisSummarySchema, type AnalysisSummary } from "@biasharamind/shared";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

class AnalysisApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "AnalysisApiError";
    this.status = status;
  }
}

async function parseJsonResponse(response: Response) {
  const text = await response.text();
  if (!text) {
    return null;
  }

  try {
    return JSON.parse(text);
  } catch {
    throw new AnalysisApiError("Received an invalid JSON response from the API.", response.status);
  }
}

function readErrorMessage(payload: unknown, fallback: string): string {
  if (
    payload &&
    typeof payload === "object" &&
    "detail" in payload &&
    typeof (payload as { detail: unknown }).detail === "string"
  ) {
    return (payload as { detail: string }).detail;
  }

  return fallback;
}

export async function getAnalysis(): Promise<AnalysisSummary | null> {
  const response = await fetch(`${API_BASE_URL}/analysis`, {
    cache: "no-store",
  });

  if (response.status === 404) {
    return null;
  }

  const payload = await parseJsonResponse(response);

  if (!response.ok) {
    throw new AnalysisApiError(
      readErrorMessage(payload, "Failed to load insights."),
      response.status,
    );
  }

  return AnalysisSummarySchema.parse(payload);
}

export async function runAnalysis(): Promise<AnalysisSummary> {
  const response = await fetch(`${API_BASE_URL}/analysis/run`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });

  const payload = await parseJsonResponse(response);

  if (!response.ok) {
    throw new AnalysisApiError(
      readErrorMessage(payload, "Failed to generate insights."),
      response.status,
    );
  }

  return AnalysisSummarySchema.parse(payload);
}
