
from pathlib import Path

import psycopg

from src.load_raw_data import get_database_config, load_raw_data
from src.load_analytics_data import load_analytics_data


PROJECT_ROOT = Path(__file__).resolve().parents[1]
NORMALIZATION_SQL = (
    PROJECT_ROOT / "sql" / "04_populate_normalized_tables.sql"
)


def populate_normalized_tables() -> None:
    """Populate genre/tag dictionaries and relationship tables."""
    print("\nSTEP 3: POPULATING GENRES AND TAGS")

    sql_script = NORMALIZATION_SQL.read_text(encoding="utf-8")
    config = get_database_config()

    # The SQL script already contains BEGIN and COMMIT.
    with psycopg.connect(**config, autocommit=True) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql_script, prepare=False)

    print("Genre and tag tables populated successfully.")


def verify_database(expected_count: int) -> None:
    """Verify analytical record counts and populated relationships."""
    print("\nSTEP 4: VERIFYING DATABASE")

    queries = {
        "Games": "SELECT COUNT(*) FROM analytics.steam_items",
        "Genres": "SELECT COUNT(*) FROM analytics.genres",
        "Tags": "SELECT COUNT(*) FROM analytics.tags",
        "Game-genre relationships": (
            "SELECT COUNT(*) FROM analytics.item_genres"
        ),
        "Game-tag relationships": (
            "SELECT COUNT(*) FROM analytics.item_tags"
        ),
    }

    counts = {}
    config = get_database_config()

    with psycopg.connect(**config) as connection:
        with connection.cursor() as cursor:
            for name, query in queries.items():
                cursor.execute(query)
                counts[name] = cursor.fetchone()[0]
                print(f"{name}: {counts[name]}")

    if counts["Games"] != expected_count:
        raise RuntimeError(
            f"Expected {expected_count} games, "
            f"found {counts['Games']}."
        )

    if counts["Game-genre relationships"] == 0:
        raise RuntimeError("Game-genre relationships are empty.")

    if counts["Game-tag relationships"] == 0:
        raise RuntimeError("Game-tag relationships are empty.")

    print("Database verification completed successfully.")

def reset_etl_tables() -> None:
    """Clear dependent and source tables in the correct order."""
    config = get_database_config()

    with psycopg.connect(**config) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                TRUNCATE TABLE
                    analytics.item_genres,
                    analytics.item_tags,
                    analytics.steam_items,
                    staging.steam_games_raw
                RESTART IDENTITY
                """
            )

def run_etl() -> None:
    """Execute the complete Steam market ETL process."""
    print("\nSTEAM MARKET ANALYTICS - ETL")

    print("\nRESETTING ETL TABLES")
    reset_etl_tables()

    print("\nSTEP 1: LOADING RAW DATA")
    raw_count = load_raw_data()

    print("\nSTEP 2: LOADING ANALYTICS DATA")
    analytics_count = load_analytics_data()

    if raw_count != analytics_count:
        raise RuntimeError(
            f"Record count mismatch: "
            f"staging={raw_count}, analytics={analytics_count}."
        )

    populate_normalized_tables()
    verify_database(analytics_count)

    print("\nETL COMPLETED SUCCESSFULLY")


def main() -> None:
    try:
        run_etl()
    except (
        FileNotFoundError,
        ValueError,
        RuntimeError,
        psycopg.Error,
    ) as exc:
        print(f"\nERROR: ETL failed: {exc}")
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
