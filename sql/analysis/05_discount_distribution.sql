WITH discount_groups AS (
    SELECT
        CASE
            WHEN discount_percent = 0 THEN '0%'
            WHEN discount_percent <= 10 THEN '1-10%'
            WHEN discount_percent <= 25 THEN '11-25%'
            WHEN discount_percent <= 50 THEN '26-50%'
            WHEN discount_percent <= 75 THEN '51-75%'
            ELSE '76-100%'
        END AS discount_band,

        CASE
            WHEN discount_percent = 0 THEN 1
            WHEN discount_percent <= 10 THEN 2
            WHEN discount_percent <= 25 THEN 3
            WHEN discount_percent <= 50 THEN 4
            WHEN discount_percent <= 75 THEN 5
            ELSE 6
        END AS sort_order,

        discount_percent,
        original_price_eur,
        price_eur
    FROM analytics.steam_items
    WHERE discount_percent IS NOT NULL
)
SELECT
    discount_band,
    COUNT(*) AS item_count,

    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage,

    ROUND(AVG(discount_percent), 2) AS average_discount_percent,

    COUNT(*) FILTER (
        WHERE original_price_eur IS NOT NULL
          AND price_eur IS NOT NULL
    ) AS items_with_both_prices,

    ROUND(
        AVG(original_price_eur - price_eur),
        2
    ) AS average_saving_eur

FROM discount_groups
GROUP BY discount_band, sort_order
ORDER BY sort_order;