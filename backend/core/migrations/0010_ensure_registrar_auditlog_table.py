from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_ensure_registrar_models_tables"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE TABLE IF NOT EXISTS core_registrarauditlog (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER REFERENCES core_customuser(id),
                    action VARCHAR(100),
                    timestamp DATETIME,
                    details TEXT,
                    encrypted BOOLEAN DEFAULT 0
                );
            """,
            reverse_sql="DROP TABLE IF EXISTS core_registrarauditlog;",
        ),
    ]
