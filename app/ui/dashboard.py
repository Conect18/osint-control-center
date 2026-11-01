from pathlib import Path
import shutil
import subprocess

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from app.core.active_case import get_case

console = Console()


def check_tool(tool):
    return "✅ Instalado" if shutil.which(tool) else "❌ No"


def get_version(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        return result.stdout.splitlines()[0]

    except Exception:
        return "-"


def count_cases():

    cases = Path.home() / "osint-lab" / "cases"

    if not cases.exists():
        return 0

    return len([c for c in cases.iterdir() if c.is_dir()])


def show_dashboard():

    console.clear()

    console.print(
        Panel.fit(
            "[bold cyan]🛡️  OSINT CONTROL CENTER[/]\nVersión 1.2",
            border_style="cyan",
        )
    )

    table = Table(title="Estado del Laboratorio")

    table.add_column("Elemento", style="cyan")
    table.add_column("Estado", style="green")

    table.add_row("Python", get_version(["python3", "--version"]).replace("Python ", ""))
    table.add_row("Git", get_version(["git", "--version"]).replace("git version ", ""))

    table.add_row("Sherlock", check_tool("sherlock"))
    table.add_row("Holehe", check_tool("holehe"))
    table.add_row("Maigret", check_tool("maigret"))
    table.add_row("Sublist3r", check_tool("sublist3r"))
    table.add_row("Nmap", check_tool("nmap"))

    table.add_row("Casos", str(count_cases()))

    total, used, free = shutil.disk_usage(Path.home())

    table.add_row(
        "Disco libre",
        f"{free // (1024**3)} GB"
    )

    case = get_case()

    if case:
        table.add_row("Caso activo", case.name)
    else:
        table.add_row("Caso activo", "Ninguno")

    console.print(table)

    console.print(
        f"\n[cyan]Laboratorio:[/] {Path.home() / 'osint-lab'}"
    )
