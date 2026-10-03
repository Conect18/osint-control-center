from pathlib import Path

from core.runner import run_tool


def run(domain, output_dir, case):

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output = output_dir / "subdomains.txt"

    result = run_tool(
        "Sublist3r",
        [
            "sublist3r",
            "-d",
            domain,
            "-o",
            str(output)
        ],
        output_dir,
        case
    )

    return result is not None and result.returncode == 0
