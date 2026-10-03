from pathlib import Path
from datetime import datetime


def log(case_path: Path, level: str, message: str):

    log_dir = case_path / "logs"
    log_dir.mkdir(exist_ok=True)

    logfile = log_dir / "activity.log"

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    line = f"{now} | {level.upper():<7} | {message}\n"

    with open(logfile, "a", encoding="utf-8") as f:
        f.write(line)
