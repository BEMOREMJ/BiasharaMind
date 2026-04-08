import { RoadmapSchema, type Roadmap } from "@biasharamind/shared";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

class RoadmapApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "RoadmapApiError";
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
    throw new RoadmapApiError("Received an invalid JSON response from the API.", response.status);
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

export async function getRoadmap(): Promise<Roadmap | null> {
  const response = await fetch(`${API_BASE_URL}/roadmap`, {
    cache: "no-store",
  });

  if (response.status === 404) {
    return null;
  }

  const payload = await parseJsonResponse(response);

  if (!response.ok) {
    throw new RoadmapApiError(
      readErrorMessage(payload, "Failed to load the roadmap."),
      response.status,
    );
  }

  return RoadmapSchema.parse(payload);
}

export async function generateRoadmap(): Promise<Roadmap> {
  const response = await fetch(`${API_BASE_URL}/roadmap/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });

  const payload = await parseJsonResponse(response);

  if (!response.ok) {
    throw new RoadmapApiError(
      readErrorMessage(payload, "Failed to generate the roadmap."),
      response.status,
    );
  }

  return RoadmapSchema.parse(payload);
}
