from pathlib import Path
from datetime import datetime
import json


def generate_report(case_path: Path):

    info_file = case_path / "info.json"

    # Si no existe el archivo de información del caso, no hacemos nada.
    if not info_file.exists():
        return

    # Cargar la información del caso.
    with open(info_file, "r", encoding="utf8") as f:
        info = json.load(f)

    # Directorio donde se guardarán los reportes.
    report_dir = case_path / "reports"
    report_dir.mkdir(exist_ok=True)

    # Generar el resumen del caso y guardarlo como JSON.
    summary = {
        "case_id": info["case_id"],
        "target": info["target"],
        "type": info["type"],
        "status": info["status"],
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(report_dir / "summary.json", "w", encoding="utf8") as f:
        json.dump(summary, f, indent=4)

    # ----------------------------------------------------------------------
    # Preparar la sección de Evidencia.
    # ----------------------------------------------------------------------
    # Se busca el archivo `sherlock.txt` dentro del subdirectorio `users`
    # del caso. Si existe, su contenido se inserta dentro de un bloque de
    # código Markdown. Si no, se muestra un mensaje informativo.
    sherlock_path = case_path / "users" / "sherlock.txt"
    if sherlock_path.exists():
        try:
            sherlock_content = sherlock_path.read_text(encoding="utf8")
            evidence_section = (
                "### Sherlock Results\n\n"
                "```text\n"
                f"{sherlock_content.rstrip()}\n"
                "```\n"
            )
        except OSError:
            # En caso de error al leer el archivo, se indica que no se pudo
            # obtener la información.
            evidence_section = "No se pudo leer el archivo de resultados de Sherlock.\n"
    else:
        evidence_section = "No hay resultados de Sherlock para este caso.\n"

    # ----------------------------------------------------------------------
    # Construir el reporte Markdown completo.
    # ----------------------------------------------------------------------
    report = f"""# OSINT REPORT

Case ID: {info['case_id']}

Target: {info['target']}

Type: {info['type']}

Status: {info['status']}

Created:
{info['created']}

Generated:
{summary['generated']}

## Evidence

users/
emails/
domains/
logs/
metadata/
evidence/

{evidence_section}
## End of report
"""

    # Guardar el reporte en formato Markdown.
    with open(report_dir / "report.md", "w", encoding="utf8") as f:
        f.write(report)
