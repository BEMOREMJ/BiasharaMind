from app.v2.config.models import IssueTaxonomyEntry


ISSUE_TAXONOMY: list[IssueTaxonomyEntry] = [
    IssueTaxonomyEntry(
        code="OPS_PROCESS_GAP",
        label="Core operations are not consistently defined",
        description="Execution depends on memory or individual heroics instead of repeatable process.",
        section_key="operations",
        severity="high",
        action_family_codes=["PROCESS_STANDARDIZATION", "ACCOUNTABILITY_RHYTHMS"],
    ),
    IssueTaxonomyEntry(
        code="OPS_OWNER_BLINDSPOT",
        label="Ownership is unclear in day-to-day operations",
        description="Recurring work lacks named owners, causing dropped tasks and confusion.",
        section_key="operations",
        severity="medium",
        action_family_codes=["ACCOUNTABILITY_RHYTHMS"],
    ),
    IssueTaxonomyEntry(
        code="SALES_PIPELINE_WEAKNESS",
        label="Sales execution is not reliably repeatable",
        description="Lead handling and conversion rely on inconsistent effort rather than a repeatable motion.",
        section_key="sales_marketing",
        severity="high",
        action_family_codes=["PIPELINE_DISCIPLINE", "METRIC_VISIBILITY"],
    ),
    IssueTaxonomyEntry(
        code="CUSTOMER_RETENTION_GAP",
        label="Customer follow-up is too inconsistent",
        description="The business is not maintaining a steady retention or feedback rhythm.",
        section_key="customer_management",
        severity="high",
        action_family_codes=["CUSTOMER_LOOP", "METRIC_VISIBILITY"],
    ),
    IssueTaxonomyEntry(
        code="FINANCE_VISIBILITY_GAP",
        label="Financial visibility is too weak for confident decisions",
        description="Reporting and cash visibility are not strong enough for predictable decision-making.",
        section_key="finance_reporting",
        severity="high",
        action_family_codes=["FINANCIAL_CONTROL", "METRIC_VISIBILITY"],
    ),
    IssueTaxonomyEntry(
        code="TEAM_HANDOFF_BREAKDOWN",
        label="Team handoffs break down too often",
        description="Work transfers between people or roles are a recurring source of delays or mistakes.",
        section_key="team_workflows",
        severity="medium",
        action_family_codes=["ACCOUNTABILITY_RHYTHMS", "PROCESS_STANDARDIZATION"],
    ),
    IssueTaxonomyEntry(
        code="TOOL_FRAGMENTATION",
        label="Tools are too fragmented or manual",
        description="The current tool stack creates duplicate work, weak trust in data, or coordination friction.",
        section_key="digital_tools",
        severity="medium",
        action_family_codes=["TOOL_CONSOLIDATION", "DATA_DISCIPLINE"],
    ),
    IssueTaxonomyEntry(
        code="GROWTH_BLOCKER_UNRESOLVED",
        label="A major growth blocker is unresolved",
        description="A known blocker continues to limit momentum, throughput, or revenue growth.",
        section_key="growth_blockers",
        severity="high",
        action_family_codes=["CONSTRAINT_REMOVAL", "EXECUTION_FOCUS"],
    ),
]
