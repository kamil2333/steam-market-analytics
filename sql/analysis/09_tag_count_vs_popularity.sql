-- Relationship between number of tags and game popularity

WITH game_tag_counts AS (
    SELECT
        si.item_id,
        si.review_count,
        COUNT(it.tag_id) AS tag_count
    FROM analytics.steam_items si
    LEFT JOIN analytics.item_tags it
        ON si.item_id = it.item_id
    GROUP BY
        si.item_id,
        si.review_count
)
SELECT
    tag_count,
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
FROM game_tag_counts
GROUP BY tag_count
ORDER BY tag_count;
