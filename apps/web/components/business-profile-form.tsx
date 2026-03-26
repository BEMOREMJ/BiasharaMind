"use client";

import {
  BudgetBandSchema,
  BusinessProfileCreateSchema,
  BusinessProfileSchema,
  BusinessSizeBandSchema,
  IndustrySchema,
  RevenueBandSchema,
  type BusinessProfile,
  type BusinessProfileCreate,
} from "@biasharamind/shared";
import { useEffect, useState, type FormEvent } from "react";

import { Badge } from "@/components/badge";
import { DashboardCard } from "@/components/dashboard-card";
import { InputField } from "@/components/input-field";
import { PrimaryButton } from "@/components/primary-button";
import { SecondaryButton } from "@/components/secondary-button";
import { SectionHeader } from "@/components/section-header";
import {
  createBusinessProfile,
  getBusinessProfile,
  updateBusinessProfile,
} from "@/lib/api/business-profile";

type FormState = {
  budgetBand: BusinessProfileCreate["budgetBand"];
  businessName: string;
  country: string;
  currentTools: string;
  industry: BusinessProfileCreate["industry"];
  mainGoal: string;
  revenueBand: BusinessProfileCreate["revenueBand"];
  sizeBand: BusinessProfileCreate["sizeBand"];
  teamSize: string;
  yearsOperating: string;
};

function startCase(value: string): string {
  return value
    .split("_")
    .map((segment) => segment.charAt(0).toUpperCase() + segment.slice(1))
    .join(" ");
}

function humanizeBand(value: string): string {
  return value
    .replace(/_/g, " ")
    .replace(/\bUsd\b/gi, "USD")
    .replace(/\bTo\b/g, "to");
}

const industryOptions = IndustrySchema.options.map((value) => ({
  label: startCase(value),
  value,
}));

const sizeBandOptions = BusinessSizeBandSchema.options.map((value) => ({
  label: startCase(value),
  value,
}));

const revenueBandOptions = RevenueBandSchema.options.map((value) => ({
  label: humanizeBand(value),
  value,
}));

const budgetBandOptions = BudgetBandSchema.options.map((value) => ({
  label: humanizeBand(value),
  value,
}));

const defaultFormState: FormState = {
  budgetBand: BudgetBandSchema.options[0],
  businessName: "",
  country: "",
  currentTools: "",
  industry: IndustrySchema.options[0],
  mainGoal: "",
  revenueBand: RevenueBandSchema.options[0],
  sizeBand: BusinessSizeBandSchema.options[0],
  teamSize: "",
  yearsOperating: "",
};

function toFormState(profile: BusinessProfile): FormState {
  return {
    budgetBand: profile.budgetBand,
    businessName: profile.businessName,
    country: profile.country,
    currentTools: profile.currentTools.join(", "),
    industry: profile.industry,
    mainGoal: profile.mainGoal,
    revenueBand: profile.revenueBand,
    sizeBand: profile.sizeBand,
    teamSize: String(profile.teamSize),
    yearsOperating: String(profile.yearsOperating),
  };
}

function toPayload(formState: FormState): BusinessProfileCreate {
  return BusinessProfileCreateSchema.parse({
    budgetBand: formState.budgetBand,
    businessName: formState.businessName.trim(),
    country: formState.country.trim().toUpperCase(),
    currentTools: formState.currentTools
      .split(",")
      .map((tool) => tool.trim())
      .filter(Boolean),
    industry: formState.industry,
    mainGoal: formState.mainGoal.trim(),
    revenueBand: formState.revenueBand,
    sizeBand: formState.sizeBand,
    teamSize: Number(formState.teamSize),
    yearsOperating: Number(formState.yearsOperating),
  });
}

