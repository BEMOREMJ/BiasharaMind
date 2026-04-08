import { ReportDocumentSchema, type ReportDocument } from "@biasharamind/shared";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

class ReportApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ReportApiError";
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
    throw new ReportApiError("Received an invalid JSON response from the API.", response.status);
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

export async function getReport(): Promise<ReportDocument | null> {
  const response = await fetch(`${API_BASE_URL}/report`, {
    cache: "no-store",
  });

  if (response.status === 404) {
    return null;
  }

  const payload = await parseJsonResponse(response);

  if (!response.ok) {
    throw new ReportApiError(
      readErrorMessage(payload, "Failed to load the report."),
      response.status,
    );
  }

  return ReportDocumentSchema.parse(payload);
}

export async function generateReport(): Promise<ReportDocument> {
  const response = await fetch(`${API_BASE_URL}/report/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });

  const payload = await parseJsonResponse(response);

  if (!response.ok) {
    throw new ReportApiError(
      readErrorMessage(payload, "Failed to generate the report."),
      response.status,
    );
  }

  return ReportDocumentSchema.parse(payload);
}
