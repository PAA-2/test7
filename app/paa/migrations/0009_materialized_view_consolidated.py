from django.db import migrations

SQL_UP = """
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_plan_consolidated AS
SELECT
  p.id as plan_id,
  p.code as plan_code,
  COUNT(a.id) as total_actions,
  COUNT(a.id) FILTER (WHERE a.status = 'EN_COURS') as en_cours,
  COUNT(a.id) FILTER (WHERE a.status = 'EN_TRAITEMENT') as en_traitement,
  COUNT(a.id) FILTER (WHERE a.status = 'CLOTUREE') as cloturees,
  COUNT(a.id) FILTER (WHERE a.due_date < now()::date AND a.status IN ('A_FAIRE','EN_COURS','EN_TRAITEMENT')) as retards
FROM paa_plan p
LEFT JOIN paa_actionplan ap ON ap.plan_id = p.id
LEFT JOIN paa_action a ON a.id = ap.action_id
GROUP BY p.id, p.code;
CREATE INDEX IF NOT EXISTS idx_mv_plan_consolidated_plan ON mv_plan_consolidated(plan_id);
"""

SQL_DOWN = "DROP MATERIALIZED VIEW IF EXISTS mv_plan_consolidated;"


def create_mv(apps, schema_editor):
    if schema_editor.connection.vendor == "postgresql":
        with schema_editor.connection.cursor() as cur:
            cur.execute(SQL_UP)


def drop_mv(apps, schema_editor):
    if schema_editor.connection.vendor == "postgresql":
        with schema_editor.connection.cursor() as cur:
            cur.execute(SQL_DOWN)


class Migration(migrations.Migration):
    dependencies = [
        ("paa", "0008_perf_indexes"),
    ]

    operations = [migrations.RunPython(create_mv, drop_mv)]
