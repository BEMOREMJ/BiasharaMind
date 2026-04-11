"use client";

import {
  AssessmentCreateSchema,
  AssessmentSubmitSchema,
  AssessmentUpdateSchema,
  type Assessment,
  type AssessmentAnswer,
  type AssessmentQuestion,
} from "@biasharamind/shared";
import { useEffect, useMemo, useState, type FormEvent } from "react";

import { Badge } from "@/components/badge";
import { DashboardCard } from "@/components/dashboard-card";
import { InputField } from "@/components/input-field";
import { PrimaryButton } from "@/components/primary-button";
import { SecondaryButton } from "@/components/secondary-button";
import { SectionHeader } from "@/components/section-header";
import {
  createAssessment,
  getAssessment,
  submitAssessment,
  updateAssessment,
} from "@/lib/api/assessment";
import {
  assessmentQuestions,
  assessmentSections,
  getQuestionsForSection,
} from "@/lib/assessment-definition";

type AnswerMap = Record<string, string>;

const ASSESSMENT_VERSION = "assessment_v1";

function serializeAnswers(answers: AnswerMap): AssessmentAnswer[] {
  return assessmentQuestions.reduce<AssessmentAnswer[]>((accumulator, question) => {
    const rawValue = answers[question.key];

    if (rawValue === undefined || rawValue === "") {
      return accumulator;
    }

    accumulator.push({
      answerType: question.answerType,
      questionKey: question.key,
      sectionKey: question.sectionKey,
      value: question.answerType === "number" ? Number(rawValue) : rawValue,
    });

    return accumulator;
  }, []);
}

function toAnswerMap(assessment: Assessment | null): AnswerMap {
  if (!assessment) {
    return {};
  }

  return Object.fromEntries(
    assessment.answers.map((answer) => [answer.questionKey, String(answer.value)]),
  );
}

function countAnsweredQuestions(answerMap: AnswerMap) {
  return assessmentQuestions.filter((question) => {
    const value = answerMap[question.key];
    return value !== undefined && value !== "";
  }).length;
}

function countCompletedSections(answerMap: AnswerMap) {
  return assessmentSections.filter((section) =>
    getQuestionsForSection(section.key).every((question) => {
      const value = answerMap[question.key];
      return !question.required || (value !== undefined && value !== "");
    }),
  ).length;
}

function getMissingRequiredQuestions(answerMap: AnswerMap) {
  return assessmentQuestions.filter((question) => {
    if (!question.required) {
      return false;
    }

    const value = answerMap[question.key];
    return value === undefined || value === "";
  });
}

function buildCreatePayload(answerMap: AnswerMap) {
  return AssessmentCreateSchema.parse({
    version: ASSESSMENT_VERSION,
    sections: assessmentSections,
    answers: serializeAnswers(answerMap),
  });
}

function buildUpdatePayload(answerMap: AnswerMap) {
  return AssessmentUpdateSchema.parse({
    status: "in_progress",
    sections: assessmentSections,
    answers: serializeAnswers(answerMap),
  });
}

function buildSubmitPayload(answerMap: AnswerMap) {
  return AssessmentSubmitSchema.parse({
    answers: serializeAnswers(answerMap),
  });
}

function questionControlType(question: AssessmentQuestion) {
  if (question.answerType === "textarea") {
    return "textarea";
  }

  if (question.answerType === "select") {
    return "select";
  }

  return "input";
}

