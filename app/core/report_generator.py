import json
import os
import sys
from datetime import datetime
from pathlib import Path

LEGACY_FILES = (
    ("users", "sherlock.txt"),
    ("users", "maigret.txt"),
    ("emails", "holehe.txt"),
    ("domains", "sublist3r.txt"),
)


def _load_info(case_path):
    try:
        return json.loads((case_path / "info.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _save_info(case_path, info):
    try:
        (case_path / "info.json").write_text(
            json.dumps(info, indent=4, ensure_ascii=False), encoding="utf-8"
        )
    except OSError:
        pass


def _executions(case_path):
    for path in sorted(case_path.glob("*/*/execution.json")):
        try:
            yield path, json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue


def _legacy(case_path):
    """Archivos de resultado del formato anterior a v1.3."""
    found = []
    for folder, name in LEGACY_FILES:
        path = case_path / folder / name
        if path.is_file():
            try:
                content = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if content.strip():
                found.append((f"{folder}/{name}", content))
    return found


def _fence(text):
    text = (text or "").rstrip()
    fence = "```"
    while fence in text:
        fence += "`"
    return f"{fence}text\n{text}\n{fence}"


def _register_report(case_path, info, rel_path):
    reports = info.get("reports")
    if not isinstance(reports, list):
        reports = []
    if rel_path not in reports:
        reports.append(rel_path)
    info["reports"] = reports
    info["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _save_info(case_path, info)


def _show(case_path, report_path):
    if os.environ.get("OSINT_SHOW_REPORT", "1") != "1":
        return
    if not sys.stdout.isatty():
        return
    try:
        from app.ui import viewer
    except ImportError:
        return
    viewer.view(case_path, report_path)


def generate_report(case_path: Path, results=None):
    case_path = Path(case_path)
    info = _load_info(case_path)
    if not info:
        return None

    report_dir = case_path / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    generated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    summary = {
        "case_id": info.get("case_id"),
        "target": info.get("target"),
        "type": info.get("type"),
        "status": info.get("status"),
        "generated": generated,
    }
    (report_dir / "summary.json").write_text(
        json.dumps(summary, indent=4, ensure_ascii=False), encoding="utf-8"
    )

    lines = [
        "# OSINT REPORT",
        "",
        f"- Case ID: {info.get('case_id')}",
        f"- Target: {info.get('target')}",
        f"- Type: {info.get('type')}",
        f"- Status: {info.get('status')}",
        f"- Created: {info.get('created')}",
        f"- Generated: {generated}",
        "",
        "## Herramientas ejecutadas",
        "",
        "| Herramienta | Estado | Hallazgos | Duración (s) |",
        "|---|---|---|---|",
    ]

    evidence = []
    rows = 0
    for path, meta in _executions(case_path):
        tool = meta.get("tool", "?")
        rows += 1
        lines.append(
            f"| {tool} | {meta.get('status', '?')} | "
            f"{meta.get('findings', 0)} | {meta.get('duration', 0)} |"
        )
        out = path.parent / "stdout.txt"
        if out.is_file():
            content = out.read_text(encoding="utf-8", errors="replace")
            if content.strip():
                evidence.append(f"### {tool}\n\n{_fence(content)}\n")

    if rows == 0:
        lines.append("| — | — | — | — |")

    lines += ["", "## Evidencia", ""]

    if evidence:
        lines += evidence
    else:
        legacy = _legacy(case_path)
        if legacy:
            for label, content in legacy:
                lines += [f"### {label}", "", _fence(content), ""]
        if not (case_path / "users" / "sherlock.txt").is_file():
            lines.append("No hay resultados de Sherlock para este caso.")
        if not legacy:
            lines.append("")
            lines.append("Sin salida registrada.")

    lines += ["", "## Fin del reporte", ""]

    report_path = report_dir / "report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")

    _register_report(case_path, info, f"reports/{report_path.name}")
    _show(case_path, report_path)

    return report_path
