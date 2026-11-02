"""Presentación visual del análisis interpretado de un caso."""

from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from app.core.result_parser import parse_case

console = Console()


def show_profiles(profiles, title, limit=30):
    """Muestra perfiles encontrados en una tabla."""
    if not profiles:
        console.print("[yellow]No se encontraron perfiles.[/]")
        return

    table = Table(title=title)
    table.add_column("#", justify="right")
    table.add_column("Plataforma")
    table.add_column("Usuario")
    table.add_column("Estado")
    table.add_column("URL")

    for index, profile in enumerate(profiles[:limit], start=1):
        table.add_row(
            str(index),
            str(profile.get("site") or "Desconocido"),
            str(profile.get("username") or "-"),
            str(profile.get("status") or "-"),
            str(profile.get("url") or "-"),
        )

    console.print(table)

    if len(profiles) > limit:
        console.print(
            f"[dim]Se muestran {limit} de {len(profiles)} resultados.[/]"
        )


def show_analysis(case: Path) -> None:
    """Muestra un resumen legible de los resultados de una investigación."""
    report = parse_case(case)

    console.clear()
    console.rule("[bold cyan]ANÁLISIS DE INVESTIGACIÓN[/]")

    console.print(
        Panel(
            f"[bold]Caso:[/] {report['case_id']}\n"
            f"[bold]Objetivo:[/] {report['target']}\n"
            f"[bold]Tipo:[/] {report['type']}\n"
            f"[bold]Estado:[/] {report['status']}",
            title="INFORMACIÓN GENERAL",
            border_style="cyan",
        )
    )

    if not report["tools"]:
        console.print("\n[yellow]No hay resultados interpretables.[/]")
        console.input("\nENTER para volver...")
        return

    for item in report["tools"]:
        analysis = item.get("analysis", {})
        tool = item["tool"].lower()

        console.print()
        console.rule(f"[bold green]{item['tool']}[/]")
        console.print(
            f"Estado: [bold]{item['status']}[/]  "
            f"Hallazgos: [bold]{item['findings']}[/]  "
            f"Duración: [bold]{item['duration']} s[/]"
        )

        if tool == "nmap":
            console.print(
                f"\n[bold]Host:[/] {analysis.get('host') or 'No identificado'}"
            )
            console.print(
                f"[bold]Estado del host:[/] {analysis.get('status')}"
            )

            addresses = analysis.get("addresses", [])
            if addresses:
                console.print(
                    "[bold]Direcciones IP:[/] " + ", ".join(addresses)
                )

            latency = analysis.get("latency")
            if latency is not None:
                console.print(f"[bold]Latencia:[/] {latency * 1000:.2f} ms")

            ports = Table(title="Puertos TCP detectados")
            ports.add_column("Puerto", justify="right")
            ports.add_column("Estado")
            ports.add_column("Servicio")

            for port in analysis.get("ports", []):
                state = port["state"]
                style = "green" if state == "open" else "yellow"
                ports.add_row(
                    str(port["port"]),
                    f"[{style}]{state}[/]",
                    port["service"],
                )

            if analysis.get("ports"):
                console.print(ports)
            else:
                console.print("[yellow]No se detectaron puertos.[/]")

            console.print(
                f"Puertos filtrados: [bold]{analysis.get('filtered', 0)}[/]"
            )

            reverse_dns = analysis.get("reverse_dns")
            if reverse_dns:
                console.print(f"DNS inverso: {reverse_dns}")

            interpretation = (
                "Los puertos abiertos indican servicios que respondieron "
                "al escaneo. Esto no demuestra por sí solo que exista una "
                "vulnerabilidad.\n\n"
                "Los puertos filtrados no respondieron de forma que Nmap "
                "pudiera determinar su estado."
            )

        elif tool == "sublist3r":
            subdomains = analysis.get("subdomains", [])
            console.print(
                f"\n[bold]Subdominios encontrados:[/] "
                f"{analysis.get('total', 0)}"
            )

            if subdomains:
                table = Table(title="Subdominios detectados")
                table.add_column("#", justify="right")
                table.add_column("Nombre")

                for index, subdomain in enumerate(subdomains, start=1):
                    table.add_row(str(index), subdomain)

                console.print(table)
            else:
                console.print("[yellow]No se encontraron subdominios.[/]")

            interpretation = (
                "Los subdominios identificados son nombres asociados "
                "al dominio consultado. Su aparición no confirma que "
                "el servicio esté activo o accesible."
            )

        elif tool == "sherlock":
            profiles = analysis.get("profiles", [])
            console.print(
                f"\n[bold]Perfiles encontrados:[/] {analysis.get('total', 0)}"
            )

            reported = analysis.get("reported_total")
            if reported is not None:
                console.print(
                    f"[bold]Resultados informados por Sherlock:[/] {reported}"
                )

            show_profiles(profiles, "Perfiles detectados")

            interpretation = (
                "Los perfiles encontrados son coincidencias potenciales "
                "del nombre de usuario. No confirman que las cuentas "
                "pertenezcan a la misma persona. Verifique manualmente "
                "cada URL y sus datos públicos."
            )

        elif tool == "holehe":
            used = analysis.get("used", [])
            not_used = analysis.get("not_used", [])
            limited = analysis.get("rate_limited", [])

            console.print(
                f"\n[bold green]Servicios utilizados:[/] "
                f"{analysis.get('total_used', len(used))}"
            )
            console.print(
                f"[bold red]Servicios no utilizados:[/] "
                f"{analysis.get('total_not_used', len(not_used))}"
            )
            console.print(
                f"[bold yellow]Límites de consulta:[/] "
                f"{analysis.get('total_rate_limited', len(limited))}"
            )

            for title, sites in (
                ("Servicios con correo registrado", used),
                ("Servicios sin registro detectado", not_used),
                ("Servicios con límite de consulta", limited),
            ):
                if sites:
                    table = Table(title=title)
                    table.add_column("#", justify="right")
                    table.add_column("Servicio")

                    for index, site in enumerate(sites, start=1):
                        table.add_row(str(index), site)

                    console.print(table)

            interpretation = (
                "Los resultados reflejan las respuestas de los servicios "
                "consultados. Un registro detectado no demuestra la "
                "titularidad del correo. Los límites de consulta pueden "
                "impedir obtener resultados completos."
            )

        elif tool == "maigret":
            claimed = analysis.get("claimed", [])
            other = analysis.get("other", [])

            console.print(
                f"\n[bold]Perfiles analizados:[/] {analysis.get('total', 0)}"
            )
            console.print(
                f"[bold green]Perfiles Claimed:[/] "
                f"{analysis.get('total_claimed', len(claimed))}"
            )
            console.print(
                f"[bold yellow]Otros estados:[/] "
                f"{analysis.get('total_other', len(other))}"
            )

            show_profiles(claimed, "Perfiles Claimed")
            if other:
                show_profiles(other, "Perfiles con otros estados")

            interpretation = (
                "Claimed significa que Maigret considera que el perfil "
                "está registrado en esa plataforma. No confirma la "
                "identidad ni la titularidad de la cuenta. Los resultados "
                "requieren verificación manual."
            )

        else:
            interpretation = (
                "Esta herramienta todavía no tiene un analizador específico."
            )

        console.print(
            Panel(
                interpretation,
                title="INTERPRETACIÓN",
                border_style="yellow",
            )
        )

        console.print(
            f"[dim]Evidencia: {analysis.get('evidence', 'No disponible')}[/]"
        )
        console.print(
            f"[dim]Metadatos: {item.get('evidence', 'No disponibles')}[/]"
        )

    console.print()
    console.rule("[bold cyan]FIN DEL ANÁLISIS[/]")
    console.input("\nENTER para volver...")
