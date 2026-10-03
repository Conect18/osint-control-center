from pathlib import Path

from core.runner import run_tool


def run(username, output_dir, case):

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    result = run_tool(
        "Maigret",
        [
            "maigret",
            username,
            "--folderoutput",
            str(output_dir)
        ],
        output_dir,
        case
    )

    return result is not None and result.returncode == 0
