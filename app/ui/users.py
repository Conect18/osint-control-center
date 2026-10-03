from rich.console import Console

from core.case_manager import create_case
from core.logger import log
from core.engine import run

console = Console()


def menu():

    console.clear()

    console.rule("[bold cyan]Investigación de Usuario[/]")

    username = console.input(
        "\n[bold green]Nombre de usuario:[/] "
    ).strip()

    if not username:
        return

    case = create_case(
        username,
        "users"
    )

    log(
        case,
        "INFO",
        "Investigación iniciada"
    )

    console.print("\n📁 Caso creado")
    console.print(case)

    run(
        case,
        "users",
        username
    )

    log(
        case,
        "INFO",
        "Investigación finalizada"
    )

    console.print()
    console.print(
        "[bold green]Investigación terminada.[/]"
    )

    console.input("\nENTER para continuar...")
