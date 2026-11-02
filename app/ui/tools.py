import subprocess

from rich.console import Console
from rich.table import Table

console = Console()


TOOLS = [
    ("Sherlock", ["sherlock", "--version"]),
    ("Maigret", ["maigret", "--version"]),
    ("Holehe", ["holehe", "--help"]),
    ("Sublist3r", ["sublist3r", "-h"]),
    ("Nmap", ["nmap", "--version"]),
]


def menu():

    console.clear()

    table = Table(title="🛠 Herramientas OSINT")

    table.add_column("Herramienta", style="cyan")
    table.add_column("Estado", style="green")

    for name, cmd in TOOLS:

        try:

            subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=5
            )

            estado = "✅ Disponible"

        except Exception:

            estado = "❌ No encontrada"

        table.add_row(name, estado)

    console.print(table)

    console.input("\nENTER para volver...")
