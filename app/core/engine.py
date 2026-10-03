from rich.console import Console

from core.logger import log
from core.report_generator import generate_report
from tool_registry import get_tools

console = Console()


def run(case, category, value):
    """
    Ejecuta todas las herramientas registradas
    para una categoría OSINT.
    """

    tools = get_tools(category)

    if not tools:
        console.print("[yellow]No hay herramientas registradas.[/]")
        return

    success = 0
    failed = 0

    for tool in tools:

        console.print(
            f"\n🔍 Ejecutando {tool['name']}..."
        )

        log(
            case,
            "INFO",
            f"{tool['name']} iniciado"
        )

        ok = tool["runner"](
            value,
            case / category,
            case
        )

        if ok:

            success += 1

            log(
                case,
                "SUCCESS",
                f"{tool['name']} finalizado"
            )

            console.print(
                f"[green]✔ {tool['name']} OK[/]"
            )

        else:

            failed += 1

            log(
                case,
                "ERROR",
                f"{tool['name']} falló"
            )

            console.print(
                f"[red]✖ {tool['name']} ERROR[/]"
            )

    generate_report(case)

    console.print()

    console.print(
        f"[bold cyan]Herramientas correctas:[/] {success}"
    )

    console.print(
        f"[bold red]Herramientas con error:[/] {failed}"
    )
