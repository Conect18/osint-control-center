import sys
from pathlib import Path

# Add the `app/` directory to the Python path so that imports like
# `from core.report_generator import generate_report` work in the test suite.
APP_ROOT = Path(__file__).resolve().parents[1] / "app"
sys.path.insert(0, str(APP_ROOT))
