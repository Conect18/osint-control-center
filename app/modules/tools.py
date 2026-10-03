from rich.console import Console
from rich.panel import Panel

console = Console()


def menu():

    console.clear()

    console.print(
        Panel.fit(
            "[bold cyan]🛠 Herramientas OSINT[/]",
            border_style="cyan"
        )
    )

    console.print("\n🚧 Módulo en desarrollo.\n")

    console.input("Presiona ENTER para volver...")
