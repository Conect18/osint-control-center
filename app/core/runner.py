"""Ejecución endurecida de herramientas externas.

Contrato: run_tool NUNCA lanza. Siempre devuelve un ToolResult con estado
explícito. OK solo se asigna si el proceso terminó bien Y produjo salida
parseable; un exit 0 sin resultados es EMPTY, no éxito.
"""

import json
import os
import signal
import subprocess
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from shutil import which

from app.core.logger import log
from app.core.normalize import slugify, strip_ansi

DEFAULT_TIMEOUT = 300
MAX_CAPTURE = 8 * 1024 * 1024
TRUNCATED = "\n...[salida truncada]\n"


class Status(str, Enum):
    OK = "ok"
    EMPTY = "empty"
    ERROR = "error"
    TIMEOUT = "timeout"
    MISSING = "missing"
    DENIED = "denied"


@dataclass
class ToolResult:
    tool: str
    status: Status
    returncode: int | None = None
    duration: float = 0.0
    command: list = field(default_factory=list)
    output_dir: str = ""
    message: str = ""
    findings: int = 0

    @property
    def ok(self):
        return self.status is Status.OK

    def __bool__(self):
        return self.ok

    def save(self):
        path = Path(self.output_dir)
        path.mkdir(parents=True, exist_ok=True)
        (path / "execution.json").write_text(
            json.dumps(self.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def to_dict(self):
        return {
            "tool": self.tool,
            "status": self.status.value,
            "returncode": self.returncode,
            "duration": self.duration,
            "command": self.command,
            "output_dir": self.output_dir,
            "message": self.message,
            "findings": self.findings,
        }


def _safe_log(case_path, level, message):
    try:
        log(case_path, level, message)
    except Exception:
        pass


def _cap(text):
    text = strip_ansi(text or "")
    if len(text) > MAX_CAPTURE:
        return text[:MAX_CAPTURE] + TRUNCATED
    return text


def _build_env():
    env = os.environ.copy()
    env.update({"PYTHONUNBUFFERED": "1", "NO_COLOR": "1", "TERM": "dumb", "CLICOLOR": "0"})
    return env


def resolve_binary(name):
    """Ruta absoluta del ejecutable o None."""
    if os.sep in name:
        path = Path(name).expanduser()
        return str(path) if path.is_file() and os.access(path, os.X_OK) else None
    return which(name)


def run_tool(tool_name: str,
             command: list,
             output_dir: Path,
             case_path: Path,
             timeout: int = DEFAULT_TIMEOUT,
             binary: str | None = None,
             success_codes=(0,),
             env_extra: dict | None = None) -> ToolResult:
    """Ejecuta una herramienta y persiste su evidencia de forma aislada."""

    out_dir = Path(output_dir) / slugify(tool_name)
    out_dir.mkdir(parents=True, exist_ok=True)

    command = [str(part) for part in command]
    exe = binary or command[0]
    resolved = resolve_binary(exe)

    result = ToolResult(
        tool=tool_name,
        status=Status.MISSING,
        command=[exe, *command[1:]],
        output_dir=str(out_dir),
    )

    if resolved is None:
        result.message = f"{tool_name} no está instalado"
        _safe_log(case_path, "ERROR", result.message)
        _persist(result)
        return result

    command[0] = resolved
    result.command = command
    result.status = Status.ERROR

    env = _build_env()
    if env_extra:
        env.update(env_extra)

    _safe_log(case_path, "INFO", f"{tool_name} iniciado")
    start = time.time()
    stdout = stderr = ""
    timed_out = False

    try:
        proc = subprocess.Popen(
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            start_new_session=True,
        )
    except PermissionError:
        result.status = Status.DENIED
        result.message = f"sin permisos para ejecutar {tool_name}"
        _safe_log(case_path, "ERROR", result.message)
        _persist(result)
        return result
    except OSError as exc:
        result.message = f"no se pudo lanzar {tool_name}: {exc}"
        _safe_log(case_path, "ERROR", result.message)
        _persist(result)
        return result

    try:
        stdout, stderr = proc.communicate(timeout=timeout)
        result.returncode = proc.returncode
    except subprocess.TimeoutExpired:
        timed_out = True
        _terminate(proc)
        try:
            stdout, stderr = proc.communicate(timeout=15)
        except subprocess.TimeoutExpired:
            stdout, stderr = "", ""
        result.returncode = proc.returncode

    result.duration = round(time.time() - start, 2)

    (out_dir / "stdout.txt").write_text(_cap(stdout), encoding="utf-8")
    (out_dir / "stderr.txt").write_text(_cap(stderr), encoding="utf-8")

    if timed_out:
        result.status = Status.TIMEOUT
        result.message = f"{tool_name} excedió {timeout}s"
    elif result.returncode not in success_codes:
        result.status = Status.ERROR
        result.message = f"{tool_name} terminó con código {result.returncode}"
    elif not (stdout or "").strip() and not (stderr or "").strip():
        result.status = Status.EMPTY
        result.message = f"{tool_name} no devolvió salida"
    else:
        result.status = Status.OK
        result.message = f"{tool_name} finalizado ({result.duration}s)"

    level = "SUCCESS" if result.ok else "ERROR"
    _safe_log(case_path, level, result.message)
    _persist(result)
    return result


def _terminate(proc):
    """Mata el grupo de procesos completo: SIGTERM, espera, SIGKILL."""
    for sig, wait in ((signal.SIGTERM, 5), (signal.SIGKILL, 5)):
        try:
            os.killpg(os.getpgid(proc.pid), sig)
        except (ProcessLookupError, PermissionError):
            return
        try:
            proc.wait(timeout=wait)
            return
        except subprocess.TimeoutExpired:
            continue


def _persist(result: ToolResult):
    result.save()
