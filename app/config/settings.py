from pathlib import Path

# Directorio de la aplicación
APP_PATH = Path(__file__).resolve().parent.parent

# Directorio del laboratorio
LAB_PATH = APP_PATH.parent

RESULTS_PATH = LAB_PATH / "results"
REPORTS_PATH = LAB_PATH / "reports"
TOOLS_PATH = LAB_PATH / "tools"
TARGETS_PATH = LAB_PATH / "targets"
PROJECTS_PATH = LAB_PATH / "projects"
LOGS_PATH = LAB_PATH / "logs"
DOCS_PATH = LAB_PATH / "docs"
WORDLISTS_PATH = LAB_PATH / "wordlists"
