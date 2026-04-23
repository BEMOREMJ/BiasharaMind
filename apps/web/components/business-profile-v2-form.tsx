"use client";

import {
  V2BudgetFlexibilitySchema,
  V2BusinessAgeStageSchema,
  V2BusinessProfileCreateSchema,
  V2BusinessProfileReadSchema,
  V2ComplianceSectorSensitivitySchema,
  V2CreditSalesExposureSchema,
  V2CustomerTypeSchema,
  V2FulfilmentModelSchema,
  V2InventoryInvolvementSchema,
  V2MonthlyRevenueBandSchema,
  V2OwnerInvolvementLevelSchema,
  V2PeakPeriodSchema,
  V2PrimaryBusinessGoalSchema,
  V2PrimaryBusinessTypeSchema,
  V2RecordAvailabilitySchema,
  V2SalesChannelSchema,
  V2SeasonalityLevelSchema,
  V2TeamSizeBandSchema,
  V2TimeCapacitySchema,
  V2ToolHireOpennessSchema,
  type V2BusinessProfileCreate,
  type V2BusinessProfileRead,
  type V2BusinessProfileSaveResponse,
} from "@biasharamind/shared";
import { useEffect, useState, type FormEvent } from "react";

import { Badge } from "@/components/badge";
import { DashboardCard } from "@/components/dashboard-card";
import { InputField } from "@/components/input-field";
import { PrimaryButton } from "@/components/primary-button";
import { SecondaryButton } from "@/components/secondary-button";
import { SectionHeader } from "@/components/section-header";
import {
  getBusinessProfileV2,
  saveBusinessProfileV2,
} from "@/lib/api/business-profile-v2";

type FormState = {
  businessAgeStage: string;
  businessName: string;
  budgetFlexibility: string;
  complianceSectorSensitivity: string;
  creditSalesExposure: string;
  customerType: string;
  fulfilmentModel: string;
  inventoryInvolvement: string;
  mainOffer: string;
  monthlyRevenueBand: string;
  numberOfLocations: string;
  ownerInvolvementLevel: string;
  peakPeriods: string[];
  primaryBusinessGoal: string;
  primaryBusinessType: string;
  recordAvailability: string;
  salesChannels: string[];
  seasonalityLevel: string;
  teamSizeBand: string;
  timeCapacity: string;
  toolHireOpenness: string;
};

type Option = {
  label: string;
  value: string;
};

function labelize(value: string): string {
  return value
    .replace(/_/g, " ")
    .replace(/\bUsd\b/gi, "USD")
    .replace(/\bB2c\b/g, "B2C")
    .replace(/\bB2b\b/g, "B2B")
    .replace(/\bTo\b/g, "to")
    .replace(/\bAnd\b/g, "and")
    .replace(/\bOr\b/g, "or")
    .replace(/\bV2\b/g, "V2")
    .replace(/\w\S*/g, (segment) => segment.charAt(0).toUpperCase() + segment.slice(1));
}

function buildOptions(values: readonly string[]): Option[] {
  return values.map((value) => ({
    label: labelize(value),
    value,
  }));
}

const primaryBusinessTypeOptions = buildOptions(V2PrimaryBusinessTypeSchema.options);
const customerTypeOptions = buildOptions(V2CustomerTypeSchema.options);
const salesChannelOptions = buildOptions(V2SalesChannelSchema.options);
const fulfilmentModelOptions = buildOptions(V2FulfilmentModelSchema.options);
const inventoryOptions = buildOptions(V2InventoryInvolvementSchema.options);
const creditExposureOptions = buildOptions(V2CreditSalesExposureSchema.options);
const businessAgeStageOptions = buildOptions(V2BusinessAgeStageSchema.options);
const teamSizeBandOptions = buildOptions(V2TeamSizeBandSchema.options);
const monthlyRevenueBandOptions = buildOptions(V2MonthlyRevenueBandSchema.options);
const seasonalityOptions = buildOptions(V2SeasonalityLevelSchema.options);
const peakPeriodOptions = buildOptions(V2PeakPeriodSchema.options);
const ownerInvolvementOptions = buildOptions(V2OwnerInvolvementLevelSchema.options);
const primaryGoalOptions = buildOptions(V2PrimaryBusinessGoalSchema.options);
const timeCapacityOptions = buildOptions(V2TimeCapacitySchema.options);
const budgetFlexibilityOptions = buildOptions(V2BudgetFlexibilitySchema.options);
const toolHireOpennessOptions = buildOptions(V2ToolHireOpennessSchema.options);
const recordAvailabilityOptions = buildOptions(V2RecordAvailabilitySchema.options);
const complianceOptions = buildOptions(V2ComplianceSectorSensitivitySchema.options);

