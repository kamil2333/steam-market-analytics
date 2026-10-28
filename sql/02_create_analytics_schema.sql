
CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.steam_items (
    item_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    source_raw_id BIGINT NOT NULL UNIQUE
        REFERENCES staging.steam_games_raw(raw_id),

    title TEXT NOT NULL,
    genres TEXT,
    description TEXT,
    url TEXT,

    price_eur NUMERIC(10, 2)
        CHECK (price_eur IS NULL OR price_eur >= 0),

    original_price_eur NUMERIC(10, 2)
        CHECK (original_price_eur IS NULL OR original_price_eur >= 0),

    discount_percent NUMERIC(5, 2)
        CHECK (
            discount_percent IS NULL
            OR discount_percent BETWEEN 0 AND 100
        ),

    launch_date_source TEXT,

    launch_date_start DATE,
    launch_date_end DATE,

    launch_date_precision TEXT NOT NULL
        CHECK (
            launch_date_precision IN (
                'day',
                'month',
                'quarter',
                'year',
                'missing',
                'coming_soon'
            )
        ),

    review_count BIGINT
        CHECK (review_count IS NULL OR review_count >= 0),

    general_reviews TEXT,
    tags TEXT,

    is_source_error BOOLEAN NOT NULL,

    loaded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT valid_launch_date_interval
        CHECK (
            launch_date_start IS NULL
            OR launch_date_end IS NULL
            OR launch_date_start <= launch_date_end
        ),

    CONSTRAINT valid_launch_date_precision
        CHECK (
            (
                launch_date_precision = 'day'
                AND launch_date_start IS NOT NULL
                AND launch_date_end IS NOT NULL
                AND launch_date_start = launch_date_end
            )
            OR (
                launch_date_precision IN ('month', 'quarter', 'year')
                AND launch_date_start IS NOT NULL
                AND launch_date_end IS NOT NULL
            )
            OR (
                launch_date_precision IN ('missing', 'coming_soon')
                AND launch_date_start IS NULL
                AND launch_date_end IS NULL
            )
        )
);

COMMENT ON TABLE analytics.steam_items IS
    'Typed analytical representation of Steam store items.';

COMMENT ON COLUMN analytics.steam_items.source_raw_id IS
    'Reference to the corresponding source record in the staging schema.';

COMMENT ON COLUMN analytics.steam_items.price_eur IS
    'Current listed price in euros. NULL means that the price is unknown.';

COMMENT ON COLUMN analytics.steam_items.review_count IS
    'Number of user reviews, not the number of sales or players.';

COMMENT ON COLUMN analytics.steam_items.launch_date_precision IS
    'Precision of the source launch date: day, month, quarter, year, missing, or coming_soon.';
