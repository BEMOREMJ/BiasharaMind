"use client";

import Link from "next/link";
import {
  type V2AssessmentAnswerPayload,
  type V2AssessmentDefinition,
  type V2AssessmentRead,
  type V2AssessmentResponseKind,
  type V2AssessmentSaveResponse,
  type V2QuestionDefinition,
} from "@biasharamind/shared";
import { useEffect, useMemo, useState, type FormEvent } from "react";

import { Badge } from "@/components/badge";
import { DashboardCard } from "@/components/dashboard-card";
import { InputField } from "@/components/input-field";
import { PrimaryButton } from "@/components/primary-button";
import { SecondaryButton } from "@/components/secondary-button";
import { SectionHeader } from "@/components/section-header";
import {
  AssessmentV2ApiError,
  getAssessmentDefinitionV2,
  getAssessmentV2,
  saveAssessmentV2,
  submitAssessmentV2,
} from "@/lib/api/assessment-v2";

type QuestionState = {
  responseKind: V2AssessmentResponseKind;
  value: string | number | string[] | null;
};

type QuestionStateMap = Record<string, QuestionState>;

type Option = {
  label: string;
  value: string;
};

function labelize(value: string): string {
  return value
    .replace(/_/g, " ")
    .replace(/\bUsd\b/gi, "USD")
    .replace(/\bTo\b/g, "to")
    .replace(/\bV2\b/g, "V2")
    .replace(/\w\S*/g, (segment) => segment.charAt(0).toUpperCase() + segment.slice(1));
}

function responseKindOptions(question: V2QuestionDefinition): Option[] {
  const options: Option[] = [{ label: "Answer this question", value: "answered" }];
  if (question.answerSpec.allowUnknown) {
    options.push({ label: "I don't know", value: "unknown" });
  }
  if (question.answerSpec.allowPreferNotToSay) {
    options.push({ label: "Prefer not to say", value: "prefer_not_to_say" });
  }
  return options;
}

function toStateMap(assessment: V2AssessmentRead | null): QuestionStateMap {
  if (!assessment) {
    return {};
  }

  return Object.fromEntries(
    assessment.answers.map((answer) => [
      answer.questionId,
      {
        responseKind: answer.responseKind,
        value: answer.value ?? null,
      },
    ]),
  );
}

function serializeAnswers(stateMap: QuestionStateMap): V2AssessmentAnswerPayload[] {
  return Object.entries(stateMap).reduce<V2AssessmentAnswerPayload[]>((accumulator, [questionId, state]) => {
    if (state.responseKind === "answered") {
      if (state.value === null || state.value === "" || (Array.isArray(state.value) && state.value.length === 0)) {
        return accumulator;
      }
    } else if (state.value !== null) {
      return accumulator;
    }

    accumulator.push({
      questionId,
      answerType: "text",
      responseKind: state.responseKind,
      value: state.responseKind === "answered" ? state.value : null,
    } as V2AssessmentAnswerPayload);

    return accumulator;
  }, []);
}

