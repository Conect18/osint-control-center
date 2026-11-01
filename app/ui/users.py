from rich.console import Console

from app.core.case_manager import create_case
from app.core.engine import run
from app.core.logger import log
from app.core.normalize import InvalidTarget

console = Console()


def menu():
    console.clear()
    console.rule("[bold cyan]Investigación de Usuario[/]")

    raw = console.input("\n[bold green]Nombre de usuario:[/] ").strip()
    if not raw:
        return

    try:
        case = create_case(raw, "users")
    except InvalidTarget as exc:
        console.print(f"[red]Objetivo inválido:[/] {exc}")
        console.input("\nENTER para continuar...")
        return

    log(case, "INFO", "Investigación iniciada")
    console.print("\n📁 Caso creado")
    console.print(case)

    run(case, "users", raw)

    log(case, "INFO", "Investigación finalizada")
    console.print("\n[bold green]Investigación terminada.[/]")
    console.input("\nENTER para continuar...")
