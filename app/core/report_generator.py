from pathlib import Path
from datetime import datetime
import json


def generate_report(case_path: Path):

    info_file = case_path / "info.json"

    if not info_file.exists():
        return

    with open(info_file, "r", encoding="utf8") as f:
        info = json.load(f)

    report_dir = case_path / "reports"
    report_dir.mkdir(exist_ok=True)

    summary = {
        "case_id": info["case_id"],
        "target": info["target"],
        "type": info["type"],
        "status": info["status"],
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(report_dir / "summary.json", "w", encoding="utf8") as f:
        json.dump(summary, f, indent=4)

    report = f"""# OSINT REPORT

Case ID: {info['case_id']}

Target: {info['target']}

Type: {info['type']}

Status: {info['status']}

Created:
{info['created']}

Generated:
{summary['generated']}

## Evidence

users/

emails/

domains/

logs/

metadata/

evidence/

## End of report
"""

    with open(report_dir / "report.md", "w", encoding="utf8") as f:
        f.write(report)
