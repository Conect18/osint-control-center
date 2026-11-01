from rich.console import Console

from app.core.case_manager import create_case
from app.core.engine import run
from app.core.normalize import InvalidTarget

console = Console()


def menu():

    console.clear()

    console.rule("[bold cyan]Investigación de Correo[/]")

    email = console.input(
        "\n[bold green]Correo electrónico:[/] "
    ).strip()

    if not email:
        return

    try:
        case = create_case(
            email,
            "email"
        )
    except InvalidTarget as exc:
        console.print(f"\n[bold red]Objetivo inválido:[/] {exc}")
        console.input("\nENTER para continuar...")
        return

    console.print("\n📁 Caso creado")
    console.print(case)

    try:
        run(
            case,
            "emails",
            email
        )
    except Exception as exc:
        console.print(f"\n[bold red]Error durante la investigación:[/] {exc}")
        console.input("\nENTER para continuar...")
        return

    console.print("\n[bold green]Investigación terminada.[/]")

    console.input("\nENTER para continuar...")
