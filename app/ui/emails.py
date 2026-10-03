from rich.console import Console

from core.case_manager import create_case
from core.engine import run

console = Console()


def menu():

    console.clear()

    console.rule("[bold cyan]Investigación de Correo[/]")

    email = console.input(
        "\n[bold green]Correo electrónico:[/] "
    ).strip()

    if not email:
        return

    case = create_case(
        email,
        "email"
    )

    console.print("\n📁 Caso creado")
    console.print(case)

    run(
        case,
        "emails",
        email
    )

    console.print("\n[bold green]Investigación terminada.[/]")

    console.input("\nENTER para continuar...")
