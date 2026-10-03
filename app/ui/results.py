from pathlib import Path

from rich.console import Console
from rich.table import Table


console = Console()


CASES_DIR = Path.home() / "osint-lab" / "cases"


def list_cases():

    if not CASES_DIR.exists():
        return []

    return sorted(
        [d for d in CASES_DIR.iterdir() if d.is_dir()],
        reverse=True
    )


def show_case_results(case):

    while True:

        console.clear()

        console.rule(
            f"[bold cyan]📂 Resultados: {case.name}[/]"
        )

        files = []

        for path in sorted(case.rglob("*")):

            if path.is_file():
                files.append(path)

        if not files:

            console.print(
                "\n[yellow]Este caso todavía no tiene resultados.[/]"
            )

            console.input("\nENTER para volver...")
            return

        table = Table(show_header=True)

        table.add_column("#", justify="right")
        table.add_column("Resultado")
        table.add_column("Tamaño")

        for i, file in enumerate(files, start=1):

            size = file.stat().st_size

            table.add_row(
                str(i),
                str(file.relative_to(case)),
                f"{size} bytes"
            )

        console.print(table)

        console.print(
            "\n[dim]ENTER para volver al listado de casos.[/]"
        )

        console.input()

        return


def menu():

    while True:

        console.clear()

        console.rule(
            "[bold cyan]📂 Casos de Investigación[/]"
        )

        cases = list_cases()

        if not cases:

            console.print(
                "\n[yellow]No hay investigaciones registradas.[/]"
            )

            console.input("\nENTER para volver...")
            return

        table = Table(show_header=True)

        table.add_column("#", justify="right")
        table.add_column("Caso")
        table.add_column("Ruta")

        for i, case in enumerate(cases, start=1):

            table.add_row(
                str(i),
                case.name,
                str(case)
            )

        console.print(table)

        console.print(
            "\n[bold green]Selecciona un caso.[/]"
        )

        choice = console.input(
            "Número [0 para volver]: "
        ).strip()

        if choice == "0":
            return

        if not choice.isdigit():
            console.print(
                "\n[red]Opción inválida.[/]"
            )
            console.input("\nENTER...")
            continue

        number = int(choice)

        if number < 1 or number > len(cases):

            console.print(
                "\n[red]Número de caso inválido.[/]"
            )
            console.input("\nENTER...")
            continue

        selected_case = cases[number - 1]

        show_case_results(selected_case)