const defaultFormState: FormState = {
  businessAgeStage: V2BusinessAgeStageSchema.options[0],
  businessName: "",
  budgetFlexibility: V2BudgetFlexibilitySchema.options[0],
  complianceSectorSensitivity: "",
  creditSalesExposure: V2CreditSalesExposureSchema.options[0],
  customerType: V2CustomerTypeSchema.options[0],
  fulfilmentModel: V2FulfilmentModelSchema.options[0],
  inventoryInvolvement: V2InventoryInvolvementSchema.options[0],
  mainOffer: "",
  monthlyRevenueBand: V2MonthlyRevenueBandSchema.options[0],
  numberOfLocations: "1",
  ownerInvolvementLevel: V2OwnerInvolvementLevelSchema.options[0],
  peakPeriods: [],
  primaryBusinessGoal: V2PrimaryBusinessGoalSchema.options[0],
  primaryBusinessType: V2PrimaryBusinessTypeSchema.options[0],
  recordAvailability: V2RecordAvailabilitySchema.options[0],
  salesChannels: [V2SalesChannelSchema.options[0]],
  seasonalityLevel: "",
  teamSizeBand: V2TeamSizeBandSchema.options[0],
  timeCapacity: V2TimeCapacitySchema.options[0],
  toolHireOpenness: V2ToolHireOpennessSchema.options[0],
};

function toFormState(profile: V2BusinessProfileRead): FormState {
  return {
    businessAgeStage: profile.businessAgeStage,
    businessName: profile.businessName,
    budgetFlexibility: profile.improvementCapacity.budgetFlexibility,
    complianceSectorSensitivity: profile.complianceSectorSensitivity ?? "",
    creditSalesExposure: profile.creditSalesExposure,
    customerType: profile.customerType,
    fulfilmentModel: profile.fulfilmentModel,
    inventoryInvolvement: profile.inventoryInvolvement,
    mainOffer: profile.mainOffer,
    monthlyRevenueBand: profile.monthlyRevenueBand,
    numberOfLocations: String(profile.numberOfLocations),
    ownerInvolvementLevel: profile.ownerInvolvementLevel,
    peakPeriods: profile.peakPeriods ?? [],
    primaryBusinessGoal: profile.primaryBusinessGoal,
    primaryBusinessType: profile.primaryBusinessType,
    recordAvailability: profile.recordAvailability,
    salesChannels: profile.salesChannels,
    seasonalityLevel: profile.seasonalityLevel ?? "",
    teamSizeBand: profile.teamSizeBand,
    timeCapacity: profile.improvementCapacity.timeCapacity,
    toolHireOpenness: profile.improvementCapacity.toolHireOpenness,
  };
}

