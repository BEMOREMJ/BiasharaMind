import {
  V2AssessmentDefinitionSchema,
  V2AssessmentReadSchema,
  V2AssessmentSaveResponseSchema,
  V2AssessmentWritePayloadSchema,
  type V2AssessmentDefinition,
  type V2AssessmentRead,
  type V2AssessmentSaveResponse,
  type V2AssessmentWritePayload,
} from "@biasharamind/shared";

import { apiFetch, parseJsonResponse, readErrorMessage } from "@/lib/api/request";

class AssessmentV2ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "AssessmentV2ApiError";
    this.status = status;
  }
}

export async function getAssessmentDefinitionV2(): Promise<V2AssessmentDefinition> {
  const response = await apiFetch("/v2/assessment/definition");

  let payload: unknown;

  try {
    payload = await parseJsonResponse(response);
  } catch {
    throw new AssessmentV2ApiError("Received an invalid JSON response from the API.", response.status);
  }

  if (!response.ok) {
    throw new AssessmentV2ApiError(
      readErrorMessage(payload, "Failed to load the V2 assessment definition."),
      response.status,
    );
  }

  return V2AssessmentDefinitionSchema.parse(payload);
}

export async function getAssessmentV2(): Promise<V2AssessmentRead | null> {
  const response = await apiFetch("/v2/assessment");

  if (response.status === 404) {
    return null;
  }

  let payload: unknown;

  try {
    payload = await parseJsonResponse(response);
  } catch {
    throw new AssessmentV2ApiError("Received an invalid JSON response from the API.", response.status);
  }

  if (!response.ok) {
    throw new AssessmentV2ApiError(
      readErrorMessage(payload, "Failed to load the saved V2 assessment."),
      response.status,
    );
  }

  return V2AssessmentReadSchema.parse(payload);
}

export async function saveAssessmentV2(
  input: V2AssessmentWritePayload,
): Promise<V2AssessmentSaveResponse> {
  const payload = V2AssessmentWritePayloadSchema.parse(input);
  const response = await apiFetch("/v2/assessment", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  let responsePayload: unknown;

  try {
    responsePayload = await parseJsonResponse(response);
  } catch {
    throw new AssessmentV2ApiError("Received an invalid JSON response from the API.", response.status);
  }

  if (!response.ok) {
    throw new AssessmentV2ApiError(
      readErrorMessage(responsePayload, "Failed to save the V2 assessment."),
      response.status,
    );
  }

  return V2AssessmentSaveResponseSchema.parse(responsePayload);
}

export async function submitAssessmentV2(
  input: V2AssessmentWritePayload,
): Promise<V2AssessmentSaveResponse> {
  const payload = V2AssessmentWritePayloadSchema.parse(input);
  const response = await apiFetch("/v2/assessment/submit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  let responsePayload: unknown;

  try {
    responsePayload = await parseJsonResponse(response);
  } catch {
    throw new AssessmentV2ApiError("Received an invalid JSON response from the API.", response.status);
  }

  if (!response.ok) {
    throw new AssessmentV2ApiError(
      readErrorMessage(responsePayload, "Failed to submit the V2 assessment."),
      response.status,
    );
  }

  return V2AssessmentSaveResponseSchema.parse(responsePayload);
}

export { AssessmentV2ApiError };
