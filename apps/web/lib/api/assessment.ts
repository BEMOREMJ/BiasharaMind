import {
  AssessmentCreateSchema,
  AssessmentSchema,
  AssessmentSubmitSchema,
  AssessmentUpdateSchema,
  type Assessment,
  type AssessmentCreate,
  type AssessmentSubmit,
  type AssessmentUpdate,
} from "@biasharamind/shared";

import { apiFetch, parseJsonResponse, readErrorMessage } from "@/lib/api/request";

class AssessmentApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "AssessmentApiError";
    this.status = status;
  }
}

export async function getAssessment(): Promise<Assessment | null> {
  const response = await apiFetch("/assessment");

  if (response.status === 404) {
    return null;
  }

  let payload: unknown;

  try {
    payload = await parseJsonResponse(response);
  } catch {
    throw new AssessmentApiError("Received an invalid JSON response from the API.", response.status);
  }

  if (!response.ok) {
    throw new AssessmentApiError(
      readErrorMessage(payload, "Failed to load the assessment."),
      response.status,
    );
  }

  return AssessmentSchema.parse(payload);
}

export async function createAssessment(input: AssessmentCreate): Promise<Assessment> {
  const payload = AssessmentCreateSchema.parse(input);
  const response = await apiFetch("/assessment", {
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
    throw new AssessmentApiError("Received an invalid JSON response from the API.", response.status);
  }

  if (!response.ok) {
    throw new AssessmentApiError(
      readErrorMessage(responsePayload, "Failed to create the assessment draft."),
      response.status,
    );
  }

  return AssessmentSchema.parse(responsePayload);
}

export async function updateAssessment(input: AssessmentUpdate): Promise<Assessment> {
  const payload = AssessmentUpdateSchema.parse(input);
  const response = await apiFetch("/assessment", {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  let responsePayload: unknown;

  try {
    responsePayload = await parseJsonResponse(response);
  } catch {
    throw new AssessmentApiError("Received an invalid JSON response from the API.", response.status);
  }

  if (!response.ok) {
    throw new AssessmentApiError(
      readErrorMessage(responsePayload, "Failed to update the assessment draft."),
      response.status,
    );
  }

  return AssessmentSchema.parse(responsePayload);
}

export async function submitAssessment(input: AssessmentSubmit): Promise<Assessment> {
  const payload = AssessmentSubmitSchema.parse(input);
  const response = await apiFetch("/assessment/submit", {
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
    throw new AssessmentApiError("Received an invalid JSON response from the API.", response.status);
  }

  if (!response.ok) {
    throw new AssessmentApiError(
      readErrorMessage(responsePayload, "Failed to submit the assessment."),
      response.status,
    );
  }

  return AssessmentSchema.parse(responsePayload);
}
