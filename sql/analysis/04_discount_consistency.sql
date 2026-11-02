WITH discount_check AS (
    SELECT
        title,
        price_eur,
        original_price_eur,
        discount_percent,
        ROUND(
            100.0 * (original_price_eur - price_eur)
            / NULLIF(original_price_eur, 0),
            2
        ) AS calculated_discount_percent
    FROM analytics.steam_items
    WHERE price_eur IS NOT NULL
      AND original_price_eur > 0
      AND discount_percent IS NOT NULL
)
SELECT
    COUNT(*) AS items_checked,
    COUNT(*) FILTER (
        WHERE ABS(
            calculated_discount_percent - discount_percent
        ) <= 1
    ) AS matching_discounts,
    COUNT(*) FILTER (
        WHERE ABS(
            calculated_discount_percent - discount_percent
        ) > 1
    ) AS potentially_inconsistent,
    ROUND(
        AVG(
            ABS(calculated_discount_percent - discount_percent)
        ),
        2
    ) AS average_absolute_difference
FROM discount_check;