import {
  V2BusinessProfileCreateSchema,
  V2BusinessProfileReadSchema,
  V2BusinessProfileSaveResponseSchema,
  type V2BusinessProfileCreate,
  type V2BusinessProfileRead,
  type V2BusinessProfileSaveResponse,
} from "@biasharamind/shared";

import { apiFetch, parseJsonResponse, readErrorMessage } from "@/lib/api/request";

class BusinessProfileV2ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "BusinessProfileV2ApiError";
    this.status = status;
  }
}

export async function getBusinessProfileV2(): Promise<V2BusinessProfileRead | null> {
  const response = await apiFetch("/v2/business-profile");

  if (response.status === 404) {
    return null;
  }

  let payload: unknown;

  try {
    payload = await parseJsonResponse(response);
  } catch {
    throw new BusinessProfileV2ApiError("Received an invalid JSON response from the API.", response.status);
  }

  if (!response.ok) {
    throw new BusinessProfileV2ApiError(
      readErrorMessage(payload, "Failed to load the V2 business profile."),
      response.status,
    );
  }

  return V2BusinessProfileReadSchema.parse(payload);
}

export async function saveBusinessProfileV2(
  input: V2BusinessProfileCreate,
): Promise<V2BusinessProfileSaveResponse> {
  const payload = V2BusinessProfileCreateSchema.parse(input);
  const response = await apiFetch("/v2/business-profile", {
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
    throw new BusinessProfileV2ApiError("Received an invalid JSON response from the API.", response.status);
  }

  if (!response.ok) {
    throw new BusinessProfileV2ApiError(
      readErrorMessage(responsePayload, "Failed to save the V2 business profile."),
      response.status,
    );
  }

  return V2BusinessProfileSaveResponseSchema.parse(responsePayload);
}
