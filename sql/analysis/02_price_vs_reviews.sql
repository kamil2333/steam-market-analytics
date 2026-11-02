WITH price_groups AS (
    SELECT
        CASE
            WHEN price_eur = 0 THEN 'Free'
            WHEN price_eur <= 10 THEN '0.01-10 EUR'
            WHEN price_eur <= 25 THEN '10.01-25 EUR'
            WHEN price_eur <= 50 THEN '25.01-50 EUR'
            ELSE 'Over 50 EUR'
        END AS price_band,

        CASE
            WHEN price_eur = 0 THEN 1
            WHEN price_eur <= 10 THEN 2
            WHEN price_eur <= 25 THEN 3
            WHEN price_eur <= 50 THEN 4
            ELSE 5
        END AS sort_order,

        review_count

    FROM analytics.steam_items
    WHERE price_eur IS NOT NULL
      AND review_count IS NOT NULL
)

SELECT
    price_band,
    COUNT(*) AS item_count,
    ROUND(AVG(review_count), 0) AS average_review_count,
    ROUND(
        percentile_cont(0.5)
        WITHIN GROUP (ORDER BY review_count)::numeric,
        0
    ) AS median_review_count

FROM price_groups
GROUP BY price_band, sort_order
ORDER BY sort_order;