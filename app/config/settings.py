"""Rutas canónicas del laboratorio. Única fuente de verdad."""

import os
from pathlib import Path

APP_PATH = Path(__file__).resolve().parent.parent
LAB_PATH = Path(os.environ.get("OSINT_LAB_PATH") or APP_PATH.parent).resolve()

CASES_PATH = LAB_PATH / "cases"
ACTIVE_CASE_FILE = LAB_PATH / "active_case.json"
LOGS_PATH = LAB_PATH / "logs"
DOCS_PATH = LAB_PATH / "docs"
WORDLISTS_PATH = LAB_PATH / "wordlists"
TOOLS_PATH = LAB_PATH / "tools"
RESULTS_PATH = LAB_PATH / "results"


def ensure_dirs():
    CASES_PATH.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.mkdir(parents=True, exist_ok=True)
