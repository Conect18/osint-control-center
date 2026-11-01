import re
from pathlib import Path

from app.core.normalize import normalize_user
from app.core.runner import Status, run_tool

FOUND = re.compile(r"^\s*\[\+\]", re.MULTILINE)
TOTAL = re.compile(r"Search completed with (\d+) results")


def _count(folder):
    path = folder / "stdout.txt"
    if not path.is_file():
        return 0
    text = path.read_text(encoding="utf-8", errors="replace")
    found = len(FOUND.findall(text))
    if found:
        return found
    match = TOTAL.search(text)
    return int(match.group(1)) if match else 0


def run(username, output_dir, case):
    username = normalize_user(username)
    out = Path(output_dir)
    folder = out / "sherlock"

    result = run_tool(
        "Sherlock",
        ["sherlock", username, "--output", str(folder),
         "--print-found", "--timeout", "10", "--no-color"],
        out, case, timeout=900,
    )
    if not result.ok:
        return result

    result.findings = _count(folder)
    if result.findings:
        result.message = f"Sherlock: {result.findings} perfiles"
    else:
        result.status = Status.EMPTY
        result.message = "Sherlock: sin perfiles"
    return result
