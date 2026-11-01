from pathlib import Path

from app.core.normalize import normalize_email
from app.core.runner import Status, run_tool


def run(email, output_dir, case):
    email = normalize_email(email)
    out = Path(output_dir)

    result = run_tool(
        "Holehe",
        ["holehe", email, "--only-used", "--no-color"],
        out, case, timeout=1200, success_codes=(0, 1),
    )
    if not result.ok:
        return result

    text = (out / "holehe" / "stdout.txt").read_text(encoding="utf-8", errors="replace")
    result.findings = sum(1 for line in text.splitlines() if line.strip().startswith("[+]"))

    if result.findings:
        result.message = f"Holehe: {result.findings} registros"
    else:
        result.status = Status.EMPTY
        result.message = "Holehe: sin registros"
    return result
