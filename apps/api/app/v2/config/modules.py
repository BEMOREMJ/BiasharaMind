from app.v2.config.models import AdaptiveModuleDefinition, QuestionDefinition


ADAPTIVE_MODULE_REGISTRY: list[AdaptiveModuleDefinition] = [
    AdaptiveModuleDefinition(
        key="retail_inventory_control",
        label="Retail inventory control",
        description="Adaptive questions for stock visibility, shrinkage, and replenishment discipline.",
        trigger_type="industry",
        trigger_values=["retail"],
        questions=[
            QuestionDefinition(
                key="inventory_accuracy_confidence",
                prompt="How confident are you that stock counts match reality?",
                input_type="select",
                scale_key="confidence_5",
                tags=["inventory"],
            ),
            QuestionDefinition(
                key="inventory_restock_breakdowns",
                prompt="What usually causes stockouts or overstock situations?",
                input_type="textarea",
                scale_key="free_text",
                interpretation_enabled=True,
                tags=["inventory", "root_cause"],
            ),
        ],
    ),
    AdaptiveModuleDefinition(
        key="service_delivery_capacity",
        label="Service delivery capacity",
        description="Adaptive questions for service firms balancing delivery quality and utilization.",
        trigger_type="business_model",
        trigger_values=["service_led"],
        questions=[
            QuestionDefinition(
                key="delivery_capacity_planning",
                prompt="How well do you plan capacity before taking on more work?",
                input_type="select",
                scale_key="maturity_4",
                tags=["capacity"],
            ),
            QuestionDefinition(
                key="delivery_rework_notes",
                prompt="What most often causes rework or delivery delays?",
                input_type="textarea",
                scale_key="free_text",
                interpretation_enabled=True,
                tags=["delivery", "root_cause"],
            ),
        ],
    ),
    AdaptiveModuleDefinition(
        key="b2b_revenue_collection",
        label="B2B revenue collection",
        description="Adaptive questions for invoicing discipline and delayed collections in B2B models.",
        trigger_type="customer_model",
        trigger_values=["b2b", "mixed"],
        questions=[
            QuestionDefinition(
                key="collections_visibility",
                prompt="How clearly can you track unpaid invoices and follow-up status?",
                input_type="select",
                scale_key="maturity_4",
                tags=["collections"],
            ),
            QuestionDefinition(
                key="collections_delay_notes",
                prompt="What usually delays payment collection?",
                input_type="textarea",
                scale_key="free_text",
                interpretation_enabled=True,
                tags=["collections", "root_cause"],
            ),
        ],
    ),
    AdaptiveModuleDefinition(
        key="manual_workload_pressure",
        label="Manual workload pressure",
        description="Adaptive questions for businesses still operating with manual or fragmented tooling.",
        trigger_type="tooling",
        trigger_values=["mostly_manual", "basic_tools"],
        questions=[
            QuestionDefinition(
                key="manual_reporting_time_loss",
                prompt="How often does manual reporting or reconciliation delay decisions?",
                input_type="select",
                scale_key="frequency_4",
                tags=["manual_work"],
            ),
            QuestionDefinition(
                key="manual_work_error_notes",
                prompt="Where do manual processes create avoidable errors or duplicate work?",
                input_type="textarea",
                scale_key="free_text",
                interpretation_enabled=True,
                tags=["manual_work", "risk"],
            ),
        ],
    ),
]
