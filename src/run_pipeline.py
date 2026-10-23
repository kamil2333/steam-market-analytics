
import argparse
from pathlib import Path

import pandas as pd

from src.cleaning import clean_dataset
from src.profile_data import load_dataset
from src.validation import build_validation_report


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_INPUT_PATH = (
    PROJECT_ROOT / "data" / "raw" / "steam-games.csv"
)
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"


def run_pipeline(
    input_path: Path,
    output_dir: Path,
) -> pd.DataFrame:
    """Load, clean, validate, and export a dataset."""
    print(f"Loading source data: {input_path}")

    source = load_dataset(input_path)

    print("Cleaning data...")
    cleaned = clean_dataset(source)

    print("Validating cleaned data...")
    report = build_validation_report(source, cleaned)

    output_dir.mkdir(parents=True, exist_ok=True)

    cleaned_path = output_dir / "steam-games-cleaned.csv"
    report_path = output_dir / "validation-report.csv"

    # Always save the validation report, including failed checks.
    report.to_csv(report_path, index=False, encoding="utf-8")

    failed_checks = report.loc[report["status"] == "FAIL"]

    if not failed_checks.empty:
        # Remove a previous output so it cannot be mistaken for
        # the result of this unsuccessful pipeline run.
        cleaned_path.unlink(missing_ok=True)
        return report

    cleaned.to_csv(
        cleaned_path,
        index=False,
        encoding="utf-8",
    )

    print(f"Cleaned dataset saved to: {cleaned_path}")
    print(f"Validation report saved to: {report_path}")

    return report


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Run the Steam games data cleaning and validation pipeline."
        )
    )

    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT_PATH,
        help="Path to the source CSV file.",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory where the outputs will be saved.",
    )

    args = parser.parse_args()

    try:
        report = run_pipeline(args.input, args.output_dir)
    except (FileNotFoundError, ValueError, pd.errors.ParserError) as exc:
        print(f"\nERROR: Pipeline stopped: {exc}")
        raise SystemExit(1) from exc

    print("\nVALIDATION REPORT")
    print(report.to_string(index=False))

    failed_checks = report.loc[report["status"] == "FAIL"]
    warning_checks = report.loc[report["status"] == "WARN"]

    print("\n=== PIPELINE SUMMARY ===")
    print(f"Checks passed: {(report['status'] == 'PASS').sum()}")
    print(f"Warnings: {len(warning_checks)}")
    print(f"Failed checks: {len(failed_checks)}")

    if not failed_checks.empty:
        print("Pipeline failed validation. Cleaned data was not exported.")
        raise SystemExit(1)

    if not warning_checks.empty:
        print(
            "Pipeline completed with warnings. "
            "Review the validation report before analysis."
        )
    else:
        print("Pipeline completed successfully without warnings.")


if __name__ == "__main__":
    main()
