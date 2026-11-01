from pathlib import Path

from app.config.settings import RESULTS_PATH

MAX_INLINE_BYTES = 2 * 1024 * 1024
TEXT_ENCODINGS = ("utf-8", "utf-8-sig", "cp1252", "latin-1")
REPORT_PREFIX = "reports/"


def create_case(username: str) -> Path:
    """Crea la estructura completa de un caso (formato legado v1.2)."""
    case = RESULTS_PATH / username

    (case / "sherlock").mkdir(parents=True, exist_ok=True)
    (case / "maigret").mkdir(parents=True, exist_ok=True)
    (case / "logs").mkdir(parents=True, exist_ok=True)

    return case


def case_files(case_dir: Path) -> list[Path]:
    """Archivos del caso ordenados, con los reportes siempre al principio."""
    files = [path for path in case_dir.rglob("*") if path.is_file()]
    return sorted(
        files,
        key=lambda path: (
            not str(path.relative_to(case_dir)).startswith(REPORT_PREFIX),
            str(path.relative_to(case_dir)),
        ),
    )


def resolve_in_case(case_dir: Path, rel: Path | str) -> Path:
    """Resuelve una ruta y comprueba que no se sale del directorio del caso."""
    base = Path(case_dir).resolve()
    target = (base / rel).resolve()

    if target != base and base not in target.parents:
        raise ValueError(f"ruta fuera del caso: {rel}")
    if not target.is_file():
        raise FileNotFoundError(str(rel))

    return target


def is_binary(data: bytes) -> bool:
    return b"\x00" in data[:2048]


def read_text_safe(path: Path) -> tuple[str, str]:
    """Devuelve (texto, codificación). Lanza ValueError si es binario."""
    data = path.read_bytes()

    if is_binary(data):
        raise ValueError("contenido binario")

    for encoding in TEXT_ENCODINGS:
        try:
            return data.decode(encoding), encoding
        except UnicodeDecodeError:
            continue

    return data.decode("latin-1", errors="replace"), "latin-1"
