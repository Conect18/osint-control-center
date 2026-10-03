from pathlib import Path
import json


LAB_PATH = Path(__file__).resolve().parent.parent.parent
ACTIVE_CASE_FILE = LAB_PATH / "active_case.json"

CURRENT_CASE = None


def set_case(case_path: Path):
    global CURRENT_CASE

    CURRENT_CASE = Path(case_path)

    data = {
        "active_case": str(CURRENT_CASE)
    }

    with open(ACTIVE_CASE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def get_case():
    global CURRENT_CASE

    if CURRENT_CASE is not None:
        return CURRENT_CASE

    if not ACTIVE_CASE_FILE.exists():
        return None

    try:

        with open(ACTIVE_CASE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        case_path = data.get("active_case")

        if not case_path:
            return None

        path = Path(case_path)

        if not path.exists():
            return None

        CURRENT_CASE = path

        return CURRENT_CASE

    except (json.JSONDecodeError, OSError):

        return None


def has_case():
    return get_case() is not None


def close_case():
    global CURRENT_CASE

    CURRENT_CASE = None

    if ACTIVE_CASE_FILE.exists():
        try:
            ACTIVE_CASE_FILE.unlink()
        except OSError:
            pass
