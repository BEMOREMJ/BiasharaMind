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

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

class AssessmentApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "AssessmentApiError";
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
    throw new AssessmentApiError("Received an invalid JSON response from the API.", response.status);
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

export async function getAssessment(): Promise<Assessment | null> {
  const response = await fetch(`${API_BASE_URL}/assessment`, {
    cache: "no-store",
  });

  if (response.status === 404) {
    return null;
  }

  const payload = await parseJsonResponse(response);

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
  const response = await fetch(`${API_BASE_URL}/assessment`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const responsePayload = await parseJsonResponse(response);

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
  const response = await fetch(`${API_BASE_URL}/assessment`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const responsePayload = await parseJsonResponse(response);

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
  const response = await fetch(`${API_BASE_URL}/assessment/submit`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const responsePayload = await parseJsonResponse(response);

  if (!response.ok) {
    throw new AssessmentApiError(
      readErrorMessage(responsePayload, "Failed to submit the assessment."),
      response.status,
    );
  }

  return AssessmentSchema.parse(responsePayload);
}
