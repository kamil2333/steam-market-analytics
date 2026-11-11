
BEGIN;

-- 1. Populate the genre dictionary
INSERT INTO analytics.genres (name)
SELECT DISTINCT
    TRIM(split_genre.genre_name)
FROM analytics.steam_items si
JOIN staging.steam_games_raw sr
    ON sr.raw_id = si.source_raw_id
CROSS JOIN LATERAL
    regexp_split_to_table(sr.genres, '-') AS split_genre(genre_name)
WHERE sr.genres IS NOT NULL
  AND TRIM(split_genre.genre_name) <> ''
ON CONFLICT (name) DO NOTHING;


-- 2. Populate the tag dictionary
INSERT INTO analytics.tags (name)
SELECT DISTINCT
    TRIM(split_tag.tag_name)
FROM analytics.steam_items si
JOIN staging.steam_games_raw sr
    ON sr.raw_id = si.source_raw_id
CROSS JOIN LATERAL
    regexp_split_to_table(sr.tags, '-') AS split_tag(tag_name)
WHERE sr.tags IS NOT NULL
  AND TRIM(split_tag.tag_name) <> ''
ON CONFLICT (name) DO NOTHING;


-- 3. Populate the item-genre relationship table
INSERT INTO analytics.item_genres (item_id, genre_id)
SELECT DISTINCT
    si.item_id,
    g.genre_id
FROM analytics.steam_items si
JOIN staging.steam_games_raw sr
    ON sr.raw_id = si.source_raw_id
CROSS JOIN LATERAL
    regexp_split_to_table(sr.genres, '-') AS split_genre(genre_name)
JOIN analytics.genres g
    ON g.name = TRIM(split_genre.genre_name)
WHERE sr.genres IS NOT NULL
  AND TRIM(split_genre.genre_name) <> ''
ON CONFLICT (item_id, genre_id) DO NOTHING;


-- 4. Populate the item-tag relationship table
INSERT INTO analytics.item_tags (item_id, tag_id)
SELECT DISTINCT
    si.item_id,
    t.tag_id
FROM analytics.steam_items si
JOIN staging.steam_games_raw sr
    ON sr.raw_id = si.source_raw_id
CROSS JOIN LATERAL
    regexp_split_to_table(sr.tags, '-') AS split_tag(tag_name)
JOIN analytics.tags t
    ON t.name = TRIM(split_tag.tag_name)
WHERE sr.tags IS NOT NULL
  AND TRIM(split_tag.tag_name) <> ''
ON CONFLICT (item_id, tag_id) DO NOTHING;

COMMIT;
