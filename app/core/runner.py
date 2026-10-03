import json
import subprocess
import time
from pathlib import Path

from core.logger import log


def run_tool(tool_name: str,
             command: list,
             output_dir: Path,
             case_path: Path,
             timeout: int = 300):

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    start = time.time()

    log(case_path, "INFO", f"{tool_name} iniciado")

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        elapsed = round(time.time() - start, 2)

        # Guardar stdout
        (output_dir / "stdout.txt").write_text(
            result.stdout,
            encoding="utf-8",
            errors="ignore"
        )

        # Guardar stderr
        (output_dir / "stderr.txt").write_text(
            result.stderr,
            encoding="utf-8",
            errors="ignore"
        )

        # Guardar metadata
        metadata = {
            "tool": tool_name,
            "command": command,
            "return_code": result.returncode,
            "duration": elapsed,
            "success": result.returncode == 0
        }

        (output_dir / "execution.json").write_text(
            json.dumps(metadata, indent=4),
            encoding="utf-8"
        )

        if result.returncode == 0:

            log(
                case_path,
                "SUCCESS",
                f"{tool_name} finalizado ({elapsed}s)"
            )

        else:

            log(
                case_path,
                "ERROR",
                f"{tool_name} finalizado con código {result.returncode}"
            )

        return result

    except subprocess.TimeoutExpired:

        log(
            case_path,
            "ERROR",
            f"{tool_name} excedió el tiempo máximo ({timeout}s)"
        )

        return None

    except FileNotFoundError:

        log(
            case_path,
            "ERROR",
            f"{tool_name} no está instalado"
        )

        return None

    except PermissionError:

        log(
            case_path,
            "ERROR",
            f"Sin permisos para ejecutar {tool_name}"
        )

        return None

    except Exception as e:

        log(
            case_path,
            "ERROR",
            str(e)
        )

        return None
