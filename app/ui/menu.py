from rich.console import Console
from rich.panel import Panel

console = Console()


def show_menu():

    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]MENÚ PRINCIPAL[/]",
            border_style="blue",
        )
    )

    console.print("1. 📊 Dashboard")
    console.print("2. 👤 Usuarios")
    console.print("3. 📧 Correos")
    console.print("4. 🌐 Dominios")
    console.print("5. 🛠 Herramientas")
    console.print("6. 📂 Resultados")
    console.print("7. 📑 Reportes")
    console.print("0. ❌ Salir")

    console.print()

    return input("Seleccione una opción: ")
