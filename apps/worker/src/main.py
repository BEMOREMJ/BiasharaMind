from src.config import get_settings
from src.graphs.business_assessment_graph import build_business_assessment_graph


def main() -> None:
    settings = get_settings()
    build_business_assessment_graph()
    print(f"Loaded graph '{settings.graph_name}'.")


if __name__ == "__main__":
    main()
