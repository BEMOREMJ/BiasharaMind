import type { ChangeEvent, InputHTMLAttributes, TextareaHTMLAttributes } from "react";

type InputOption = {
  label: string;
  value: string;
};

type BaseInputFieldProps = {
  control?: "input" | "select" | "textarea";
  hint?: string;
  id: string;
  label: string;
  onChange?: (
    event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>,
  ) => void;
  options?: readonly InputOption[];
  value?: string | number;
};

type InputControlProps = Omit<InputHTMLAttributes<HTMLInputElement>, "onChange" | "value"> &
  Omit<TextareaHTMLAttributes<HTMLTextAreaElement>, "onChange" | "value">;

export function InputField({
  control = "input",
  hint,
  id,
  label,
  onChange,
  options,
  value,
  ...props
}: BaseInputFieldProps & InputControlProps) {
  const commonProps = {
    className: "input-field__control",
    id,
    onChange,
    value,
  };

  return (
    <label className="input-field" htmlFor={id}>
      <span className="input-field__label">{label}</span>
      {control === "textarea" ? (
        <textarea {...commonProps} {...props} />
      ) : null}
      {control === "select" ? (
        <select {...commonProps} {...props}>
          {options?.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      ) : null}
      {control === "input" ? <input {...commonProps} {...props} /> : null}
      {hint ? <span className="input-field__hint">{hint}</span> : null}
    </label>
  );
}
