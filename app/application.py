import importlib
import os
import traceback

from rich.console import Console

from app.core.normalize import InvalidTarget
from app.ui.dashboard import show_dashboard
from app.ui.menu import show_menu

console = Console()

MENU_HANDLERS = {
    "2": ("app.ui.users", "menu"),
    "3": ("app.ui.emails", "menu"),
    "4": ("app.ui.domains", "menu"),
    "5": ("app.ui.tools", "menu"),
    "6": ("app.ui.results", "menu"),
    "7": ("app.ui.reports", "menu"),
    "8": ("app.ui.results", "open_active"),
}


class OSINTApplication:

    def run(self):
        try:
            self._loop()
        except KeyboardInterrupt:
            console.print("\nInterrumpido. Hasta luego.\n")
        except EOFError:
            console.print("\nHasta luego.\n")

    def _loop(self):
        while True:

            show_dashboard()

            option = show_menu()

            if option == "0":
                console.print("\nHasta luego.\n")
                return

            if option == "1":
                continue

            handler = MENU_HANDLERS.get(option)

            if handler is None:
                console.print("\nOpción inválida.\n")
                input("ENTER...")
                continue

            self._dispatch(*handler)

    def _dispatch(self, module_name, func_name):
        try:
            module = importlib.import_module(module_name)
            getattr(module, func_name)()
        except InvalidTarget as exc:
            console.print(f"\n[bold red]Objetivo inválido:[/] {exc}")
            input("ENTER...")
        except Exception as exc:
            if os.environ.get("OSINT_DEBUG"):
                traceback.print_exc()
            console.print(f"\n[bold red]Error inesperado:[/] {exc}")
            input("ENTER...")
