import json
from pathlib import Path

import pytest

# The conftest.py file adds `app/` to sys.path, allowing this import.
from app.core.report_generator import generate_report


@pytest.fixture
def case_dir(tmp_path: Path) -> Path:
    """
    Create a temporary case directory structure:

    case_dir/
        info.json          <-- contains case metadata
        users/             <-- directory for tool results
    """
    # Create the case directory (tmp_path is already a temporary directory)
    case_path = tmp_path

    # Write a minimal info.json that the report generator expects.
    info = {
        "case_id": "CASE-1234",
        "target": "example_user",
        "type": "username",
        "status": "open",
        "created": "2024-01-01T00:00:00Z",
    }
    (case_path / "info.json").write_text(json.dumps(info, ensure_ascii=False, indent=2))

    # Create the users directory where tool outputs (e.g., sherlock.txt) are stored.
    (case_path / "users").mkdir(parents=True, exist_ok=True)

    return case_path


def test_generate_report_with_sherlock_output(case_dir: Path):
    """
    When a `users/sherlock.txt` file exists, the generated report must:
    - contain a `reports/summary.json` with the correct case_id,
    - contain a `reports/report.md`,
    - embed the content of `sherlock.txt` inside `report.md`,
    - embed the case_id inside `report.md`.
    """
    sherlock_content = "Sherlock found 2 accounts for example_user."
    sherlock_file = case_dir / "users" / "sherlock.txt"
    sherlock_file.write_text(sherlock_content, encoding="utf-8")

    # Run the report generator.
    generate_report(case_dir)

    # Verify that the summary JSON exists and contains the correct case_id.
    summary_path = case_dir / "reports" / "summary.json"
    assert summary_path.is_file(), "summary.json was not created"
    summary_data = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary_data.get("case_id") == "CASE-1234"

    # Verify that the markdown report exists.
    report_md_path = case_dir / "reports" / "report.md"
    assert report_md_path.is_file(), "report.md was not created"
    report_md_content = report_md_path.read_text(encoding="utf-8")

    # The markdown must contain the sherlock output and the case_id.
    assert sherlock_content in report_md_content
    assert "CASE-1234" in report_md_content


def test_generate_report_without_sherlock_output(case_dir: Path):
    """
    When no `users/sherlock.txt` file is present, the generated markdown
    report must contain a default message indicating the lack of results.
    """
    # Ensure there is no sherlock.txt file.
    sherlock_file = case_dir / "users" / "sherlock.txt"
    if sherlock_file.is_file():
        sherlock_file.unlink()

    # Run the report generator.
    generate_report(case_dir)

    report_md_path = case_dir / "reports" / "report.md"
    assert report_md_path.is_file(), "report.md was not created"
    report_md_content = report_md_path.read_text(encoding="utf-8")

    # Expected default message (Spanish, as requested).
    expected_message = "No hay resultados de Sherlock para este caso"
    assert expected_message in report_md_content
