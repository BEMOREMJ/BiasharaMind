type BrandLogoProps = {
  mode?: "lockup" | "icon" | "text";
};

export function BrandLogo({ mode = "lockup" }: BrandLogoProps) {
  if (mode === "text") {
    return <span className="brand-logo__name">BiasharaMind</span>;
  }

  return (
    <span className="brand-logo">
      <span aria-hidden="true" className="brand-logo__icon">
        B
      </span>
      {mode === "lockup" ? (
        <span className="brand-logo__lockup">
          <span className="brand-logo__name">BiasharaMind</span>
          <span className="brand-logo__tag">Growth clarity for SMEs</span>
        </span>
      ) : null}
    </span>
  );
}
