"""
Clean a responses CSV file.

Reads `responses.csv`, removes rows where `name` is blank, uppercases the `role`
column, and writes the cleaned rows to `responses_cleaned.csv`.
"""

import csv
from pathlib import Path


def clean_responses(input_path: Path, output_path: Path) -> tuple[int, int]:
    """Return (rows_read, rows_written) after cleaning."""
    with open(input_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if reader.fieldnames is None:
            raise ValueError("CSV appears to be missing a header row.")

        required_headers = {"name", "role"}
        missing = required_headers - set(reader.fieldnames)
        if missing:
            missing_list = ", ".join(sorted(missing))
            raise ValueError(f"Missing required column(s): {missing_list}")

        fieldnames = list(reader.fieldnames)

        rows_read = 0
        cleaned_rows: list[dict[str, str]] = []

        for row in reader:
            rows_read += 1

            name = (row.get("name") or "").strip()
            if not name:
                continue

            row["name"] = name
            row["role"] = (row.get("role") or "").upper()
            cleaned_rows.append(row)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    return rows_read, len(cleaned_rows)


def main() -> None:
    project_dir = Path(__file__).resolve().parent
    input_path = project_dir / "responses.csv"
    output_path = project_dir / "responses_cleaned.csv"

    if not input_path.exists():
        raise SystemExit(
            "Could not find `responses.csv` in this folder.\n"
            "Put `responses.csv` next to this script, then run:\n"
            "  python3 clean_responses.py"
        )

    rows_read, rows_written = clean_responses(input_path=input_path, output_path=output_path)

    print("── Cleaning complete ───────────────────────")
    print(f"  Input file    : {input_path.name}")
    print(f"  Output file   : {output_path.name}")
    print(f"  Rows read     : {rows_read}")
    print(f"  Rows written  : {rows_written}")


if __name__ == "__main__":
    main()

