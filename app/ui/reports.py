from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from app.config.settings import CASES_PATH
from app.ui import viewer

console = Console()


def _reports() -> list[Path]:
    files = [path for path in CASES_PATH.glob("*/reports/*") if path.is_file()]
    return sorted(files, key=lambda path: path.stat().st_mtime, reverse=True)


def menu() -> None:
    while True:

        console.clear()

        console.print(Panel.fit("[bold cyan]📑 Reportes[/]", border_style="cyan"))

        reports = _reports()

        if not reports:

            console.print("\n[yellow]Todavía no existen reportes generados.[/]")
            console.input("\nENTER para volver...")
            return

        table = Table(show_header=True)

        table.add_column("#", justify="right")
        table.add_column("Caso")
        table.add_column("Reporte")
        table.add_column("Ruta")

        for index, report in enumerate(reports, start=1):

            table.add_row(
                str(index),
                report.parent.parent.name,
                report.name,
                str(report),
            )

        console.print(table)
        console.print(
            "[dim]Nº = abrir · r Nº = crudo · e Nº = editor · "
            "c Nº = copiar ruta · ENTER = volver[/]"
        )

        raw = console.input("\n> ").strip().lower()

        if not raw:
            return

        command, _, argument = raw.partition(" ")

        try:
            if command in {"r", "e", "c"}:
                report = reports[int(argument or console.input("Nº: ")) - 1]
                case_dir = report.parent.parent
                if command == "r":
                    viewer.view(case_dir, report, raw=True)
                elif command == "e":
                    viewer.open_external(report)
                else:
                    viewer.copy_path(report)
            elif command.isdigit():
                report = reports[int(command) - 1]
                viewer.view(report.parent.parent, report)
            else:
                console.print("\n[red]Opción inválida.[/]")
                continue
        except (IndexError, ValueError):
            console.print("\n[red]Número fuera de rango.[/]")
            continue

        console.input("\nENTER para volver al listado.")
