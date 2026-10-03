from pathlib import Path
from datetime import datetime
import json

from core.active_case import set_case


LAB_PATH = Path(__file__).resolve().parent.parent.parent
CASES_PATH = LAB_PATH / "cases"


def create_case(target: str, case_type: str = "username"):

    CASES_PATH.mkdir(exist_ok=True)

    today = datetime.now().strftime("%Y%m%d")

    existing = sorted(CASES_PATH.glob(f"CASE-{today}-*"))

    number = len(existing) + 1

    case_id = f"CASE-{today}-{number:04d}"

    case_path = CASES_PATH / case_id

    folders = [
        "logs",
        "reports",
        "users",
        "emails",
        "domains",
        "metadata",
        "evidence",
    ]

    case_path.mkdir()

    for folder in folders:
        (case_path / folder).mkdir()

    info = {
        "case_id": case_id,
        "target": target,
        "type": case_type,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "OPEN",
    }

    with open(case_path / "info.json", "w", encoding="utf8") as f:
        json.dump(info, f, indent=4)

    # Establecer automáticamente este caso como activo
    set_case(case_path)

    return case_path
