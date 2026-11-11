
BEGIN;

ALTER TABLE analytics.steam_items
    DROP COLUMN IF EXISTS genres,
    DROP COLUMN IF EXISTS tags;

COMMIT;
