import csv
from collections import Counter
from pathlib import Path


def normalize_role(role: str) -> str:
    """Normalize a role so similar values count together."""
    return " ".join(role.strip().lower().split())


def count_roles(csv_path: Path) -> tuple[Counter[str], int, int]:
    """Return role counts, rows read, and rows skipped."""
    role_counts: Counter[str] = Counter()
    rows_read = 0
    rows_skipped = 0

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if reader.fieldnames is None:
            raise ValueError("CSV appears to be missing a header row.")

        required_headers = {"participant_id", "role", "response"}
        missing = required_headers - set(reader.fieldnames)
        if missing:
            missing_list = ", ".join(sorted(missing))
            raise ValueError(f"Missing required column(s): {missing_list}")

        for row in reader:
            rows_read += 1
            normalized_role = normalize_role(row.get("role", ""))

            if not normalized_role:
                rows_skipped += 1
                continue

            role_counts[normalized_role] += 1

    return role_counts, rows_read, rows_skipped


def main() -> None:
    project_dir = Path(__file__).resolve().parent
    csv_path = project_dir / "responses.csv"

    if not csv_path.exists():
        raise SystemExit(
            "Could not find `responses.csv` in this folder.\n"
            "Put `responses.csv` next to this script, then run:\n"
            "  python3 count_roles.py"
        )

    role_counts, rows_read, rows_skipped = count_roles(csv_path)

    print(f"{'Role':<28} {'Count':<5}")
    print("-" * 34)

    for role, count in sorted(role_counts.items(), key=lambda item: (-item[1], item[0])):
        print(f"{role:<28} {count:<5}")

    print()
    print("── Summary ─────────────────────────────────")
    print(f"  Rows read      : {rows_read}")
    print(f"  Roles counted  : {sum(role_counts.values())}")
    print(f"  Rows skipped   : {rows_skipped}")
    print(f"  Unique roles   : {len(role_counts)}")


if __name__ == "__main__":
    main()
