import type {
  ChangeEvent,
  InputHTMLAttributes,
  SelectHTMLAttributes,
  TextareaHTMLAttributes,
} from "react";

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
  Omit<TextareaHTMLAttributes<HTMLTextAreaElement>, "onChange" | "value"> &
  Omit<SelectHTMLAttributes<HTMLSelectElement>, "onChange" | "value">;

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
  return (
    <label className="input-field" htmlFor={id}>
      <span className="input-field__label">{label}</span>
      {control === "textarea" ? (
        <textarea
          {...(props as TextareaHTMLAttributes<HTMLTextAreaElement>)}
          className="input-field__control"
          id={id}
          onChange={onChange}
          value={value}
        />
      ) : null}
      {control === "select" ? (
        <select
          {...(props as SelectHTMLAttributes<HTMLSelectElement>)}
          className="input-field__control"
          id={id}
          onChange={onChange}
          value={value}
        >
          {options?.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      ) : null}
      {control === "input" ? (
        <input
          {...(props as InputHTMLAttributes<HTMLInputElement>)}
          className="input-field__control"
          id={id}
          onChange={onChange}
          value={value}
        />
      ) : null}
      {hint ? <span className="input-field__hint">{hint}</span> : null}
    </label>
  );
}
