from app.v2.config.models import CriticalRiskTaxonomyEntry


CRITICAL_RISK_TAXONOMY: list[CriticalRiskTaxonomyEntry] = [
    CriticalRiskTaxonomyEntry(
        code="CRITICAL_CASH_PRESSURE",
        label="Cash pressure is acute enough to threaten normal operations",
        description="The business may not have enough early warning or control to manage short-term cash strain safely.",
        severity="critical",
        issue_codes=["REACTIVE_CASH_MANAGEMENT", "FINANCE_VISIBILITY_GAP"],
        action_family_codes=["FINANCIAL_CONTROL"],
    ),
    CriticalRiskTaxonomyEntry(
        code="CRITICAL_OWNER_DEPENDENCY",
        label="Business execution depends too heavily on one person",
        description="Operational continuity is exposed because critical knowledge and approvals sit with one person.",
        severity="critical",
        issue_codes=["TEAM_CONTINUITY_RISK", "DELIVERY_UNRELIABILITY"],
        action_family_codes=["PROCESS_STANDARDIZATION", "ACCOUNTABILITY_RHYTHMS"],
    ),
    CriticalRiskTaxonomyEntry(
        code="CRITICAL_COMPLIANCE_EXPOSURE",
        label="Compliance exposure could materially affect the business",
        description="A missed compliance step could create immediate operational or financial harm.",
        severity="critical",
        issue_codes=["MANAGEMENT_VISIBILITY_GAP", "FINANCE_VISIBILITY_GAP"],
        action_family_codes=["ACCOUNTABILITY_RHYTHMS", "FINANCIAL_CONTROL"],
    ),
    CriticalRiskTaxonomyEntry(
        code="CRITICAL_COLLECTIONS_STRAIN",
        label="Collections weakness is creating near-term cash strain",
        description="Receivables follow-up is weak enough to create material cash uncertainty.",
        severity="critical",
        issue_codes=["OVERDUE_RECEIVABLES_TRAP", "FINANCE_VISIBILITY_GAP"],
        action_family_codes=["FINANCIAL_CONTROL", "METRIC_VISIBILITY"],
    ),
]
