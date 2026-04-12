import { ReportDocumentSchema, type ReportDocument } from "@biasharamind/shared";

import { apiFetch, parseJsonResponse, readErrorMessage } from "@/lib/api/request";

class ReportApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ReportApiError";
    this.status = status;
  }
}

export async function getReport(): Promise<ReportDocument | null> {
  const response = await apiFetch("/report");

  if (response.status === 404) {
    return null;
  }

  let payload: unknown;

  try {
    payload = await parseJsonResponse(response);
  } catch {
    throw new ReportApiError("Received an invalid JSON response from the API.", response.status);
  }

  if (!response.ok) {
    throw new ReportApiError(
      readErrorMessage(payload, "Failed to load the report."),
      response.status,
    );
  }

  return ReportDocumentSchema.parse(payload);
}

export async function generateReport(): Promise<ReportDocument> {
  const response = await apiFetch("/report/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });

  let payload: unknown;

  try {
    payload = await parseJsonResponse(response);
  } catch {
    throw new ReportApiError("Received an invalid JSON response from the API.", response.status);
  }

  if (!response.ok) {
    throw new ReportApiError(
      readErrorMessage(payload, "Failed to generate the report."),
      response.status,
    );
  }

  return ReportDocumentSchema.parse(payload);
}
