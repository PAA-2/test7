from django.db import migrations

MIG_SQL = """
-- Extension nécessaire (si non active)
CREATE EXTENSION IF NOT EXISTS unaccent;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Colonne tsvector sur paa_action
ALTER TABLE paa_action
  ADD COLUMN IF NOT EXISTS search_vector tsvector;

-- Index GIN sur search_vector
CREATE INDEX IF NOT EXISTS idx_action_search_gin
  ON paa_action
  USING GIN (search_vector);

-- Fonction de mise à jour (langue française)
CREATE OR REPLACE FUNCTION paa_update_action_search_vector(a_id uuid)
RETURNS void
LANGUAGE plpgsql
AS $$
DECLARE
  combined_ocr text;
BEGIN
  SELECT string_agg(coalesce(attach.ocr_text, ''), ' ')
  INTO combined_ocr
  FROM paa_attachment attach
  WHERE attach.action_id = a_id;

  UPDATE paa_action
  SET search_vector = 
    setweight(to_tsvector('french', coalesce(title,'')), 'A') ||
    setweight(to_tsvector('french', coalesce(description,'')), 'B') ||
    setweight(to_tsvector('french', coalesce(combined_ocr, '')), 'C')
  WHERE id = a_id;
END$$;

-- Trigger pour maj auto (insert/update) côté action
DROP TRIGGER IF EXISTS trg_action_search_update ON paa_action;
CREATE TRIGGER trg_action_search_update
AFTER INSERT OR UPDATE OF title, description ON paa_action
FOR EACH ROW EXECUTE FUNCTION
  paa_update_action_search_vector(NEW.id);
"""

MIG_SQL_DOWN = """
DROP TRIGGER IF EXISTS trg_action_search_update ON paa_action;
DROP FUNCTION IF EXISTS paa_update_action_search_vector(uuid);
DROP INDEX IF EXISTS idx_action_search_gin;
ALTER TABLE paa_action DROP COLUMN IF EXISTS search_vector;
"""


def apply_sql(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(MIG_SQL)


def reverse_sql(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(MIG_SQL_DOWN)


class Migration(migrations.Migration):
    dependencies = [
        ("paa", "0005_attachment"),
    ]

    operations = [
        migrations.RunPython(apply_sql, reverse_sql),
    ]
