"""Visor de archivos del caso: ruta, metadatos, paginador y portapapeles."""

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

from app.utils.files import MAX_INLINE_BYTES, read_text_safe, resolve_in_case

console = Console()

MARKDOWN_EXT = {".md", ".markdown"}
JSON_EXT = {".json", ".jsonl"}
SYNTAX_EXT = {
    ".py", ".sh", ".yaml", ".yml", ".xml", ".html",
    ".css", ".js", ".toml", ".ini", ".cfg",
}


def pager_enabled() -> bool:
    return sys.stdout.isatty() and not os.environ.get("OSINT_NO_PAGER")


def _stamp(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def _header(case_dir: Path, path: Path) -> Panel:
    stat = path.stat()

    return Panel(
        "\n".join(
            [
                f"[bold]Caso:[/] {case_dir.name}",
                f"[bold]Ruta:[/] {path.resolve()}",
                f"[bold]URI:[/] file://{path.resolve()}",
                f"[bold]Tamaño:[/] {stat.st_size} bytes",
                f"[bold]Modificado:[/] {_stamp(stat.st_mtime)}",
            ]
        ),
        title="VISOR",
        border_style="cyan",
        expand=False,
    )


def _render(path: Path, text: str, raw: bool) -> None:
    if raw:
        console.print(Syntax(text, lexer=None, line_numbers=True, word_wrap=True))
        return

    suffix = path.suffix.lower()

    if suffix in MARKDOWN_EXT:
        console.print(Markdown(text))
    elif suffix in JSON_EXT:
        try:
            pretty = json.dumps(json.loads(text), indent=4, ensure_ascii=False)
        except json.JSONDecodeError:
            console.print(Syntax(text, "json", line_numbers=True, word_wrap=True))
        else:
            console.print(Syntax(pretty, "json", line_numbers=True, word_wrap=True))
    elif suffix in SYNTAX_EXT:
        console.print(Syntax(text, suffix.lstrip("."), line_numbers=True, word_wrap=True))
    else:
        console.print(Text(text))


def open_external(path: Path) -> bool:
    """Abre en el paginador del sistema o en el visor del escritorio."""
    pager = os.environ.get("PAGER") or ("less" if shutil.which("less") else None)

    if pager:
        subprocess.call([pager, "-R", str(path)])
        return True

    if shutil.which("xdg-open"):
        subprocess.call(["xdg-open", str(path)])
        return True

    console.print("\n[red]No hay less ni xdg-open disponibles.[/]")
    return False


def copy_path(path: Path) -> None:
    for command in (["wl-copy"], ["xclip", "-selection", "clipboard"], ["xsel", "-b"]):
        if not shutil.which(command[0]):
            continue
        try:
            subprocess.run(command, input=str(path.resolve()).encode(), check=True)
        except (OSError, subprocess.CalledProcessError):
            continue
        console.print(f"\n[green]Ruta copiada:[/] {path.resolve()}")
        return

    console.print("\n[yellow]Sin portapapeles; copia la ruta del encabezado a mano.[/]")


def view(case_dir: Path, path: Path, *, raw: bool = False) -> bool:
    case_dir = Path(case_dir)

    try:
        target = resolve_in_case(case_dir, Path(path))
    except (ValueError, FileNotFoundError) as exc:
        console.print(f"\n[red]No se puede abrir:[/] {exc}")
        return False

    size = target.stat().st_size

    if size > MAX_INLINE_BYTES:
        console.print(_header(case_dir, target))
        console.print(
            f"\n[yellow]Archivo grande ({size} bytes); se abre en el visor del sistema.[/]"
        )
        return open_external(target)

    if size == 0:
        console.print(_header(case_dir, target))
        console.print("\n[yellow]Archivo vacío.[/]")
        return True

    try:
        text, encoding = read_text_safe(target)
    except ValueError:
        console.print(_header(case_dir, target))
        console.print("\n[yellow]Contenido binario; se abre en el visor del sistema.[/]")
        return open_external(target)

    def body() -> None:
        console.print(_header(case_dir, target))
        console.print(f"[dim]Codificación: {encoding}[/]\n")
        _render(target, text, raw)
        console.print(f"\n[dim]Fin del archivo · {target.resolve()}[/]")

    if pager_enabled():
        with console.pager(styles=True):
            body()
    else:
        body()

    return True
