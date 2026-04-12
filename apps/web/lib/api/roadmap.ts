import { RoadmapSchema, type Roadmap } from "@biasharamind/shared";

import { apiFetch, parseJsonResponse, readErrorMessage } from "@/lib/api/request";

class RoadmapApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "RoadmapApiError";
    this.status = status;
  }
}

export async function getRoadmap(): Promise<Roadmap | null> {
  const response = await apiFetch("/roadmap");

  if (response.status === 404) {
    return null;
  }

  let payload: unknown;

  try {
    payload = await parseJsonResponse(response);
  } catch {
    throw new RoadmapApiError("Received an invalid JSON response from the API.", response.status);
  }

  if (!response.ok) {
    throw new RoadmapApiError(
      readErrorMessage(payload, "Failed to load the roadmap."),
      response.status,
    );
  }

  return RoadmapSchema.parse(payload);
}

export async function generateRoadmap(): Promise<Roadmap> {
  const response = await apiFetch("/roadmap/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });

  let payload: unknown;

  try {
    payload = await parseJsonResponse(response);
  } catch {
    throw new RoadmapApiError("Received an invalid JSON response from the API.", response.status);
  }

  if (!response.ok) {
    throw new RoadmapApiError(
      readErrorMessage(payload, "Failed to generate the roadmap."),
      response.status,
    );
  }

  return RoadmapSchema.parse(payload);
}
