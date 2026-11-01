from datetime import datetime
from pathlib import Path


def log(case_path: Path, level: str, message: str):
    log_dir = Path(case_path) / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    safe = " ".join(str(message).split())

    with open(log_dir / "activity.log", "a", encoding="utf-8") as fh:
        fh.write(f"{now} | {level.upper():<7} | {safe}\n")
