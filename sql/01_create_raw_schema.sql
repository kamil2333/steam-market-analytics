
--Create a schema for source data.
CREATE SCHEMA IF NOT EXISTS staging;

--Store source values without cleaning or normalization.
CREATE TABLE IF NOT EXISTS staging.steam_games_raw (
    raw_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    title TEXT,
    genres TEXT,
    description TEXT,
    url TEXT,
    price TEXT,
    discount TEXT,
    original_price TEXT,
    launch_date TEXT,
    is_error SMALLINT,
    reviews TEXT,
    general_reviews TEXT,
    tags TEXT,

    ingested_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON SCHEMA staging IS
    'Schema for source data before cleaning and transformation.';

COMMENT ON TABLE staging.steam_games_raw IS
    'Source Steam game records, preserving original values.';

COMMENT ON COLUMN staging.steam_games_raw.raw_id IS
    'Technical identifier assigned during database ingestion.';

COMMENT ON COLUMN staging.steam_games_raw.ingested_at IS
    'Timestamp when the record was inserted into the database.';
