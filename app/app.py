from rich.console import Console

from ui.dashboard import show_dashboard
from ui.menu import show_menu

console = Console()


class OSINTApplication:

    def run(self):

        while True:

            show_dashboard()

            option = show_menu()

            if option == "0":
                console.print("\nHasta luego.\n")
                break

            elif option == "1":
                pass

            elif option == "2":
                from ui.users import menu
                menu()

            elif option == "3":
                from ui.emails import menu
                menu()

            elif option == "4":
                from ui.domains import menu
                menu()

            elif option == "5":
                from ui.tools import menu
                menu()

            elif option == "6":
                from ui.results import menu
                menu()

            elif option == "7":
                from ui.reports import menu
                menu()

            else:
                console.print("\nOpción inválida.\n")
                input("ENTER...")
