from rich.console import Console

from core.case_manager import create_case
from core.active_case import set_case
from core.logger import log

from services.sherlock_service import run as sherlock
from services.maigret_service import run as maigret

console = Console()


def investigate_username(username):

    # Crear caso
    case = create_case(username)

    # Marcar como caso activo
    set_case(case)

    log(case, "INFO", "Investigación iniciada")

    console.print("\n📁 Caso creado")
    console.print(case)

    console.print("\n🔍 Sherlock...")

    if sherlock(username, case / "users"):
        log(case, "SUCCESS", "Sherlock finalizado")
        console.print("[green]✔ Sherlock OK[/]")
    else:
        log(case, "ERROR", "Sherlock falló")
        console.print("[red]✖ Sherlock ERROR[/]")

    console.print("\n🔍 Maigret...")

    if maigret(username, case / "users"):
        log(case, "SUCCESS", "Maigret finalizado")
        console.print("[green]✔ Maigret OK[/]")
    else:
        log(case, "ERROR", "Maigret falló")
        console.print("[red]✖ Maigret ERROR[/]")

    log(case, "INFO", "Investigación finalizada")

    return case
