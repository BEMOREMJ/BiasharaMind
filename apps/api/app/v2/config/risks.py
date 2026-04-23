from app.v2.config.models import CriticalRiskTaxonomyEntry


CRITICAL_RISK_TAXONOMY: list[CriticalRiskTaxonomyEntry] = [
    CriticalRiskTaxonomyEntry(
        code="CRITICAL_CASH_VISIBILITY",
        label="Cash position is not visible enough to manage near-term risk",
        description="The business may not be able to anticipate cash pressure early enough to respond well.",
        severity="critical",
        issue_codes=["FINANCE_VISIBILITY_GAP"],
        action_family_codes=["FINANCIAL_CONTROL"],
    ),
    CriticalRiskTaxonomyEntry(
        code="CRITICAL_OWNER_DEPENDENCY",
        label="Business execution depends too heavily on one person",
        description="Operational continuity is exposed because key knowledge and approvals sit with one person.",
        severity="critical",
        issue_codes=["OPS_PROCESS_GAP", "OPS_OWNER_BLINDSPOT", "TEAM_HANDOFF_BREAKDOWN"],
        action_family_codes=["PROCESS_STANDARDIZATION", "ACCOUNTABILITY_RHYTHMS"],
    ),
    CriticalRiskTaxonomyEntry(
        code="CRITICAL_REVENUE_CONCENTRATION",
        label="Growth depends on a narrow and fragile revenue engine",
        description="Revenue generation is exposed because acquisition or repeat business lacks resilience.",
        severity="critical",
        issue_codes=["SALES_PIPELINE_WEAKNESS", "CUSTOMER_RETENTION_GAP", "GROWTH_BLOCKER_UNRESOLVED"],
        action_family_codes=["PIPELINE_DISCIPLINE", "CUSTOMER_LOOP", "CONSTRAINT_REMOVAL"],
    ),
]
