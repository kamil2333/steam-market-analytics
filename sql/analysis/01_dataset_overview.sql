-- 1. General overview of the analytical dataset

SELECT
    COUNT(*) AS total_items,
    COUNT(price_eur) AS items_with_price,
    COUNT(*) FILTER (
        WHERE price_eur IS NULL
    ) AS items_without_price,
    COUNT(*) FILTER (
        WHERE price_eur = 0
    ) AS zero_price_items,
    ROUND(AVG(price_eur), 2) AS average_price_eur,
    ROUND(
        percentile_cont(0.5)
        WITHIN GROUP (ORDER BY price_eur)::numeric,
        2
    ) AS median_price_eur,
    MIN(price_eur) AS minimum_price_eur,
    MAX(price_eur) AS maximum_price_eur,
    COUNT(*) FILTER (
        WHERE is_source_error
    ) AS source_error_items
FROM analytics.steam_items;


-- 2. Distribution of items by price range

WITH price_groups AS (
    SELECT
        CASE
            WHEN price_eur IS NULL THEN 'Unknown price'
            WHEN price_eur = 0 THEN 'Zero price'
            WHEN price_eur <= 10 THEN 'Up to 10 EUR'
            WHEN price_eur <= 25 THEN '10.01-25 EUR'
            WHEN price_eur <= 50 THEN '25.01-50 EUR'
            ELSE 'Over 50 EUR'
        END AS price_band,
        CASE
            WHEN price_eur IS NULL THEN 5
            WHEN price_eur = 0 THEN 0
            WHEN price_eur <= 10 THEN 1
            WHEN price_eur <= 25 THEN 2
            WHEN price_eur <= 50 THEN 3
            ELSE 4
        END AS sort_order
    FROM analytics.steam_items
)
SELECT
    price_band,
    COUNT(*) AS item_count,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM price_groups
GROUP BY price_band, sort_order
ORDER BY sort_order;


-- 3. Distribution of review categories

SELECT
    COALESCE(
        NULLIF(TRIM(general_reviews), ''),
        'Unknown'
    ) AS review_category,
    COUNT(*) AS item_count,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM analytics.steam_items
GROUP BY
    COALESCE(NULLIF(TRIM(general_reviews), ''), 'Unknown')
ORDER BY item_count DESC;


-- 4. Ten items with the highest number of reviews

SELECT
    title,
    review_count,
    general_reviews,
    price_eur,
    url
FROM analytics.steam_items
WHERE review_count IS NOT NULL
ORDER BY review_count DESC
LIMIT 10;