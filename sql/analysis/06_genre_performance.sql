-- Genre performance analysis

SELECT
    g.name AS genre,
    COUNT(*) AS games_count,

    COUNT(si.price_eur) AS games_with_price,
    ROUND(AVG(si.price_eur), 2) AS average_price,
    ROUND(
        PERCENTILE_CONT(0.5)
        WITHIN GROUP (ORDER BY si.price_eur)::numeric,
        2
    ) AS median_price,

    COUNT(si.review_count) AS games_with_reviews,
    ROUND(AVG(si.review_count), 0) AS average_review_count,
    SUM(si.review_count) AS total_reviews

FROM analytics.genres g

JOIN analytics.item_genres ig
    ON g.genre_id = ig.genre_id

JOIN analytics.steam_items si
    ON ig.item_id = si.item_id

GROUP BY
    g.genre_id,
    g.name

ORDER BY
    total_reviews DESC NULLS LAST;


-- Genre ranking with review coverage

WITH genre_statistics AS (
    SELECT
        g.genre_id,
        g.name AS genre,

        COUNT(DISTINCT si.item_id) AS total_games,

        COUNT(si.review_count) AS games_with_reviews,

        ROUND(
            COUNT(si.review_count)::numeric
            / NULLIF(COUNT(DISTINCT si.item_id), 0) * 100,
            2
        ) AS review_coverage_percent,

        ROUND(AVG(si.review_count), 0) AS average_reviews,

        PERCENTILE_CONT(0.5)
            WITHIN GROUP (ORDER BY si.review_count)
            AS median_reviews

    FROM analytics.genres g

    JOIN analytics.item_genres ig
        ON g.genre_id = ig.genre_id

    JOIN analytics.steam_items si
        ON ig.item_id = si.item_id

    GROUP BY
        g.genre_id,
        g.name
),

ranked_genres AS (
    SELECT
        *,
        RANK() OVER (
            ORDER BY median_reviews DESC NULLS LAST
        ) AS genre_rank

    FROM genre_statistics
)

SELECT *
FROM ranked_genres
ORDER BY genre_rank
LIMIT 10;
