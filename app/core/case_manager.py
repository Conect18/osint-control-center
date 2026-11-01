import json
from datetime import datetime
from pathlib import Path

from app.config.settings import ensure_dirs
from app.core.active_case import set_case
from app.core.normalize import normalize_target, slugify
from app.config import settings

CATEGORIES = ("users", "emails", "domains", "hosts")
CASE_FOLDERS = ("logs", "reports", "metadata", "evidence", *CATEGORIES)


def _next_id(today):
    prefix = f"CASE-{today}-"
    highest = 0
    for path in settings.CASES_PATH.glob(f"{prefix}*"):
        tail = path.name[len(prefix):]
        if tail.isdigit():
            highest = max(highest, int(tail))
    return f"{prefix}{highest + 1:04d}"


def create_case(target: str, case_type: str = "users") -> Path:
    """Crea un caso con ID correlativo seguro y objetivo normalizado."""
    ensure_dirs()

    value = normalize_target(case_type, target)
    today = datetime.now().strftime("%Y%m%d")

    while True:
        case_id = _next_id(today)
        case_path = settings.CASES_PATH / case_id
        try:
            case_path.mkdir()
            break
        except FileExistsError:
            continue

    for folder in CASE_FOLDERS:
        (case_path / folder).mkdir()

    info = {
        "case_id": case_id,
        "target": value,
        "slug": slugify(value),
        "type": case_type,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "OPEN",
    }
    (case_path / "info.json").write_text(
        json.dumps(info, indent=4, ensure_ascii=False), encoding="utf-8"
    )

    set_case(case_path)
    return case_path
