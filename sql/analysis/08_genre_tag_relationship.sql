-- Most common tags within each genre
-- Including genre coverage percentage

WITH genre_totals AS (
    SELECT
        g.genre_id,
        g.name AS genre,
        COUNT(DISTINCT ig.item_id) AS total_games
    FROM analytics.genres g
    JOIN analytics.item_genres ig
        ON g.genre_id = ig.genre_id
    GROUP BY g.genre_id, g.name
),
genre_tag_statistics AS (
    SELECT
        g.genre_id,
        g.name AS genre,
        t.name AS tag,
        COUNT(DISTINCT ig.item_id) AS games_count
    FROM analytics.genres g
    JOIN analytics.item_genres ig
        ON g.genre_id = ig.genre_id
    JOIN analytics.item_tags it
        ON ig.item_id = it.item_id
    JOIN analytics.tags t
        ON it.tag_id = t.tag_id
    GROUP BY
        g.genre_id,
        g.name,
        t.tag_id,
        t.name
),
ranked_tags AS (
    SELECT
        s.genre,
        s.tag,
        s.games_count,
        ROUND(
            s.games_count::numeric
            / NULLIF(gt.total_games, 0) * 100,
            2
        ) AS genre_coverage_percent,
        RANK() OVER (
            PARTITION BY s.genre
            ORDER BY s.games_count DESC
        ) AS tag_rank
    FROM genre_tag_statistics s
    JOIN genre_totals gt
        ON s.genre_id = gt.genre_id
)
SELECT
    genre,
    tag,
    games_count,
    genre_coverage_percent,
    tag_rank
FROM ranked_tags
WHERE tag_rank <= 5
ORDER BY genre, tag_rank, tag;