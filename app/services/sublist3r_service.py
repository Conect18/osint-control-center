from pathlib import Path

from app.core.normalize import normalize_domain
from app.core.runner import Status, run_tool


def _count(path):
    if not path.is_file():
        return 0
    seen = set()
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        value = line.strip().lower()
        if value and " " not in value and "." in value:
            seen.add(value)
    return len(seen)


def run(domain, output_dir, case):
    domain = normalize_domain(domain)
    out = Path(output_dir)
    folder = out / "sublist3r"
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / "subdomains.txt"

    result = run_tool(
        "Sublist3r",
        ["sublist3r", "-d", domain, "-o", str(target), "-t", "20"],
        out, case, timeout=900, success_codes=(0, 1),
    )
    if not result.ok:
        return result

    result.findings = _count(target)
    if result.findings:
        result.message = f"Sublist3r: {result.findings} subdominios"
    else:
        result.status = Status.EMPTY
        result.message = "Sublist3r: sin subdominios"
    return result
