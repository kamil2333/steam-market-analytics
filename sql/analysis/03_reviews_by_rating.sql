SELECT
    COALESCE(
        NULLIF(TRIM(general_reviews), ''),
        'Unknown'
    ) AS review_category,
    COUNT(*) AS item_count,
    COUNT(review_count) AS items_with_review_count,
    ROUND(AVG(review_count), 0) AS average_review_count,
    ROUND(
        percentile_cont(0.5)
        WITHIN GROUP (ORDER BY review_count)::numeric,
        0
    ) AS median_review_count
FROM analytics.steam_items
GROUP BY
    COALESCE(
        NULLIF(TRIM(general_reviews), ''),
        'Unknown'
    )
ORDER BY median_review_count DESC NULLS LAST;