import csv
from pathlib import Path


def clean_role(role: str) -> str:
    # Remove extra spaces and standardize capitalization
    # so similar role labels are grouped more consistently
    return role.strip().title()


def clean_experience(value: str) -> str:
    # Remove extra spaces from the experience value
    value = value.strip()

    # Convert known word values into digits so they don’t cause errors
    # when the script tries to turn them into numbers (e.g., "fifteen" -> 15)
    word_to_number = {
        "zero": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
        "ten": "10",
        "eleven": "11",
        "twelve": "12",
        "thirteen": "13",
        "fourteen": "14",
        "fifteen": "15",
    }

    return word_to_number.get(value.lower(), value)


def clean_score(value: str) -> str:
    # Remove extra spaces from the satisfaction score
    return value.strip()


def clean_week3_survey(input_path: Path, output_path: Path) -> tuple[int, int]:
    # Open the messy input CSV and prepare to read each row as a dictionary, clean the key fields in each row
    # and prepare the cleaned rows to be written to a new CSV file
    with open(input_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if reader.fieldnames is None:
            raise ValueError("CSV appears to be missing a header row.")

        required_headers = {
            "participant_name",
            "role",
            "experience_years",
            "satisfaction_score",
        }
        missing = required_headers - set(reader.fieldnames)
        if missing:
            missing_list = ", ".join(sorted(missing))
            raise ValueError(f"Missing required column(s): {missing_list}")

        fieldnames = list(reader.fieldnames)

        rows_read = 0
        cleaned_rows = []

        # Go through each row in the messy CSV and clean the values we care about
        for row in reader:
            rows_read += 1

            row["participant_name"] = (row.get("participant_name") or "").strip()
            row["role"] = clean_role(row.get("role") or "")
            row["experience_years"] = clean_experience(row.get("experience_years") or "")
            row["satisfaction_score"] = clean_score(row.get("satisfaction_score") or "")

            # Add the cleaned row to the list that will be written out later
            cleaned_rows.append(row)

    # Write all cleaned rows into a new output CSV file
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    return rows_read, len(cleaned_rows)


def main() -> None:
    # Build file paths relative to this script so it works from the project folder
    project_dir = Path(__file__).resolve().parent
    input_path = project_dir / "week3_survey_messy.csv"
    output_path = project_dir / "week3_survey_cleaned.csv"

    if not input_path.exists():
        raise SystemExit(
            "Could not find `week3_survey_messy.csv` in this folder.\n"
            "Put the CSV next to this script, then run:\n"
            "  python3 clean_week3_survey.py"
        )

    rows_read, rows_written = clean_week3_survey(
        input_path=input_path,
        output_path=output_path,
    )

    print("Cleaning complete")
    print(f"Input file: {input_path.name}")
    print(f"Output file: {output_path.name}")
    print(f"Rows read: {rows_read}")
    print(f"Rows written: {rows_written}")


if __name__ == "__main__":
    main()
