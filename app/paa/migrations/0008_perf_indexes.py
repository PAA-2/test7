from django.db import migrations

SQL = """
CREATE INDEX IF NOT EXISTS idx_action_status_due ON paa_action (status, due_date);
CREATE INDEX IF NOT EXISTS idx_action_priority ON paa_action (priority);
CREATE INDEX IF NOT EXISTS idx_action_j_delta ON paa_action (j_delta);
CREATE INDEX IF NOT EXISTS idx_action_updated_at ON paa_action (updated_at);
CREATE INDEX IF NOT EXISTS idx_plan_is_active ON paa_plan (is_active);
"""


class Migration(migrations.Migration):
    dependencies = [
        ("paa", "0007_auditlog_systemsettings_smtp_password"),
    ]

    operations = [migrations.RunSQL(SQL)]
