from rich.console import Console

from core.case_manager import create_case
from core.logger import log

from services.sherlock_service import run as sherlock
from services.maigret_service import run as maigret

console = Console()


def menu():

    console.clear()

    console.rule("[bold cyan]Investigación de Usuario[/]")

    username = console.input(
        "\n[bold green]Nombre de usuario:[/] "
    ).strip()

    if not username:
        return

    case = create_case(username)

    log(case, "INFO", "Investigación iniciada")

    console.print("\n📁 Caso creado")
    console.print(case)

    console.print("\n🔍 Ejecutando Sherlock...")

    if sherlock(
        username,
        case / "users",
        case
    ):
        console.print("[green]✔ Sherlock OK[/]")
        log(case, "SUCCESS", "Sherlock finalizado")
    else:
        console.print("[red]✖ Sherlock ERROR[/]")
        log(case, "ERROR", "Sherlock falló")

    console.print("\n🔍 Ejecutando Maigret...")

    if maigret(
        username,
        case / "users",
        case
    ):
        console.print("[green]✔ Maigret OK[/]")
        log(case, "SUCCESS", "Maigret finalizado")
    else:
        console.print("[red]✖ Maigret ERROR[/]")
        log(case, "ERROR", "Maigret falló")

    log(case, "INFO", "Investigación finalizada")

    console.print("\n[bold green]Investigación terminada.[/]")
    console.print(case)

    console.input("\nENTER para continuar...")
