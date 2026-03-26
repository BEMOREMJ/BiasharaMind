import {
  BusinessProfileCreateSchema,
  BusinessProfileSchema,
  BusinessProfileUpdateSchema,
  type BusinessProfile,
  type BusinessProfileCreate,
  type BusinessProfileUpdate,
} from "@biasharamind/shared";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

class BusinessProfileApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "BusinessProfileApiError";
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
    throw new BusinessProfileApiError(
      "Received an invalid JSON response from the API.",
      response.status,
    );
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

export async function getBusinessProfile(): Promise<BusinessProfile | null> {
  const response = await fetch(`${API_BASE_URL}/business-profile`, {
    cache: "no-store",
  });

  if (response.status === 404) {
    return null;
  }

  const payload = await parseJsonResponse(response);

  if (!response.ok) {
    throw new BusinessProfileApiError(
      readErrorMessage(payload, "Failed to load the business profile."),
      response.status,
    );
  }

  return BusinessProfileSchema.parse(payload);
}

export async function createBusinessProfile(
  input: BusinessProfileCreate,
): Promise<BusinessProfile> {
  const payload = BusinessProfileCreateSchema.parse(input);
  const response = await fetch(`${API_BASE_URL}/business-profile`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const responsePayload = await parseJsonResponse(response);

  if (!response.ok) {
    throw new BusinessProfileApiError(
      readErrorMessage(responsePayload, "Failed to create the business profile."),
      response.status,
    );
  }

  return BusinessProfileSchema.parse(responsePayload);
}

export async function updateBusinessProfile(
  input: BusinessProfileUpdate,
): Promise<BusinessProfile> {
  const payload = BusinessProfileUpdateSchema.parse(input);
  const response = await fetch(`${API_BASE_URL}/business-profile`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const responsePayload = await parseJsonResponse(response);

  if (!response.ok) {
    throw new BusinessProfileApiError(
      readErrorMessage(responsePayload, "Failed to update the business profile."),
      response.status,
    );
  }

  return BusinessProfileSchema.parse(responsePayload);
}