function MultiSelectField({
  label,
  options,
  selectedValues,
  onToggle,
  hint,
}: {
  label: string;
  options: readonly Option[];
  selectedValues: readonly string[];
  onToggle: (value: string) => void;
  hint?: string | null;
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

export function AssessmentV2Flow() {
  const [definition, setDefinition] = useState<V2AssessmentDefinition | null>(null);
  const [savedAssessment, setSavedAssessment] = useState<V2AssessmentRead | null>(null);
  const [stateMap, setStateMap] = useState<QuestionStateMap>({});
  const [currentSectionIndex, setCurrentSectionIndex] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [staleMessage, setStaleMessage] = useState<string | null>(null);
  const [profileRequired, setProfileRequired] = useState(false);

  const sections = definition?.sections ?? [];
  const currentSection = sections[currentSectionIndex] ?? null;
  const completedEssentialQuestions = useMemo(() => {
    if (!definition) {
      return 0;
    }
    return definition.sections
      .flatMap((section) => section.questions)
      .filter((question) => {
        if (!question.essential) {
          return false;
        }
        const state = stateMap[question.questionId];
        return state !== undefined;
      }).length;
  }, [definition, stateMap]);
  const totalEssentialQuestions = useMemo(
    () => definition?.sections.flatMap((section) => section.questions).filter((question) => question.essential).length ?? 0,
    [definition],
  );

  useEffect(() => {
    let active = true;

    async function loadV2Assessment() {
      try {
        const loadedDefinition = await getAssessmentDefinitionV2();
        const loadedAssessment = await getAssessmentV2();

        if (!active) {
          return;
        }

        setDefinition(loadedDefinition);
        setSavedAssessment(loadedAssessment);
        setStateMap(toStateMap(loadedAssessment));
        setStatusMessage(
          loadedAssessment
            ? "Loaded the current V2 assessment draft."
            : "No saved V2 assessment yet. Start answering and save when you’re ready.",
        );
      } catch (error) {
        if (!active) {
          return;
        }

        if (error instanceof AssessmentV2ApiError && error.status === 409) {
          setProfileRequired(true);
          setErrorMessage(error.message);
        } else {
          setErrorMessage(
            error instanceof Error ? error.message : "Failed to load the V2 assessment.",
          );
        }
      } finally {
        if (active) {
          setIsLoading(false);
        }
      }
    }

    void loadV2Assessment();

    return () => {
      active = false;
    };
  }, []);

  function setQuestionState(questionId: string, nextState: QuestionState) {
    setStateMap((current) => ({
      ...current,
      [questionId]: nextState,
    }));
  }

  function handleResponseKindChange(question: V2QuestionDefinition, nextKind: string) {
    setQuestionState(question.questionId, {
      responseKind: nextKind as V2AssessmentResponseKind,
      value: nextKind === "answered" ? stateMap[question.questionId]?.value ?? "" : null,
    });
  }

  function handleValueChange(question: V2QuestionDefinition, rawValue: string | number | string[] | null) {
    setQuestionState(question.questionId, {
      responseKind: stateMap[question.questionId]?.responseKind ?? "answered",
      value: rawValue,
    });
  }

  function toggleMultiSelect(question: V2QuestionDefinition, value: string) {
    const currentValue = stateMap[question.questionId]?.value;
    const selected = Array.isArray(currentValue) ? currentValue : [];

    handleValueChange(
      question,
      selected.includes(value)
        ? selected.filter((item) => item !== value)
        : [...selected, value],
    );
  }

  function buildPayload(): { answers: V2AssessmentAnswerPayload[] } {
    const questionMap = new Map(
      sections.flatMap((section) =>
        section.questions.map((question) => [question.questionId, question] as const),
      ),
    );

    const answers = Object.entries(stateMap).reduce<V2AssessmentAnswerPayload[]>((accumulator, [questionId, state]) => {
      const question = questionMap.get(questionId);
      if (!question) {
        return accumulator;
      }

      if (
        state.responseKind === "answered" &&
        (state.value === null || state.value === "" || (Array.isArray(state.value) && state.value.length === 0))
      ) {
        return accumulator;
      }

      accumulator.push({
        questionId,
        answerType: question.questionType,
        responseKind: state.responseKind,
        value: state.responseKind === "answered" ? state.value : null,
      });
      return accumulator;
    }, []);

    return { answers };
  }

  async function applyResponse(
    action: (payload: { answers: V2AssessmentAnswerPayload[] }) => Promise<V2AssessmentSaveResponse>,
    successMessage: string,
  ) {
    const response = await action(buildPayload());
    setSavedAssessment(response.assessment);
    setStateMap(toStateMap(response.assessment));
    setStatusMessage(successMessage);
    setStaleMessage(response.analysisImpact.message ?? null);
  }

  async function handleSave() {
    setIsSaving(true);
    setErrorMessage(null);
    setStatusMessage(null);
    setStaleMessage(null);

    try {
      await applyResponse(saveAssessmentV2, "V2 assessment progress saved.");
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Unable to save the V2 assessment.");
    } finally {
      setIsSaving(false);
    }
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSubmitting(true);
    setErrorMessage(null);
    setStatusMessage(null);
    setStaleMessage(null);

    try {
      await applyResponse(submitAssessmentV2, "V2 assessment submitted successfully.");
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Unable to submit the V2 assessment.");
    } finally {
      setIsSubmitting(false);
    }
  }

  if (profileRequired) {
    return (
      <div className="dashboard-stack">
        <DashboardCard tone="hero" title="V2 assessment">
          <div className="dashboard-stack">
            <Badge tone="warning">Profile needed</Badge>
            <SectionHeader
              title="V2 assessment"
              eyebrow="Slice 3"
              description="The V2 assessment uses your V2 business profile to decide which adaptive modules apply."
            />
            <div className="status-banner status-banner--warning">
              {errorMessage ?? "Complete the V2 business profile before starting the V2 assessment."}
            </div>
            <div className="button-row">
              <Link className="button button--primary" href="/business-v2">
                Go to V2 business profile
              </Link>
            </div>
          </div>
        </DashboardCard>
      </div>
    );
  }

  return (
    <div className="dashboard-stack">
      <DashboardCard tone="hero" title="Assessment V2">
        <div className="dashboard-stack">
          <Badge tone={savedAssessment?.status === "submitted" ? "success" : "default"}>
            {savedAssessment?.status === "submitted" ? "V2 assessment submitted" : "V2 assessment draft"}
          </Badge>
          <SectionHeader
            title="Assessment V2"
            eyebrow="Slice 3"
            description="Answer the backend-defined V2 assessment. Core sections are always included, and adaptive modules are selected from your saved V2 business profile."
          />
          <div className="stats-row">
            <div className="stat-chip">
              <strong>{sections.length}</strong>
              <span>Active sections</span>
            </div>
            <div className="stat-chip">
              <strong>{definition?.adaptiveModules.length ?? 0}</strong>
              <span>Adaptive modules</span>
            </div>
            <div className="stat-chip">
              <strong>{completedEssentialQuestions}/{totalEssentialQuestions}</strong>
              <span>Essential questions touched</span>
            </div>
          </div>
        </div>
      </DashboardCard>

      <div className="dashboard-grid dashboard-grid--assessment">
        <DashboardCard title="Section progress" description="Move through the V2 assessment one section at a time.">
          {isLoading ? <p className="muted-copy">Loading V2 assessment definition...</p> : null}
          {!isLoading && definition ? (
            <div className="assessment-progress">
              {sections.map((section, index) => {
                const complete = section.questions
                  .filter((question) => question.essential)
                  .every((question) => stateMap[question.questionId] !== undefined);

                return (
                  <button
                    className={`assessment-progress__item ${index === currentSectionIndex ? "assessment-progress__item--active" : ""}`}
                    key={section.sectionId}
                    onClick={() => setCurrentSectionIndex(index)}
                    type="button"
                  >
                    <span className="assessment-progress__step">{index + 1}</span>
                    <span>
                      <strong>{section.title}</strong>
                      <small>
                        {section.isCore ? "Core section" : "Adaptive module"}
                        {" • "}
                        {complete ? "Essential answers covered" : "Still in progress"}
                      </small>
                    </span>
                  </button>
                );
              })}
            </div>
          ) : null}
        </DashboardCard>

        <DashboardCard
          title={currentSection?.title ?? "Assessment section"}
          description={currentSection?.description ?? "The current section will appear here once the definition is loaded."}
        >
          {isLoading ? <p className="muted-copy">Preparing questions...</p> : null}
          {!isLoading && currentSection ? (
            <form className="form-grid" onSubmit={handleSubmit}>
              {currentSection.questions.map((question) => {
                const state = stateMap[question.questionId] ?? { responseKind: "answered", value: null };
                const options = question.answerSpec.options.map((option) => ({
                  label: option.label,
                  value: option.value,
                }));

                return (
                  <div className="form-grid__full question-card" key={question.questionId}>
                    <div className="question-card__header">
                      <div className="question-card__meta">
                        <span className="badge badge--default">
                          {question.essential ? "Essential" : "Supporting"}
                        </span>
                        <span className="muted-copy">Bucket: {labelize(question.bucket)}</span>
                      </div>
                      {(question.answerSpec.allowUnknown || question.answerSpec.allowPreferNotToSay) ? (
                        <InputField
                          control="select"
                          id={`${question.questionId}-response-kind`}
                          label="Response mode"
                          onChange={(event) => handleResponseKindChange(question, event.target.value)}
                          options={responseKindOptions(question)}
                          value={state.responseKind}
                        />
                      ) : null}
                    </div>

                    {state.responseKind === "answered" ? (
                      <>
                        {question.questionType === "select" ? (
                          <InputField
                            control="select"
                            hint={question.helpText ?? undefined}
                            id={question.questionId}
                            label={question.prompt}
                            onChange={(event) => handleValueChange(question, event.target.value)}
                            options={[{ label: "Select an option", value: "" }, ...options]}
                            value={typeof state.value === "string" ? state.value : ""}
                          />
                        ) : null}

                        {question.questionType === "number" ? (
                          <InputField
                            hint={question.helpText ?? undefined}
                            id={question.questionId}
                            label={question.prompt}
                            max={question.answerSpec.maxValue?.toString()}
                            min={question.answerSpec.minValue?.toString()}
                            onChange={(event) =>
                              handleValueChange(
                                question,
                                event.target.value === "" ? null : Number(event.target.value),
                              )
                            }
                            step={question.answerSpec.step?.toString()}
                            type="number"
                            value={typeof state.value === "number" ? state.value : ""}
                          />
                        ) : null}

                        {question.questionType === "textarea" ? (
                          <InputField
                            control="textarea"
                            hint={question.helpText ?? undefined}
                            id={question.questionId}
                            label={question.prompt}
                            onChange={(event) => handleValueChange(question, event.target.value)}
                            rows={5}
                            value={typeof state.value === "string" ? state.value : ""}
                          />
                        ) : null}

                        {question.questionType === "text" ? (
                          <InputField
                            hint={question.helpText ?? undefined}
                            id={question.questionId}
                            label={question.prompt}
                            onChange={(event) => handleValueChange(question, event.target.value)}
                            value={typeof state.value === "string" ? state.value : ""}
                          />
                        ) : null}

                        {question.questionType === "multiselect" ? (
                          <MultiSelectField
                            hint={question.helpText}
                            label={question.prompt}
                            onToggle={(value) => toggleMultiSelect(question, value)}
                            options={options}
                            selectedValues={Array.isArray(state.value) ? state.value : []}
                          />
                        ) : null}
                      </>
                    ) : (
                      <div className="status-banner status-banner--warning">
                        {state.responseKind === "unknown"
                          ? "Marked as “I don't know”."
                          : "Marked as “Prefer not to say”."}
                      </div>
                    )}
                  </div>
                );
              })}

              {(statusMessage || staleMessage || errorMessage) ? (
                <div className="form-grid__full status-stack">
                  {statusMessage ? <div className="status-banner status-banner--success">{statusMessage}</div> : null}
                  {staleMessage ? <div className="status-banner status-banner--warning">{staleMessage}</div> : null}
                  {errorMessage ? <div className="status-banner status-banner--error">{errorMessage}</div> : null}
                </div>
              ) : null}

              <div className="form-grid__full section-actions">
                <div className="button-row">
                  <SecondaryButton
                    disabled={currentSectionIndex === 0 || isSaving || isSubmitting}
                    onClick={() => setCurrentSectionIndex((current) => Math.max(current - 1, 0))}
                    type="button"
                  >
                    Previous section
                  </SecondaryButton>
                  <SecondaryButton
                    disabled={currentSectionIndex === sections.length - 1 || isSaving || isSubmitting}
                    onClick={() =>
                      setCurrentSectionIndex((current) => Math.min(current + 1, sections.length - 1))
                    }
                    type="button"
                  >
                    Next section
                  </SecondaryButton>
                </div>

                <div className="button-row">
                  <PrimaryButton disabled={isLoading || isSaving || isSubmitting} onClick={handleSave} type="button">
                    {isSaving ? "Saving..." : "Save draft"}
                  </PrimaryButton>
                  <PrimaryButton disabled={isLoading || isSaving || isSubmitting} type="submit">
                    {isSubmitting ? "Submitting..." : "Submit assessment"}
                  </PrimaryButton>
                </div>
              </div>
            </form>
          ) : null}
        </DashboardCard>
      </div>

      <DashboardCard title="Saved assessment state" description="The latest V2 assessment returned by the backend is shown here for verification.">
        {savedAssessment ? (
          <dl className="summary-list">
            <div>
              <dt>Status</dt>
              <dd>{savedAssessment.status}</dd>
            </div>
            <div>
              <dt>Question bank version</dt>
              <dd>{savedAssessment.questionBankVersion}</dd>
            </div>
            <div>
              <dt>Completeness hint</dt>
              <dd>{savedAssessment.completenessHint ?? "Not available yet"}</dd>
            </div>
            <div>
              <dt>Answers saved</dt>
              <dd>{savedAssessment.answers.length}</dd>
            </div>
            <div>
              <dt>Started at</dt>
              <dd>{savedAssessment.startedAt}</dd>
            </div>
            <div>
              <dt>Submitted at</dt>
              <dd>{savedAssessment.submittedAt ?? "Not submitted yet"}</dd>
            </div>
          </dl>
        ) : (
          <p className="muted-copy">
            No V2 assessment has been saved yet. Answer a few questions and save your draft to begin.
          </p>
        )}
      </DashboardCard>
    </div>
  );
}
