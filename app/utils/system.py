import os
import platform
import shutil
import subprocess


def get_os():
    """Sistema operativo."""
    return platform.system()


def get_hostname():
    """Nombre del equipo."""
    return platform.node()


def get_python_version():
    """Versión de Python."""
    return platform.python_version()


def get_git_version():
    """Versión de Git."""
    try:
        salida = subprocess.check_output(
            ["git", "--version"],
            text=True
        )
        return salida.replace("git version", "").strip()
    except Exception:
        return "No instalado"


def is_tool_installed(tool):
    """Comprueba si una herramienta existe."""
    return shutil.which(tool) is not None


def get_disk_usage():
    """Espacio del disco."""
    total, used, free = shutil.disk_usage("/")

    return {
        "total": round(total / (1024 ** 3), 1),
        "used": round(used / (1024 ** 3), 1),
        "free": round(free / (1024 ** 3), 1),
    }


def count_directories(path):
    """Cuenta directorios."""
    if not os.path.exists(path):
        return 0

    return len(
        [
            item
            for item in os.listdir(path)
            if os.path.isdir(os.path.join(path, item))
        ]
    )
