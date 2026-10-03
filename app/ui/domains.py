from rich.console import Console

from core.case_manager import create_case
from core.engine import run

console = Console()


def menu():

    console.clear()

    console.rule("[bold cyan]Investigación de Dominio[/]")

    domain = console.input(
        "\n[bold green]Dominio:[/] "
    ).strip()

    if not domain:
        return

    case = create_case(
        domain,
        "domain"
    )

    console.print("\n📁 Caso creado")
    console.print(case)

    run(
        case,
        "domains",
        domain
    )

    console.print("\n[bold green]Investigación terminada.[/]")

    console.input("\nENTER para continuar...")
