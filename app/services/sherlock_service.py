from pathlib import Path

from core.runner import run_tool


def run(username, output_dir, case):

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output = output_dir / "sherlock.txt"

    result = run_tool(
        "Sherlock",
        [
            "sherlock",
            username,
            "--output",
            str(output)
        ],
        output_dir,
        case
    )

    return result is not None and result.returncode == 0