function toPayload(formState: FormState): V2BusinessProfileCreate {
  return V2BusinessProfileCreateSchema.parse({
    businessName: formState.businessName.trim(),
    primaryBusinessType: formState.primaryBusinessType,
    mainOffer: formState.mainOffer.trim(),
    customerType: formState.customerType,
    salesChannels: formState.salesChannels,
    fulfilmentModel: formState.fulfilmentModel,
    inventoryInvolvement: formState.inventoryInvolvement,
    creditSalesExposure: formState.creditSalesExposure,
    businessAgeStage: formState.businessAgeStage,
    teamSizeBand: formState.teamSizeBand,
    numberOfLocations: Number(formState.numberOfLocations),
    monthlyRevenueBand: formState.monthlyRevenueBand,
    seasonalityLevel: formState.seasonalityLevel || null,
    peakPeriods: formState.peakPeriods.length > 0 ? formState.peakPeriods : null,
    ownerInvolvementLevel: formState.ownerInvolvementLevel,
    primaryBusinessGoal: formState.primaryBusinessGoal,
    improvementCapacity: {
      timeCapacity: formState.timeCapacity,
      budgetFlexibility: formState.budgetFlexibility,
      toolHireOpenness: formState.toolHireOpenness,
    },
    recordAvailability: formState.recordAvailability,
    complianceSectorSensitivity: formState.complianceSectorSensitivity || null,
  });
}

function SummaryItem({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt>{label}</dt>
      <dd>{value}</dd>
    </div>
  );
}

function MultiSelectField({
  hint,
  label,
  onToggle,
  options,
  selectedValues,
}: {
  hint?: string;
  label: string;
  onToggle: (value: string) => void;
  options: readonly Option[];
  selectedValues: readonly string[];
}) {
  return (
    <div className="multi-select-field">
      <div className="multi-select-field__header">
        <span className="input-field__label">{label}</span>
        {hint ? <span className="input-field__hint">{hint}</span> : null}
      </div>
      <div className="checkbox-grid">
        {options.map((option) => {
          const checked = selectedValues.includes(option.value);

          return (
            <label className={`checkbox-chip ${checked ? "checkbox-chip--selected" : ""}`} key={option.value}>
              <input
                checked={checked}
                onChange={() => onToggle(option.value)}
                type="checkbox"
              />
              <span>{option.label}</span>
            </label>
          );
        })}
      </div>
    </div>
  );
}

