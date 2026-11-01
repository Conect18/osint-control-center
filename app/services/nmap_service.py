from pathlib import Path

from app.core.normalize import normalize_domain
from app.core.runner import Status, run_tool


def run(host, output_dir, case):
    host = normalize_domain(host)
    out = Path(output_dir)
    folder = out / "nmap"
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / "scan.txt"

    result = run_tool(
        "Nmap",
        ["nmap", "-sT", "-Pn", "-T4", "--top-ports", "200", "-oN", str(target), host],
        out, case, timeout=1800,
    )
    if not result.ok:
        return result

    text = target.read_text(encoding="utf-8", errors="replace") if target.is_file() else ""
    result.findings = sum(1 for line in text.splitlines() if "/tcp" in line and "open" in line)

    if result.findings:
        result.message = f"Nmap: {result.findings} puertos abiertos"
    else:
        result.status = Status.EMPTY
        result.message = "Nmap: sin puertos abiertos"
    return result
