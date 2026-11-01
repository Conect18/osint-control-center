import re
from pathlib import Path

from app.core.normalize import normalize_user
from app.core.runner import Status, run_tool

FOUND = re.compile(r"^\s*\[\+\]", re.MULTILINE)
BLOCK = re.compile(r"^\[\*\] Checking username (.+?) on:", re.MULTILINE)


def _blocks(folder):
    """Devuelve {username: cantidad de hallazgos} separado por bloque."""
    path = folder / "stdout.txt"
    if not path.is_file():
        return {}

    text = path.read_text(encoding="utf-8", errors="replace")
    marks = list(BLOCK.finditer(text))

    counts = {}
    for index, mark in enumerate(marks):
        end = marks[index + 1].start() if index + 1 < len(marks) else len(text)
        chunk = text[mark.end():end]
        name = mark.group(1).strip().lower()
        counts[name] = counts.get(name, 0) + len(FOUND.findall(chunk))
    return counts


def run(username, output_dir, case):
    username = normalize_user(username)
    out = Path(output_dir)
    folder = out / "maigret"

    result = run_tool(
        "Maigret",
        ["maigret", username, "--folderoutput", str(folder),
         "--json", "simple", "--no-progressbar", "--timeout", "15", "--no-color"],
        out, case, timeout=1800,
    )
    if not result.ok:
        return result

    counts = _blocks(folder)
    result.findings = counts.get(username, 0)
    total = sum(counts.values())

    if result.findings:
        result.message = f"Maigret: {result.findings} cuentas (total con variantes: {total})"
    elif total:
        result.status = Status.EMPTY
        result.message = f"Maigret: 0 para el objetivo (total con variantes: {total})"
    else:
        result.status = Status.EMPTY
        result.message = "Maigret: sin cuentas"
    return result
