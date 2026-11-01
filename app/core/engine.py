from pathlib import Path

from rich.console import Console

from app.core.logger import log
from app.core.report_generator import generate_report
from app.core.runner import Status
from app.tool_registry import get_tools

console = Console()


def run(case, category, value):
    case = Path(case)
    tools = get_tools(category)

    if not tools:
        console.print("[yellow]No hay herramientas habilitadas para esta categoría.[/]")
        return {"ok": 0, "empty": 0, "failed": 0}

    base = case / category
    base.mkdir(parents=True, exist_ok=True)

    counters = {"ok": 0, "empty": 0, "failed": 0}
    results = []

    for tool in tools:
        console.print(f"\n🔍 Ejecutando {tool['name']}...")

        result = tool["runner"](value, base, case)
        results.append(result)

        if result is not None:
            result.save()
            log(case, "SUCCESS" if result.ok else "ERROR", result.message)

        if result is None:
            counters["failed"] += 1
            console.print(f"[red]✖ {tool['name']}: sin resultado[/]")
        elif result.status is Status.OK:
            counters["ok"] += 1
            console.print(f"[green]✔ {tool['name']}: {result.findings} hallazgo(s)[/]")
        elif result.status is Status.EMPTY:
            counters["empty"] += 1
            console.print(f"[yellow]• {tool['name']}: sin hallazgos[/]")
        else:
            counters["failed"] += 1
            console.print(f"[red]✖ {tool['name']}: {result.message}[/]")

    generate_report(case, results)

    console.print()
    console.print(f"[bold green]Con hallazgos:[/] {counters['ok']}")
    console.print(f"[bold yellow]Sin hallazgos:[/] {counters['empty']}")
    console.print(f"[bold red]Con error:[/] {counters['failed']}")

    return counters
