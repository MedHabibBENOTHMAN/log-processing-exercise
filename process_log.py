import json
import sys
from collections.abc import Iterator
from pathlib import Path


def compute_new_data(line: str, line_number: int) -> str:
    stripped = line.rstrip("\r\n")

    if line_number % 5 == 0:
        return "Multiple of 5"
    if "$" in stripped:
        return stripped.replace(" ", "_")
    if stripped.endswith("."):
        return stripped
    if stripped.startswith("{"):
        try:
            data = json.loads(stripped)
        except json.JSONDecodeError:
            return "Nothing to display"
        data["even"] = line_number % 2 == 0
        return json.dumps(data, ensure_ascii=False)
    return "Nothing to display"


def process(path: Path) -> Iterator[str]:
    with path.open(encoding="utf-8") as f:
        for line_number, line in enumerate(f):
            yield f"{line_number} : {compute_new_data(line, line_number)}"


def main(path: Path) -> None:
    for output_line in process(path):
        print(output_line)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <path_to_log_file>", file=sys.stderr)
        sys.exit(1)
    main(Path(sys.argv[1]))
