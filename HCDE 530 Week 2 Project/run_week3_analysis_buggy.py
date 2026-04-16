from pathlib import Path
import runpy


def main() -> None:
    week2_dir = Path(__file__).resolve().parent
    repo_root = week2_dir.parent
    target = repo_root / "HCDE 530 Week 3 Project" / "week3_analysis_buggy.py"

    if not target.exists():
        raise SystemExit(f"Could not find: {target}")

    runpy.run_path(str(target), run_name="__main__")


if __name__ == "__main__":
    main()

