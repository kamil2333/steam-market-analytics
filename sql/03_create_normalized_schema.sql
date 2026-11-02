BEGIN;

CREATE TABLE analytics.genres (
    genre_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE analytics.item_genres (
    item_id BIGINT NOT NULL,
    genre_id BIGINT NOT NULL,

    PRIMARY KEY (item_id, genre_id),

    CONSTRAINT item_genres_item_id_fkey
        FOREIGN KEY (item_id)
        REFERENCES analytics.steam_items(item_id)
        ON DELETE CASCADE,

    CONSTRAINT item_genres_genre_id_fkey
        FOREIGN KEY (genre_id)
        REFERENCES analytics.genres(genre_id)
        ON DELETE CASCADE
);

CREATE TABLE analytics.tags (
    tag_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE analytics.item_tags (
    item_id BIGINT NOT NULL,
    tag_id BIGINT NOT NULL,

    PRIMARY KEY (item_id, tag_id),

    CONSTRAINT item_tags_item_id_fkey
        FOREIGN KEY (item_id)
        REFERENCES analytics.steam_items(item_id)
        ON DELETE CASCADE,

    CONSTRAINT item_tags_tag_id_fkey
        FOREIGN KEY (tag_id)
        REFERENCES analytics.tags(tag_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_item_genres_genre_id
    ON analytics.item_genres(genre_id);

CREATE INDEX idx_item_tags_tag_id
    ON analytics.item_tags(tag_id);

COMMIT;