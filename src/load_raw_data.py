
import os
from pathlib import Path

import pandas as pd
import psycopg
from dotenv import load_dotenv

from src.profile_data import load_dataset


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "steam-games.csv"
ENV_PATH = PROJECT_ROOT / ".env"

RAW_COLUMNS = (
    "title",
    "genres",
    "description",
    "url",
    "price",
    "discount",
    "original_price",
    "launch_date",
    "is_error",
    "reviews",
    "general_reviews",
    "tags",
)

INSERT_SQL = """
    INSERT INTO staging.steam_games_raw (
        title,
        genres,
        description,
        url,
        price,
        discount,
        original_price,
        launch_date,
        is_error,
        reviews,
        general_reviews,
        tags
    )
    VALUES (
        %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s
    )
"""


def get_database_config() -> dict:
    """Load PostgreSQL connection settings from environment variables."""
    load_dotenv(ENV_PATH, override=True)

    required_variables = (
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
    )

    missing_variables = [
        name for name in required_variables
        if not os.getenv(name)
    ]

    if missing_variables:
        raise RuntimeError(
            "Missing database configuration: "
            + ", ".join(missing_variables)
            + ". Check your .env file."
        )

    return {
        "host": os.environ["DB_HOST"],
        "port": int(os.environ["DB_PORT"]),
        "dbname": os.environ["DB_NAME"],
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
    }


def prepare_records(df: pd.DataFrame) -> list[tuple]:
    """Validate source columns and convert missing values to SQL NULL."""
    missing_columns = set(RAW_COLUMNS) - set(df.columns)

    if missing_columns:
        raise ValueError(
            "Source CSV is missing columns: "
            + ", ".join(sorted(missing_columns))
        )

    source = df.loc[:, list(RAW_COLUMNS)]
    records = []

    for row in source.itertuples(index=False, name=None):
        record = tuple(
            None
            if pd.isna(value)
            else value.item()
            if hasattr(value, "item")
            else value
            for value in row
        )
        records.append(record)

    return records


def load_raw_data() -> int:
    """Replace staging data with the current source CSV in one transaction."""
    source = load_dataset(DATA_PATH)
    records = prepare_records(source)

    config = get_database_config()

    print(f"Source records: {len(records)}")
    print("Connecting to PostgreSQL...")

    # A connection context commits on success and rolls back on failure.
    with psycopg.connect(**config) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "TRUNCATE TABLE staging.steam_games_raw RESTART IDENTITY"
            )

            cursor.executemany(INSERT_SQL, records)

            cursor.execute(
                "SELECT COUNT(*) FROM staging.steam_games_raw"
            )
            inserted_count = cursor.fetchone()[0]

            if inserted_count != len(records):
                raise RuntimeError(
                    f"Expected {len(records)} records, "
                    f"but found {inserted_count}."
                )

    print(f"Successfully loaded {inserted_count} records.")
    return inserted_count


def main() -> None:
    try:
        load_raw_data()
    except (
        FileNotFoundError,
        RuntimeError,
        ValueError,
        psycopg.Error,
    ) as exc:
        print(f"ERROR: Import failed: {exc}")
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
