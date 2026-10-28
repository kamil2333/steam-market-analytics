
import pandas as pd
import psycopg

from src.cleaning import clean_dataset
from src.load_raw_data import get_database_config
from src.validation import build_validation_report


SOURCE_QUERY = """
    SELECT
        raw_id,
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
        tags,
        ingested_at
    FROM staging.steam_games_raw
    ORDER BY raw_id
"""

INSERT_QUERY = """
    INSERT INTO analytics.steam_items (
        source_raw_id,
        title,
        genres,
        description,
        url,
        price_eur,
        original_price_eur,
        discount_percent,
        launch_date_source,
        launch_date_start,
        launch_date_end,
        launch_date_precision,
        review_count,
        general_reviews,
        tags,
        is_source_error
    )
    VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s
    )
"""


def to_database_value(value):
    """Convert Pandas missing values and scalars for PostgreSQL."""
    if pd.isna(value):
        return None

    if isinstance(value, pd.Timestamp):
        return value.date()

    if hasattr(value, "item"):
        return value.item()

    return value


def fetch_source_data() -> pd.DataFrame:
    """Fetch raw source records from PostgreSQL staging."""
    config = get_database_config()

    with psycopg.connect(**config) as connection:
        with connection.cursor() as cursor:
            cursor.execute(SOURCE_QUERY)
            rows = cursor.fetchall()
            columns = [column.name for column in cursor.description]

    if not rows:
        raise ValueError(
            "The staging table is empty. Load source data first."
        )

    return pd.DataFrame(rows, columns=columns)


def prepare_analytics_records(
    source: pd.DataFrame,
    cleaned: pd.DataFrame,
) -> list[tuple]:
    """Map cleaned records to the analytical table structure."""
    records = []

    for raw, clean in zip(
        source.to_dict(orient="records"),
        cleaned.to_dict(orient="records"),
        strict=True,
    ):
        if pd.isna(raw["is_error"]):
            raise ValueError(
                f"Missing is_error flag for raw record {raw['raw_id']}."
            )

        records.append(
            (
                to_database_value(raw["raw_id"]),
                to_database_value(raw["title"]),
                to_database_value(raw["genres"]),
                to_database_value(raw["description"]),
                to_database_value(raw["url"]),
                to_database_value(clean["price_eur"]),
                to_database_value(clean["original_price_eur"]),
                to_database_value(clean["discount_percent"]),
                to_database_value(raw["launch_date"]),
                to_database_value(clean["launch_date_start"]),
                to_database_value(clean["launch_date_end"]),
                to_database_value(clean["launch_date_precision"]),
                to_database_value(clean["review_count"]),
                to_database_value(raw["general_reviews"]),
                to_database_value(raw["tags"]),
                bool(raw["is_error"]),
            )
        )

    return records


def load_analytics_data() -> int:
    """Clean, validate, and transactionally replace analytical records."""
    config = get_database_config()

    print("Reading source records from PostgreSQL...")
    source = fetch_source_data()

    print(f"Source records: {len(source)}")
    print("Cleaning data...")

    cleaned = clean_dataset(source)

    print("Validating data...")
    report = build_validation_report(source, cleaned)

    print("\n=== VALIDATION REPORT ===")
    print(report.to_string(index=False))

    failed_checks = report.loc[report["status"] == "FAIL"]

    if not failed_checks.empty:
        raise ValueError(
            "Analytics loading aborted because validation failed."
        )

    records = prepare_analytics_records(source, cleaned)

    print(f"\nPrepared records: {len(records)}")
    print("Loading records into analytics.steam_items...")

    # The transaction commits on success and rolls back on failure.
    with psycopg.connect(**config) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "TRUNCATE TABLE analytics.steam_items RESTART IDENTITY"
            )

            cursor.executemany(INSERT_QUERY, records)

            cursor.execute(
                "SELECT COUNT(*) FROM analytics.steam_items"
            )
            inserted_count = cursor.fetchone()[0]

            if inserted_count != len(records):
                raise RuntimeError(
                    f"Expected {len(records)} records, "
                    f"found {inserted_count}."
                )

    print(f"Successfully loaded {inserted_count} analytical records.")

    warning_count = int((report["status"] == "WARN").sum())
    print(f"Validation warnings: {warning_count}")

    return inserted_count


def main() -> None:
    try:
        load_analytics_data()
    except (
        ValueError,
        RuntimeError,
        psycopg.Error,
    ) as exc:
        print(f"ERROR: Analytics loading failed: {exc}")
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
