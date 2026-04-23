from app.v2.config.models import ScaleDefinition, ScaleOption


SCALE_LIBRARY: list[ScaleDefinition] = [
    ScaleDefinition(
        key="maturity_4",
        label="4-point maturity scale",
        response_type="single_select",
        options=[
            ScaleOption(value="not_in_place", label="Not in place", numeric_value=25, evidence_hint="No routine or proof exists"),
            ScaleOption(value="ad_hoc", label="Ad hoc", numeric_value=45, evidence_hint="Done inconsistently or by memory"),
            ScaleOption(value="partly_defined", label="Partly defined", numeric_value=65, evidence_hint="Some process exists but is uneven"),
            ScaleOption(value="well_managed", label="Well managed", numeric_value=85, evidence_hint="Repeatable, owned, and visible"),
        ],
    ),
    ScaleDefinition(
        key="confidence_5",
        label="5-point confidence scale",
        response_type="single_select",
        options=[
            ScaleOption(value="very_low", label="Very low", numeric_value=20),
            ScaleOption(value="low", label="Low", numeric_value=35),
            ScaleOption(value="mixed", label="Mixed", numeric_value=50),
            ScaleOption(value="good", label="Good", numeric_value=70),
            ScaleOption(value="very_good", label="Very good", numeric_value=85),
        ],
    ),
    ScaleDefinition(
        key="frequency_4",
        label="4-point frequency scale",
        response_type="single_select",
        options=[
            ScaleOption(value="rarely", label="Rarely", numeric_value=25),
            ScaleOption(value="sometimes", label="Sometimes", numeric_value=50),
            ScaleOption(value="weekly", label="Weekly", numeric_value=72),
            ScaleOption(value="consistently", label="Consistently", numeric_value=85),
        ],
    ),
    ScaleDefinition(
        key="urgency_4",
        label="4-point urgency scale",
        response_type="single_select",
        options=[
            ScaleOption(value="low", label="Low", numeric_value=85),
            ScaleOption(value="moderate", label="Moderate", numeric_value=65),
            ScaleOption(value="high", label="High", numeric_value=40),
            ScaleOption(value="critical", label="Critical", numeric_value=20),
        ],
    ),
    ScaleDefinition(
        key="numeric_0_10",
        label="0 to 10 numeric scale",
        response_type="numeric",
        min_value=0,
        max_value=10,
        step=1,
    ),
    ScaleDefinition(
        key="free_text",
        label="Free text response",
        response_type="free_text",
    ),
]
