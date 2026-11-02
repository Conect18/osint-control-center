import contextlib
import json
import os
from pathlib import Path

from app.config.settings import ACTIVE_CASE_FILE

CURRENT_CASE = None


def set_case(case_path: Path):
    global CURRENT_CASE
    CURRENT_CASE = Path(case_path).resolve()

    tmp = ACTIVE_CASE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps({"active_case": str(CURRENT_CASE)}, indent=2), encoding="utf-8")
    os.replace(tmp, ACTIVE_CASE_FILE)


def get_case():
    global CURRENT_CASE
    if CURRENT_CASE is not None and CURRENT_CASE.exists():
        return CURRENT_CASE
    CURRENT_CASE = None

    try:
        data = json.loads(ACTIVE_CASE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

    path = Path(data.get("active_case") or "")
    if not path.is_dir():
        return None

    CURRENT_CASE = path
    return CURRENT_CASE


def has_case():
    return get_case() is not None


def close_case():
    global CURRENT_CASE
    CURRENT_CASE = None
    with contextlib.suppress(OSError):
        ACTIVE_CASE_FILE.unlink()