export function AssessmentFlow() {
  const [answerMap, setAnswerMap] = useState<AnswerMap>({});
  const [savedAssessment, setSavedAssessment] = useState<Assessment | null>(null);
  const [currentSectionIndex, setCurrentSectionIndex] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const currentSection = assessmentSections[currentSectionIndex];
  const currentQuestions = useMemo(
    () => getQuestionsForSection(currentSection.key),
    [currentSection.key],
  );
  const answeredCount = countAnsweredQuestions(answerMap);
  const completedSections = countCompletedSections(answerMap);
  const missingRequiredQuestions = getMissingRequiredQuestions(answerMap);
  const isSubmitted = savedAssessment?.status === "submitted";

  useEffect(() => {
    let active = true;

    async function loadAssessment() {
      try {
        const assessment = await getAssessment();

        if (!active) {
          return;
        }

        if (assessment) {
          setSavedAssessment(assessment);
          setAnswerMap(toAnswerMap(assessment));
          setStatusMessage("Your current assessment has been loaded.");
        } else {
          setStatusMessage(
            "No saved assessment yet. Start with the first section and save your progress as you go.",
          );
        }
      } catch (error) {
        if (!active) {
          return;
        }

        setErrorMessage(error instanceof Error ? error.message : "Failed to load the assessment.");
      } finally {
        if (active) {
          setIsLoading(false);
        }
      }
    }

    void loadAssessment();

    return () => {
      active = false;
    };
  }, []);

  function handleAnswerChange(questionKey: string, value: string) {
    setAnswerMap((current) => ({
      ...current,
      [questionKey]: value,
    }));
  }

  async function handleSaveProgress() {
    setIsSaving(true);
    setErrorMessage(null);
    setStatusMessage(null);

    try {
      const assessment = savedAssessment
        ? await updateAssessment(buildUpdatePayload(answerMap))
        : await createAssessment(buildCreatePayload(answerMap));

      setSavedAssessment(assessment);
      setStatusMessage("Assessment progress saved.");
    } catch (error) {
      setErrorMessage(
        error instanceof Error ? error.message : "Unable to save assessment progress.",
      );
    } finally {
      setIsSaving(false);
    }
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (missingRequiredQuestions.length > 0) {
      setErrorMessage("Complete all required questions before submitting the assessment.");
      setStatusMessage(null);
      return;
    }

    if (!savedAssessment) {
      setErrorMessage("Save your progress at least once before submitting.");
      setStatusMessage(null);
      return;
    }

    setIsSubmitting(true);
    setErrorMessage(null);
    setStatusMessage(null);

    try {
      const assessment = await submitAssessment(buildSubmitPayload(answerMap));
      setSavedAssessment(assessment);
      setStatusMessage("Assessment submitted successfully.");
    } catch (error) {
      setErrorMessage(
        error instanceof Error ? error.message : "Unable to submit the assessment.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  function handleResetSection() {
    setAnswerMap((current) => {
      const next = { ...current };
      for (const question of currentQuestions) {
        delete next[question.key];
      }
      return next;
    });
    setStatusMessage(`Cleared answers for ${currentSection.title}.`);
    setErrorMessage(null);
  }

  return (
    <div className="dashboard-stack">
      <DashboardCard tone="hero" title="Business assessment">
        <div className="dashboard-stack">
          <Badge tone={isSubmitted ? "success" : "default"}>
            {isSubmitted ? "Assessment submitted" : "Assessment in progress"}
          </Badge>
          <SectionHeader
            title="Business assessment"
            eyebrow="Guided review"
            description="Answer a set of practical questions about how your business operates today. BiasharaMind uses your responses to identify strengths, risks, and the areas that need the most attention."
          />
          <div className="stats-row">
            <div className="stat-chip">
              <strong>{completedSections}</strong>
              <span>Sections completed</span>
            </div>
            <div className="stat-chip">
              <strong>{answeredCount}</strong>
              <span>Answers captured</span>
            </div>
            <div className="stat-chip">
              <strong>{assessmentSections.length}</strong>
              <span>Total sections</span>
            </div>
          </div>
        </div>
      </DashboardCard>

      <div className="dashboard-grid dashboard-grid--assessment">
        <DashboardCard title="Section progress" description="Move through the assessment one section at a time.">
          <div className="assessment-progress">
            {assessmentSections.map((section, index) => {
              const sectionQuestions = getQuestionsForSection(section.key);
              const complete = sectionQuestions.every((question) => {
                const value = answerMap[question.key];
                return !question.required || (value !== undefined && value !== "");
              });

              return (
                <button
                  className={`assessment-progress__item ${
                    index === currentSectionIndex ? "assessment-progress__item--active" : ""
                  }`}
                  key={section.key}
                  onClick={() => setCurrentSectionIndex(index)}
                  type="button"
                >
                  <span className="assessment-progress__step">{index + 1}</span>
                  <span>
                    <strong>{section.title}</strong>
                    <small>{complete ? "Completed" : "In progress"}</small>
                  </span>
                </button>
              );
            })}
          </div>
        </DashboardCard>

        <DashboardCard
          title={currentSection.title}
          description={currentSection.description}
        >
          {isLoading ? <p className="muted-copy">Loading assessment...</p> : null}
          {!isLoading ? (
            <form className="form-grid" onSubmit={handleSubmit}>
              {currentQuestions.map((question) => (
                <div className="form-grid__full" key={question.key}>
                  <InputField
                    control={questionControlType(question)}
                    hint={question.helpText}
                    id={question.key}
                    label={question.prompt}
                    onChange={(event) => handleAnswerChange(question.key, event.target.value)}
                    options={
                      question.answerType === "select"
                        ? [
                            { label: "Select an option", value: "" },
                            ...(question.options ?? []),
                          ]
                        : undefined
                    }
                    placeholder={
                      question.answerType === "number"
                        ? "Enter a number"
                        : "Enter your answer"
                    }
                    rows={question.answerType === "textarea" ? 4 : undefined}
                    type={question.answerType === "number" ? "number" : undefined}
                    value={answerMap[question.key] ?? ""}
                  />
                </div>
              ))}

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
                    disabled={
                      currentSectionIndex === assessmentSections.length - 1 ||
                      isSaving ||
                      isSubmitting
                    }
                    onClick={() =>
                      setCurrentSectionIndex((current) =>
                        Math.min(current + 1, assessmentSections.length - 1),
                      )
                    }
                    type="button"
                  >
                    Next section
                  </SecondaryButton>
                </div>

                <div className="button-row">
                  <SecondaryButton
                    disabled={isLoading || isSaving || isSubmitting || isSubmitted}
                    onClick={handleResetSection}
                    type="button"
                  >
                    Clear section
                  </SecondaryButton>
                  <PrimaryButton
                    disabled={isLoading || isSaving || isSubmitting || isSubmitted}
                    onClick={handleSaveProgress}
                    type="button"
                  >
                    {isSaving ? "Saving..." : "Save progress"}
                  </PrimaryButton>
                  <PrimaryButton disabled={isLoading || isSaving || isSubmitting || isSubmitted}>
                    {isSubmitting ? "Submitting..." : "Submit assessment"}
                  </PrimaryButton>
                </div>
              </div>
            </form>
          ) : null}
        </DashboardCard>
      </div>

      <DashboardCard
        title="Saved assessment state"
        description="The latest assessment returned by the backend is shown here so the current persisted state is visible."
      >
        {savedAssessment ? (
          <dl className="summary-list">
            <div>
              <dt>Status</dt>
              <dd>{savedAssessment.status}</dd>
            </div>
            <div>
              <dt>Version</dt>
              <dd>{savedAssessment.version}</dd>
            </div>
            <div>
              <dt>Sections</dt>
              <dd>{savedAssessment.sections.length}</dd>
            </div>
            <div>
              <dt>Answers saved</dt>
              <dd>{savedAssessment.answers.length}</dd>
            </div>
            <div>
              <dt>Started on</dt>
              <dd>{savedAssessment.startedAt}</dd>
            </div>
            <div>
              <dt>Submitted on</dt>
              <dd>{savedAssessment.submittedAt ?? "Not submitted yet"}</dd>
            </div>
          </dl>
        ) : (
          <p className="muted-copy">
            You have not saved an assessment yet. Complete a section and save your progress to begin building your business review.
          </p>
        )}
      </DashboardCard>
    </div>
  );
}
