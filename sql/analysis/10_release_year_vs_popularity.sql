-- Game popularity by release year

SELECT
    EXTRACT(YEAR FROM launch_date_start)::int AS release_year,
    COUNT(*) AS total_games,
    COUNT(review_count) AS games_with_reviews,

    ROUND(
        COUNT(review_count)::numeric
        / NULLIF(COUNT(*), 0) * 100,
        2
    ) AS review_coverage_percent,

    ROUND(AVG(review_count), 0) AS average_reviews,

    PERCENTILE_CONT(0.5)
        WITHIN GROUP (ORDER BY review_count) AS median_reviews,

    SUM(review_count) AS total_reviews

FROM analytics.steam_items

WHERE launch_date_precision IN ('day', 'month', 'quarter', 'year')
  AND launch_date_start IS NOT NULL
  AND launch_date_start < DATE '2026-01-01'

GROUP BY release_year

ORDER BY release_year;
