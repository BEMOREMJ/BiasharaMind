from app.v2.config.models import BusinessProfileEnumOption, BusinessProfileFieldDefinition


BUSINESS_PROFILE_FIELD_REGISTRY: list[BusinessProfileFieldDefinition] = [
    BusinessProfileFieldDefinition(
        key="business_name",
        label="Business name",
        field_type="string",
        description="The primary name used to identify the business.",
    ),
    BusinessProfileFieldDefinition(
        key="primary_business_type",
        label="Primary business type",
        field_type="enum",
        description="The closest broad operating model for the business.",
        options=[
            BusinessProfileEnumOption(value="retail", label="Retail"),
            BusinessProfileEnumOption(value="food_and_hospitality", label="Food and hospitality"),
            BusinessProfileEnumOption(value="services", label="Services"),
            BusinessProfileEnumOption(value="manufacturing", label="Manufacturing"),
            BusinessProfileEnumOption(value="agriculture", label="Agriculture"),
            BusinessProfileEnumOption(value="healthcare", label="Healthcare"),
            BusinessProfileEnumOption(value="education", label="Education"),
            BusinessProfileEnumOption(value="technology", label="Technology"),
            BusinessProfileEnumOption(value="construction", label="Construction"),
            BusinessProfileEnumOption(value="logistics", label="Logistics"),
            BusinessProfileEnumOption(value="other", label="Other"),
        ],
    ),
    BusinessProfileFieldDefinition(
        key="main_offer",
        label="Main offer",
        field_type="string",
        description="The core product or service the business sells most often.",
    ),
    BusinessProfileFieldDefinition(
        key="customer_type",
        label="Customer type",
        field_type="enum",
        options=[
            BusinessProfileEnumOption(value="b2c", label="B2C"),
            BusinessProfileEnumOption(value="b2b", label="B2B"),
            BusinessProfileEnumOption(value="mixed", label="Mixed"),
        ],
    ),
    BusinessProfileFieldDefinition(
        key="sales_channels",
        label="Sales channels",
        field_type="multi_enum",
        options=[
            BusinessProfileEnumOption(value="walk_in", label="Walk-in"),
            BusinessProfileEnumOption(value="whatsapp", label="WhatsApp"),
            BusinessProfileEnumOption(value="social_media", label="Social media"),
            BusinessProfileEnumOption(value="phone", label="Phone"),
            BusinessProfileEnumOption(value="website", label="Website"),
            BusinessProfileEnumOption(value="marketplace", label="Marketplace"),
            BusinessProfileEnumOption(value="field_sales", label="Field sales"),
            BusinessProfileEnumOption(value="referrals", label="Referrals"),
        ],
    ),
    BusinessProfileFieldDefinition(
        key="fulfilment_model",
        label="Fulfilment model",
        field_type="enum",
        options=[
            BusinessProfileEnumOption(value="immediate_delivery", label="Immediate delivery"),
            BusinessProfileEnumOption(value="made_to_order", label="Made to order"),
            BusinessProfileEnumOption(value="scheduled_service", label="Scheduled service"),
            BusinessProfileEnumOption(value="delivery_or_dispatch", label="Delivery or dispatch"),
            BusinessProfileEnumOption(value="mixed", label="Mixed"),
        ],
    ),
    BusinessProfileFieldDefinition(
        key="inventory_involvement",
        label="Inventory involvement",
        field_type="enum",
        options=[
            BusinessProfileEnumOption(value="none", label="None"),
            BusinessProfileEnumOption(value="light", label="Light"),
            BusinessProfileEnumOption(value="moderate", label="Moderate"),
            BusinessProfileEnumOption(value="heavy", label="Heavy"),
        ],
    ),
    BusinessProfileFieldDefinition(
        key="credit_sales_exposure",
        label="Credit sales exposure",
        field_type="enum",
        options=[
            BusinessProfileEnumOption(value="none", label="None"),
            BusinessProfileEnumOption(value="low", label="Low"),
            BusinessProfileEnumOption(value="moderate", label="Moderate"),
            BusinessProfileEnumOption(value="high", label="High"),
        ],
    ),
    BusinessProfileFieldDefinition(
        key="business_age_stage",
        label="Business age stage",
        field_type="enum",
        options=[
            BusinessProfileEnumOption(value="starting_out", label="Starting out"),
            BusinessProfileEnumOption(value="early_growth", label="Early growth"),
            BusinessProfileEnumOption(value="established", label="Established"),
            BusinessProfileEnumOption(value="mature", label="Mature"),
        ],
    ),
    BusinessProfileFieldDefinition(
        key="team_size_band",
        label="Team size band",
        field_type="enum",
        options=[
            BusinessProfileEnumOption(value="solo", label="Solo"),
            BusinessProfileEnumOption(value="two_to_five", label="2 to 5"),
            BusinessProfileEnumOption(value="six_to_fifteen", label="6 to 15"),
            BusinessProfileEnumOption(value="sixteen_to_fifty", label="16 to 50"),
            BusinessProfileEnumOption(value="over_fifty", label="Over 50"),
        ],
    ),
    BusinessProfileFieldDefinition(
        key="number_of_locations",
        label="Number of locations",
        field_type="number",
        min_value=1,
        max_value=500,
    ),
    BusinessProfileFieldDefinition(
        key="monthly_revenue_band",
        label="Monthly revenue band",
        field_type="enum",
        options=[
            BusinessProfileEnumOption(value="pre_revenue", label="Pre-revenue"),
            BusinessProfileEnumOption(value="under_1000_usd", label="Under $1,000"),
            BusinessProfileEnumOption(value="1000_to_5000_usd", label="$1,000 to $5,000"),
            BusinessProfileEnumOption(value="5000_to_20000_usd", label="$5,000 to $20,000"),
            BusinessProfileEnumOption(value="20000_to_100000_usd", label="$20,000 to $100,000"),
            BusinessProfileEnumOption(value="over_100000_usd", label="Over $100,000"),
        ],
    ),
    BusinessProfileFieldDefinition(
        key="seasonality_level",
        label="Seasonality level",
        field_type="enum",
        required=False,
        options=[
            BusinessProfileEnumOption(value="low", label="Low"),
            BusinessProfileEnumOption(value="moderate", label="Moderate"),
            BusinessProfileEnumOption(value="high", label="High"),
        ],
    ),
    BusinessProfileFieldDefinition(
        key="peak_periods",
        label="Peak periods",
        field_type="multi_enum",
        required=False,
        options=[
            BusinessProfileEnumOption(value="month_end", label="Month end"),
            BusinessProfileEnumOption(value="payday_weeks", label="Payday weeks"),
            BusinessProfileEnumOption(value="weekends", label="Weekends"),
            BusinessProfileEnumOption(value="holiday_periods", label="Holiday periods"),
            BusinessProfileEnumOption(value="festive_season", label="Festive season"),
            BusinessProfileEnumOption(value="back_to_school", label="Back to school"),
            BusinessProfileEnumOption(value="harvest_period", label="Harvest period"),
            BusinessProfileEnumOption(value="tourist_season", label="Tourist season"),
        ],
    ),
    BusinessProfileFieldDefinition(
        key="owner_involvement_level",
        label="Owner involvement level",
        field_type="enum",
        options=[
            BusinessProfileEnumOption(value="hands_on_daily", label="Hands-on daily"),
            BusinessProfileEnumOption(value="involved_in_key_areas", label="Involved in key areas"),
            BusinessProfileEnumOption(value="mostly_delegated", label="Mostly delegated"),
        ],
    ),
    BusinessProfileFieldDefinition(
        key="primary_business_goal",
        label="Primary business goal",
        field_type="enum",
        options=[
            BusinessProfileEnumOption(value="grow_sales", label="Grow sales"),
            BusinessProfileEnumOption(value="improve_cash_flow", label="Improve cash flow"),
            BusinessProfileEnumOption(value="improve_efficiency", label="Improve efficiency"),
            BusinessProfileEnumOption(value="stabilize_operations", label="Stabilize operations"),
            BusinessProfileEnumOption(value="increase_customer_retention", label="Increase customer retention"),
            BusinessProfileEnumOption(value="prepare_to_expand", label="Prepare to expand"),
        ],
    ),
    BusinessProfileFieldDefinition(
        key="time_capacity",
        label="Time capacity",
        field_type="enum",
        options=[
            BusinessProfileEnumOption(value="very_limited", label="Very limited"),
            BusinessProfileEnumOption(value="limited", label="Limited"),
            BusinessProfileEnumOption(value="moderate", label="Moderate"),
            BusinessProfileEnumOption(value="strong", label="Strong"),
        ],
    ),
    BusinessProfileFieldDefinition(
        key="budget_flexibility",
        label="Budget flexibility",
        field_type="enum",
        options=[
            BusinessProfileEnumOption(value="none", label="None"),
            BusinessProfileEnumOption(value="tight", label="Tight"),
            BusinessProfileEnumOption(value="moderate", label="Moderate"),
            BusinessProfileEnumOption(value="flexible", label="Flexible"),
        ],
    ),
    BusinessProfileFieldDefinition(
        key="tool_hire_openness",
        label="Tool or hire openness",
        field_type="enum",
        options=[
            BusinessProfileEnumOption(value="not_open", label="Not open"),
            BusinessProfileEnumOption(value="cautiously_open", label="Cautiously open"),
            BusinessProfileEnumOption(value="open", label="Open"),
        ],
    ),
    BusinessProfileFieldDefinition(
        key="record_availability",
        label="Record availability",
        field_type="enum",
        options=[
            BusinessProfileEnumOption(value="minimal", label="Minimal"),
            BusinessProfileEnumOption(value="some_manual_records", label="Some manual records"),
            BusinessProfileEnumOption(value="organized_manual_records", label="Organized manual records"),
            BusinessProfileEnumOption(value="current_digital_records", label="Current digital records"),
        ],
    ),
    BusinessProfileFieldDefinition(
        key="compliance_sector_sensitivity",
        label="Compliance sector sensitivity",
        field_type="enum",
        required=False,
        options=[
            BusinessProfileEnumOption(value="moderate", label="Moderate"),
            BusinessProfileEnumOption(value="high", label="High"),
        ],
    ),
]

BUSINESS_PROFILE_FIELD_MAP: dict[str, BusinessProfileFieldDefinition] = {
    field.key: field for field in BUSINESS_PROFILE_FIELD_REGISTRY
}

BUSINESS_PROFILE_ENUM_VALUES: dict[str, set[str]] = {
    key: {option.value for option in field.options}
    for key, field in BUSINESS_PROFILE_FIELD_MAP.items()
    if field.options
}


def get_profile_enum_values(field_key: str) -> set[str]:
    return BUSINESS_PROFILE_ENUM_VALUES.get(field_key, set())
