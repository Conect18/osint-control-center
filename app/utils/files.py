from pathlib import Path

from config.settings import RESULTS_PATH


def create_case(username: str) -> Path:
    """
    Crea la estructura completa de un caso.
    """

    case = RESULTS_PATH / username

    (case / "sherlock").mkdir(parents=True, exist_ok=True)
    (case / "maigret").mkdir(parents=True, exist_ok=True)
    (case / "logs").mkdir(parents=True, exist_ok=True)

    return case
