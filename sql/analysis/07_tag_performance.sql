
-- Tag performance analysis
-- Only tags assigned to at least 10 games

SELECT
    t.name AS tag,

    COUNT(DISTINCT si.item_id) AS games_count,

    COUNT(si.review_count) AS games_with_reviews,

    ROUND(
        COUNT(si.review_count)::numeric
        / NULLIF(COUNT(DISTINCT si.item_id), 0) * 100,
        2
    ) AS review_coverage_percent,

    ROUND(AVG(si.review_count), 0) AS average_reviews,

    PERCENTILE_CONT(0.5)
        WITHIN GROUP (ORDER BY si.review_count)
        AS median_reviews,

    SUM(si.review_count) AS total_reviews

FROM analytics.tags t

JOIN analytics.item_tags it
    ON t.tag_id = it.tag_id

JOIN analytics.steam_items si
    ON it.item_id = si.item_id

GROUP BY
    t.tag_id,
    t.name

HAVING COUNT(DISTINCT si.item_id) >= 10

ORDER BY
    median_reviews DESC NULLS LAST

LIMIT 20;


-- Tag performance analysis
-- Only tags assigned to at least 20 games

SELECT
    t.name AS tag,

    COUNT(DISTINCT si.item_id) AS games_count,

    COUNT(si.review_count) AS games_with_reviews,

    ROUND(
        COUNT(si.review_count)::numeric
        / NULLIF(COUNT(DISTINCT si.item_id), 0) * 100,
        2
    ) AS review_coverage_percent,

    ROUND(AVG(si.review_count), 0) AS average_reviews,

    PERCENTILE_CONT(0.5)
        WITHIN GROUP (ORDER BY si.review_count)
        AS median_reviews,

    SUM(si.review_count) AS total_reviews

FROM analytics.tags t

JOIN analytics.item_tags it
    ON t.tag_id = it.tag_id

JOIN analytics.steam_items si
    ON it.item_id = si.item_id

GROUP BY
    t.tag_id,
    t.name

HAVING COUNT(DISTINCT si.item_id) >= 20

ORDER BY
    median_reviews DESC NULLS LAST

LIMIT 20;

