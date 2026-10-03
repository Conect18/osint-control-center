from pathlib import Path

from rich.console import Console
from rich.panel import Panel

console = Console()


def menu():

    console.clear()

    console.print(
        Panel.fit(
            "[bold cyan]📑 Reportes[/]",
            border_style="cyan"
        )
    )

    reports = list(
        Path.home()
        .joinpath("osint-lab", "cases")
        .glob("*/reports/*")
    )

    console.print()

    if reports:

        for report in reports:

            console.print(f"📄 {report}")

    else:

        console.print(
            "[yellow]Todavía no existen reportes generados.[/]"
        )

    console.input("\nENTER para volver...")