export function BusinessProfileV2Form() {
  const [formState, setFormState] = useState<FormState>(defaultFormState);
  const [savedProfile, setSavedProfile] = useState<V2BusinessProfileRead | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [staleMessage, setStaleMessage] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    async function loadProfile() {
      try {
        const profile = await getBusinessProfileV2();

        if (!active) {
          return;
        }

        if (profile) {
          const parsedProfile = V2BusinessProfileReadSchema.parse(profile);
          setSavedProfile(parsedProfile);
          setFormState(toFormState(parsedProfile));
          setStatusMessage("Loaded the saved V2 business profile.");
        } else {
          setSavedProfile(null);
          setStatusMessage("No V2 business profile saved yet. Complete the form to create one.");
        }
      } catch (error) {
        if (!active) {
          return;
        }

        setErrorMessage(
          error instanceof Error ? error.message : "Failed to load the V2 business profile.",
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

  function toggleMultiSelect(key: "salesChannels" | "peakPeriods", value: string) {
    setFormState((current) => {
      const currentValues = current[key];
      return {
        ...current,
        [key]: currentValues.includes(value)
          ? currentValues.filter((item) => item !== value)
          : [...currentValues, value],
      };
    });
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSaving(true);
    setErrorMessage(null);
    setStatusMessage(null);
    setStaleMessage(null);

    try {
      const payload = toPayload(formState);
      const response: V2BusinessProfileSaveResponse = await saveBusinessProfileV2(payload);

      setSavedProfile(response.profile);
      setFormState(toFormState(response.profile));
      setStatusMessage(savedProfile ? "V2 business profile updated." : "V2 business profile created.");
      if (response.analysisImpact.rerunRequired) {
        setStaleMessage(
          response.analysisImpact.message ??
            "Your business context changed. Future V2 analysis should be rerun to reflect the latest profile.",
        );
      }
    } catch (error) {
      setErrorMessage(
        error instanceof Error ? error.message : "Unable to save the V2 business profile.",
      );
    } finally {
      setIsSaving(false);
    }
  }

  function handleReset() {
    if (savedProfile) {
      setFormState(toFormState(savedProfile));
      setStatusMessage("Form reset to the last saved V2 business profile.");
    } else {
      setFormState(defaultFormState);
      setStatusMessage("Form cleared.");
    }
    setErrorMessage(null);
    setStaleMessage(null);
  }

  const isProfileSaved = Boolean(savedProfile);

  return (
    <div className="dashboard-stack">
      <DashboardCard tone="hero" title="Business profile V2">
        <div className="dashboard-stack">
          <Badge tone={isProfileSaved ? "success" : "default"}>
            {isProfileSaved ? "V2 profile saved" : "V2 profile preview"}
          </Badge>
          <SectionHeader
            title="Business profile V2"
            eyebrow="Slice 2"
            description="Capture the fuller business context used for V2 routing, tailoring, feasibility, and interpretation without changing how V1 works."
          />
          <p className="muted-copy">
            This page is intentionally isolated from the existing V1 business profile flow so we can exercise the new V2 profile safely.
          </p>
        </div>
      </DashboardCard>

      <div className="dashboard-grid dashboard-grid--business">
        <DashboardCard
          title="V2 profile details"
          description="Save the current operating context that future V2 analysis should use."
        >
          {isLoading ? <p className="muted-copy">Loading V2 business profile...</p> : null}
          {!isLoading ? (
            <form className="form-grid" onSubmit={handleSubmit}>
              <div className="form-grid__full profile-section">
                <h3 className="profile-section__title">Business basics</h3>
                <div className="form-grid">
                  <InputField
                    id="v2-business-name"
                    label="Business name"
                    onChange={(event) => handleFieldChange("businessName", event.target.value)}
                    placeholder="BiasharaMind Foods"
                    value={formState.businessName}
                  />
                  <InputField
                    control="select"
                    id="v2-primary-business-type"
                    label="Primary business type"
                    onChange={(event) => handleFieldChange("primaryBusinessType", event.target.value)}
                    options={primaryBusinessTypeOptions}
                    value={formState.primaryBusinessType}
                  />
                  <div className="form-grid__full">
                    <InputField
                      id="v2-main-offer"
                      label="Main offer"
                      onChange={(event) => handleFieldChange("mainOffer", event.target.value)}
                      placeholder="Prepared meals and event catering"
                      value={formState.mainOffer}
                    />
                  </div>
                  <InputField
                    control="select"
                    id="v2-customer-type"
                    label="Customer type"
                    onChange={(event) => handleFieldChange("customerType", event.target.value)}
                    options={customerTypeOptions}
                    value={formState.customerType}
                  />
                  <InputField
                    control="select"
                    id="v2-team-size-band"
                    label="Team size band"
                    onChange={(event) => handleFieldChange("teamSizeBand", event.target.value)}
                    options={teamSizeBandOptions}
                    value={formState.teamSizeBand}
                  />
                </div>
              </div>

              <div className="form-grid__full profile-section">
                <h3 className="profile-section__title">How the business operates</h3>
                <div className="form-grid">
                  <div className="form-grid__full">
                    <MultiSelectField
                      hint="Select every channel that meaningfully contributes to current sales."
                      label="Sales channels"
                      onToggle={(value) => toggleMultiSelect("salesChannels", value)}
                      options={salesChannelOptions}
                      selectedValues={formState.salesChannels}
                    />
                  </div>
                  <InputField
                    control="select"
                    id="v2-fulfilment-model"
                    label="Fulfilment model"
                    onChange={(event) => handleFieldChange("fulfilmentModel", event.target.value)}
                    options={fulfilmentModelOptions}
                    value={formState.fulfilmentModel}
                  />
                  <InputField
                    control="select"
                    id="v2-inventory-involvement"
                    label="Inventory involvement"
                    onChange={(event) => handleFieldChange("inventoryInvolvement", event.target.value)}
                    options={inventoryOptions}
                    value={formState.inventoryInvolvement}
                  />
                  <InputField
                    control="select"
                    id="v2-credit-sales-exposure"
                    label="Credit sales exposure"
                    onChange={(event) => handleFieldChange("creditSalesExposure", event.target.value)}
                    options={creditExposureOptions}
                    value={formState.creditSalesExposure}
                  />
                  <InputField
                    control="select"
                    id="v2-business-age-stage"
                    label="Business age stage"
                    onChange={(event) => handleFieldChange("businessAgeStage", event.target.value)}
                    options={businessAgeStageOptions}
                    value={formState.businessAgeStage}
                  />
                </div>
              </div>

              <div className="form-grid__full profile-section">
                <h3 className="profile-section__title">Growth and financial context</h3>
                <div className="form-grid">
                  <InputField
                    id="v2-number-of-locations"
                    label="Number of locations"
                    min="1"
                    onChange={(event) => handleFieldChange("numberOfLocations", event.target.value)}
                    type="number"
                    value={formState.numberOfLocations}
                  />
                  <InputField
                    control="select"
                    id="v2-monthly-revenue-band"
                    label="Monthly revenue band"
                    onChange={(event) => handleFieldChange("monthlyRevenueBand", event.target.value)}
                    options={monthlyRevenueBandOptions}
                    value={formState.monthlyRevenueBand}
                  />
                  <InputField
                    control="select"
                    id="v2-seasonality-level"
                    label="Seasonality level"
                    onChange={(event) => handleFieldChange("seasonalityLevel", event.target.value)}
                    options={[{ label: "Not set", value: "" }, ...seasonalityOptions]}
                    value={formState.seasonalityLevel}
                  />
                  <InputField
                    control="select"
                    id="v2-primary-business-goal"
                    label="Primary business goal"
                    onChange={(event) => handleFieldChange("primaryBusinessGoal", event.target.value)}
                    options={primaryGoalOptions}
                    value={formState.primaryBusinessGoal}
                  />
                  <div className="form-grid__full">
                    <MultiSelectField
                      hint="Optional. Use this when the business has clear high-demand periods."
                      label="Peak periods"
                      onToggle={(value) => toggleMultiSelect("peakPeriods", value)}
                      options={peakPeriodOptions}
                      selectedValues={formState.peakPeriods}
                    />
                  </div>
                </div>
              </div>

              <div className="form-grid__full profile-section">
                <h3 className="profile-section__title">Owner role and improvement capacity</h3>
                <div className="form-grid">
                  <InputField
                    control="select"
                    id="v2-owner-involvement-level"
                    label="Owner involvement level"
                    onChange={(event) => handleFieldChange("ownerInvolvementLevel", event.target.value)}
                    options={ownerInvolvementOptions}
                    value={formState.ownerInvolvementLevel}
                  />
                  <InputField
                    control="select"
                    id="v2-time-capacity"
                    label="Time capacity"
                    onChange={(event) => handleFieldChange("timeCapacity", event.target.value)}
                    options={timeCapacityOptions}
                    value={formState.timeCapacity}
                  />
                  <InputField
                    control="select"
                    id="v2-budget-flexibility"
                    label="Budget flexibility"
                    onChange={(event) => handleFieldChange("budgetFlexibility", event.target.value)}
                    options={budgetFlexibilityOptions}
                    value={formState.budgetFlexibility}
                  />
                  <InputField
                    control="select"
                    id="v2-tool-hire-openness"
                    label="Tool or hire openness"
                    onChange={(event) => handleFieldChange("toolHireOpenness", event.target.value)}
                    options={toolHireOpennessOptions}
                    value={formState.toolHireOpenness}
                  />
                </div>
              </div>

              <div className="form-grid__full profile-section">
                <h3 className="profile-section__title">Data, readiness, and compliance context</h3>
                <div className="form-grid">
                  <InputField
                    control="select"
                    id="v2-record-availability"
                    label="Record availability"
                    onChange={(event) => handleFieldChange("recordAvailability", event.target.value)}
                    options={recordAvailabilityOptions}
                    value={formState.recordAvailability}
                  />
                  <InputField
                    control="select"
                    id="v2-compliance-sector-sensitivity"
                    label="Compliance sector sensitivity"
                    onChange={(event) =>
                      handleFieldChange("complianceSectorSensitivity", event.target.value)
                    }
                    options={[{ label: "Not set", value: "" }, ...complianceOptions]}
                    value={formState.complianceSectorSensitivity}
                  />
                </div>
              </div>

              {(statusMessage || errorMessage || staleMessage) && (
                <div className="form-grid__full status-stack">
                  {statusMessage ? (
                    <div className="status-banner status-banner--success">{statusMessage}</div>
                  ) : null}
                  {staleMessage ? (
                    <div className="status-banner status-banner--warning">{staleMessage}</div>
                  ) : null}
                  {errorMessage ? (
                    <div className="status-banner status-banner--error">{errorMessage}</div>
                  ) : null}
                </div>
              )}

              <div className="form-grid__full button-row">
                <PrimaryButton disabled={isLoading || isSaving} type="submit">
                  {isSaving ? "Saving..." : isProfileSaved ? "Update V2 profile" : "Create V2 profile"}
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
          title="Saved V2 profile"
          description="The most recent V2 profile from the backend is shown here for quick verification."
        >
          {savedProfile ? (
            <dl className="summary-list">
              <SummaryItem label="Business name" value={savedProfile.businessName} />
              <SummaryItem label="Primary business type" value={labelize(savedProfile.primaryBusinessType)} />
              <SummaryItem label="Main offer" value={savedProfile.mainOffer} />
              <SummaryItem label="Customer type" value={labelize(savedProfile.customerType)} />
              <SummaryItem label="Sales channels" value={savedProfile.salesChannels.map(labelize).join(", ")} />
              <SummaryItem label="Fulfilment model" value={labelize(savedProfile.fulfilmentModel)} />
              <SummaryItem label="Inventory involvement" value={labelize(savedProfile.inventoryInvolvement)} />
              <SummaryItem label="Credit sales exposure" value={labelize(savedProfile.creditSalesExposure)} />
              <SummaryItem label="Business age stage" value={labelize(savedProfile.businessAgeStage)} />
              <SummaryItem label="Team size band" value={labelize(savedProfile.teamSizeBand)} />
              <SummaryItem label="Number of locations" value={String(savedProfile.numberOfLocations)} />
              <SummaryItem label="Monthly revenue band" value={labelize(savedProfile.monthlyRevenueBand)} />
              <SummaryItem label="Seasonality level" value={savedProfile.seasonalityLevel ? labelize(savedProfile.seasonalityLevel) : "Not set"} />
              <SummaryItem label="Peak periods" value={savedProfile.peakPeriods?.length ? savedProfile.peakPeriods.map(labelize).join(", ") : "Not set"} />
              <SummaryItem label="Owner involvement level" value={labelize(savedProfile.ownerInvolvementLevel)} />
              <SummaryItem label="Primary business goal" value={labelize(savedProfile.primaryBusinessGoal)} />
              <SummaryItem label="Time capacity" value={labelize(savedProfile.improvementCapacity.timeCapacity)} />
              <SummaryItem label="Budget flexibility" value={labelize(savedProfile.improvementCapacity.budgetFlexibility)} />
              <SummaryItem label="Tool or hire openness" value={labelize(savedProfile.improvementCapacity.toolHireOpenness)} />
              <SummaryItem label="Record availability" value={labelize(savedProfile.recordAvailability)} />
              <SummaryItem label="Compliance sensitivity" value={savedProfile.complianceSectorSensitivity ? labelize(savedProfile.complianceSectorSensitivity) : "Not set"} />
              <SummaryItem label="Created at" value={savedProfile.createdAt} />
              <SummaryItem label="Updated at" value={savedProfile.updatedAt} />
            </dl>
          ) : (
            <p className="muted-copy">
              No V2 business profile has been saved yet. Submit the form to create the first one.
            </p>
          )}
        </DashboardCard>
      </div>
    </div>
  );
}
