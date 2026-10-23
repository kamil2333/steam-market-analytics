
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "steam-games.csv"

ERROR_METADATA_COLUMNS = (
    "url",
    "tags",
    "price",
    "description",
    "reviews",
)


def load_dataset(path: Path) -> pd.DataFrame:
    """Load a CSV dataset from the specified path."""
    if not path.is_file():
        raise FileNotFoundError(
            f"Dataset not found: {path.resolve()}"
        )

    return pd.read_csv(path)


def build_column_profile(df: pd.DataFrame) -> pd.DataFrame:
    """Build a data quality profile for every column."""
    profile = pd.DataFrame(
        {
            "column": df.columns,
            "dtype": [str(dtype) for dtype in df.dtypes],
            "non_null_count": df.notna().sum().to_numpy(),
            "missing_count": df.isna().sum().to_numpy(),
            "missing_percentage": (
                df.isna().mean().mul(100).round(2).to_numpy()
            ),
            "unique_count": df.nunique(dropna=True).to_numpy(),
        }
    )

    return (
        profile.sort_values(
            by=["missing_percentage", "column"],
            ascending=[False, True],
        )
        .reset_index(drop=True)
    )


def build_error_flag_profile(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize missing metadata for each error flag value."""
    required_columns = {
        "title",
        "is_error",
        *ERROR_METADATA_COLUMNS,
    }
    missing_columns = sorted(required_columns - set(df.columns))

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {', '.join(missing_columns)}"
        )

    aggregations = {
        "record_count": ("title", "size"),
    }

    for column in ERROR_METADATA_COLUMNS:
        aggregations[f"missing_{column}"] = (
            column,
            lambda values: int(values.isna().sum()),
        )

    return (
        df.groupby("is_error", dropna=False)
        .agg(**aggregations)
        .reset_index()
        .sort_values("is_error")
        .reset_index(drop=True)
    )


def print_dataset_summary(df: pd.DataFrame) -> None:
    """Print general dataset statistics."""
    print("\nDATASET SUMMARY")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print(f"Exact duplicate rows: {df.duplicated().sum()}")

    for column in ("title", "url"):
        if column in df.columns:
            values = df[column].dropna()
            duplicate_count = int(values.duplicated().sum())
            print(
                f"Repeated non-null values in '{column}': "
                f"{duplicate_count}"
            )

    if "is_error" in df.columns:
        print("\nERROR FLAG DISTRIBUTION")
        print(
            df["is_error"]
            .value_counts(dropna=False)
            .sort_index()
            .to_string()
        )


def main() -> None:
    df = load_dataset(DATA_PATH)

    print_dataset_summary(df)

    print("\nCOLUMN DATA QUALITY PROFILE")
    print(build_column_profile(df).to_string(index=False))

    print("\nMISSING FIELDS BY ERROR FLAG")
    print(build_error_flag_profile(df).to_string(index=False))

    print("\nProfiling completed successfully.")


if __name__ == "__main__":
    main()