export function BusinessProfileForm() {
  const [formState, setFormState] = useState<FormState>(defaultFormState);
  const [savedProfile, setSavedProfile] = useState<BusinessProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    async function loadProfile() {
      try {
        const profile = await getBusinessProfile();

        if (!active) {
          return;
        }

        if (profile) {
          setSavedProfile(BusinessProfileSchema.parse(profile));
          setFormState(toFormState(profile));
          setStatusMessage("Loaded the current business profile.");
        } else {
          setSavedProfile(null);
          setStatusMessage("No saved business profile yet. Fill out the form to create one.");
        }
      } catch (error) {
        if (!active) {
          return;
        }

        setErrorMessage(
          error instanceof Error ? error.message : "Failed to load the business profile.",
        );
      } finally {
        if (active) {
          setIsLoading(false);
        }
      }
    }

    void loadProfile();

    return () => {
      active = false;
    };
  }, []);

  function handleFieldChange<K extends keyof FormState>(key: K, value: FormState[K]) {
    setFormState((current) => ({
      ...current,
      [key]: value,
    }));
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSaving(true);
    setErrorMessage(null);
    setStatusMessage(null);

    try {
      const payload = toPayload(formState);
      const profile = savedProfile
        ? await updateBusinessProfile(payload)
        : await createBusinessProfile(payload);

      setSavedProfile(profile);
      setFormState(toFormState(profile));
      setStatusMessage(savedProfile ? "Business profile updated." : "Business profile created.");
    } catch (error) {
      setErrorMessage(
        error instanceof Error ? error.message : "Unable to save the business profile.",
      );
    } finally {
      setIsSaving(false);
    }
  }

  function handleReset() {
    if (savedProfile) {
      setFormState(toFormState(savedProfile));
      setStatusMessage("Form reset to the last saved business profile.");
    } else {
      setFormState(defaultFormState);
      setStatusMessage("Form cleared.");
    }
    setErrorMessage(null);
  }

  const isProfileSaved = Boolean(savedProfile);

  return (
    <div className="dashboard-stack">
      <DashboardCard tone="hero" title="Business Profile">
        <div className="dashboard-stack">
          <Badge tone={isProfileSaved ? "success" : "default"}>
            {isProfileSaved ? "Saved profile" : "Create profile"}
          </Badge>
          <SectionHeader
            title="Business profile"
            eyebrow="Onboarding"
            description="Capture the core business context that BiasharaMind will use to tailor assessment scoring, recommendations, and future roadmap outputs."
          />
          <p className="muted-copy">
            This V1 flow stores data in a temporary in-memory backend service for now.
          </p>
        </div>
      </DashboardCard>

      <div className="dashboard-grid dashboard-grid--business">
        <DashboardCard
          title="Profile details"
          description="Create a profile if one does not exist, or update the saved profile later."
        >
          {isLoading ? <p className="muted-copy">Loading business profile...</p> : null}
          {!isLoading ? (
            <form className="form-grid" onSubmit={handleSubmit}>
              <InputField
                id="business-name"
                label="Business name"
                onChange={(event) => handleFieldChange("businessName", event.target.value)}
                placeholder="Sunrise Grocers"
                value={formState.businessName}
              />
              <InputField
                control="select"
                id="industry"
                label="Industry"
                onChange={(event) =>
                  handleFieldChange("industry", event.target.value as FormState["industry"])
                }
                options={industryOptions}
                value={formState.industry}
              />
              <InputField
                id="country"
                label="Country code"
                maxLength={2}
                onChange={(event) => handleFieldChange("country", event.target.value.toUpperCase())}
                placeholder="KE"
                value={formState.country}
              />
              <InputField
                control="select"
                id="size-band"
                label="Business size"
                onChange={(event) =>
                  handleFieldChange("sizeBand", event.target.value as FormState["sizeBand"])
                }
                options={sizeBandOptions}
                value={formState.sizeBand}
              />
              <InputField
                id="years-operating"
                label="Years operating"
                min="0"
                onChange={(event) => handleFieldChange("yearsOperating", event.target.value)}
                placeholder="6"
                type="number"
                value={formState.yearsOperating}
              />
              <InputField
                control="select"
                id="revenue-band"
                label="Revenue band"
                onChange={(event) =>
                  handleFieldChange("revenueBand", event.target.value as FormState["revenueBand"])
                }
                options={revenueBandOptions}
                value={formState.revenueBand}
              />
              <InputField
                id="team-size"
                label="Team size"
                min="1"
                onChange={(event) => handleFieldChange("teamSize", event.target.value)}
                placeholder="14"
                type="number"
                value={formState.teamSize}
              />
              <InputField
                control="select"
                id="budget-band"
                label="Budget band"
                onChange={(event) =>
                  handleFieldChange("budgetBand", event.target.value as FormState["budgetBand"])
                }
                options={budgetBandOptions}
                value={formState.budgetBand}
              />
              <div className="form-grid__full">
                <InputField
                  control="textarea"
                  hint="Keep this focused on the main growth or operational objective."
                  id="main-goal"
                  label="Main goal"
                  onChange={(event) => handleFieldChange("mainGoal", event.target.value)}
                  placeholder="Increase repeat customer sales without opening a second branch."
                  rows={4}
                  value={formState.mainGoal}
                />
              </div>
              <div className="form-grid__full">
                <InputField
                  control="textarea"
                  hint="Enter a comma-separated list, for example: WhatsApp Business, Google Sheets, M-Pesa"
                  id="current-tools"
                  label="Current tools"
                  onChange={(event) => handleFieldChange("currentTools", event.target.value)}
                  placeholder="WhatsApp Business, Google Sheets, M-Pesa"
                  rows={3}
                  value={formState.currentTools}
                />
              </div>
              {(statusMessage || errorMessage) && (
                <div className="form-grid__full">
                  <div
                    className={`status-banner ${
                      errorMessage ? "status-banner--error" : "status-banner--success"
                    }`}
                  >
                    {errorMessage ?? statusMessage}
                  </div>
                </div>
              )}
              <div className="form-grid__full button-row">
                <PrimaryButton disabled={isLoading || isSaving}>
                  {isSaving
                    ? "Saving..."
                    : isProfileSaved
                      ? "Update business profile"
                      : "Create business profile"}
                </PrimaryButton>
                <SecondaryButton
                  disabled={isLoading || isSaving}
                  onClick={handleReset}
                  type="button"
                >
                  Reset form
                </SecondaryButton>
              </div>
            </form>
          ) : null}
        </DashboardCard>

        <DashboardCard
          title="Saved state"
          description="The latest profile returned by the backend is shown here so the current persisted state is always visible."
        >
          {savedProfile ? (
            <dl className="summary-list">
              <div>
                <dt>Business name</dt>
                <dd>{savedProfile.businessName}</dd>
              </div>
              <div>
                <dt>Industry</dt>
                <dd>{startCase(savedProfile.industry)}</dd>
              </div>
              <div>
                <dt>Country</dt>
                <dd>{savedProfile.country}</dd>
              </div>
              <div>
                <dt>Size band</dt>
                <dd>{startCase(savedProfile.sizeBand)}</dd>
              </div>
              <div>
                <dt>Years operating</dt>
                <dd>{savedProfile.yearsOperating}</dd>
              </div>
              <div>
                <dt>Revenue band</dt>
                <dd>{humanizeBand(savedProfile.revenueBand)}</dd>
              </div>
              <div>
                <dt>Team size</dt>
                <dd>{savedProfile.teamSize}</dd>
              </div>
              <div>
                <dt>Budget band</dt>
                <dd>{humanizeBand(savedProfile.budgetBand)}</dd>
              </div>
              <div>
                <dt>Main goal</dt>
                <dd>{savedProfile.mainGoal}</dd>
              </div>
              <div>
                <dt>Current tools</dt>
                <dd>{savedProfile.currentTools.join(", ") || "None listed"}</dd>
              </div>
              <div>
                <dt>Created at</dt>
                <dd>{savedProfile.createdAt}</dd>
              </div>
              <div>
                <dt>Updated at</dt>
                <dd>{savedProfile.updatedAt}</dd>
              </div>
            </dl>
          ) : (
            <p className="muted-copy">
              No business profile has been saved yet. Submit the form to create the first profile.
            </p>
          )}
        </DashboardCard>
      </div>
    </div>
  );
}
