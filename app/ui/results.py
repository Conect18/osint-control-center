from pathlib import Path

from rich.console import Console
from rich.table import Table

from app.config.settings import CASES_PATH
from app.core.active_case import get_case
from app.ui import viewer
from app.utils.files import case_files

console = Console()

HINT = (
    "[dim]Nº = abrir · f = primero · u = último · r Nº = crudo · "
    "e Nº = editor · c Nº = copiar ruta · ENTER = volver[/]"
)


def list_cases() -> list[Path]:
    if not CASES_PATH.exists():
        return []

    return sorted(
        (path for path in CASES_PATH.iterdir() if path.is_dir()),
        reverse=True,
    )


def _open(case: Path, files: list[Path], command: str, argument: str) -> None:
    if command in {"f", "u"}:
        viewer.view(case, files[0] if command == "f" else files[-1])
        return

    number = int(argument or console.input("Nº: "))
    target = files[number - 1]

    if command == "r":
        viewer.view(case, target, raw=True)
    elif command == "e":
        viewer.open_external(target)
    else:
        viewer.copy_path(target)


def show_case_results(case: Path) -> None:
    while True:

        console.clear()

        console.rule(f"[bold cyan]📂 Resultados: {case.name}[/]")

        files = case_files(case)

        if not files:

            console.print("\n[yellow]Este caso todavía no tiene resultados.[/]")
            console.input("\nENTER para volver...")
            return

        table = Table(show_header=True)

        table.add_column("#", justify="right")
        table.add_column("Resultado")
        table.add_column("Tamaño")

        for index, file in enumerate(files, start=1):

            table.add_row(
                str(index),
                str(file.relative_to(case)),
                f"{file.stat().st_size} bytes",
            )

        console.print(table)
        console.print(HINT)

        raw = console.input("\n> ").strip().lower()

        if not raw:
            return

        command, _, argument = raw.partition(" ")

        try:
            if command in {"f", "u", "r", "e", "c"}:
                _open(case, files, command, argument)
            elif command.isdigit():
                viewer.view(case, files[int(command) - 1])
            else:
                console.print("\n[red]Opción inválida.[/]")
                continue
        except (IndexError, ValueError):
            console.print("\n[red]Número fuera de rango.[/]")
            continue

        console.input("\nENTER para volver al listado.")


def open_active() -> None:
    case = get_case()

    if case is None:

        console.print(
            "\n[yellow]No hay caso activo. Crea uno desde Usuarios, Correos o Dominios.[/]"
        )
        console.input("\nENTER...")
        return

    show_case_results(case)


def menu() -> None:
    while True:

        console.clear()

        console.rule("[bold cyan]📂 Casos de Investigación[/]")

        cases = list_cases()

        if not cases:

            console.print("\n[yellow]No hay investigaciones registradas.[/]")
            console.input("\nENTER para volver...")
            return

        active = get_case()

        table = Table(show_header=True)

        table.add_column("#", justify="right")
        table.add_column("Caso")
        table.add_column("Ruta")
        table.add_column("")

        for index, case in enumerate(cases, start=1):

            table.add_row(
                str(index),
                case.name,
                str(case),
                "activo" if active and case.resolve() == active else "",
            )

        console.print(table)

        console.print("\n[bold green]Selecciona un caso.[/]")
        console.print("[dim]f = primero · u = último · a = caso activo · 0 = volver[/]")

        choice = console.input("Número [0 para volver]: ").strip().lower()

        if choice == "0":
            return

        if choice in {"f", "u", "a"}:

            if choice == "f":
                show_case_results(cases[-1])
            elif choice == "u":
                show_case_results(cases[0])
            elif active is None:
                console.print("\n[red]No hay caso activo.[/]")
                console.input("\nENTER...")
            else:
                show_case_results(active)

            continue

        if not choice.isdigit():

            console.print("\n[red]Opción inválida.[/]")
            console.input("\nENTER...")
            continue

        number = int(choice)

        if number < 1 or number > len(cases):

            console.print("\n[red]Número de caso inválido.[/]")
            console.input("\nENTER...")
            continue

        show_case_results(cases[number - 1])
