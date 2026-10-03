from pathlib import Path
from datetime import datetime


def log(case_path, message):

    logfile = Path(case_path) / "logs" / "scan.log"

    with open(logfile, "a", encoding="utf8") as f:

        hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        f.write(f"[{hora}] {message}\n")
