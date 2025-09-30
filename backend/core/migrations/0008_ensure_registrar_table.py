from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_merge_20250928_2110"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE TABLE IF NOT EXISTS core_registrarprofile (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role VARCHAR(16),
                    user_id INTEGER UNIQUE REFERENCES core_customuser(id)
                );
            """,
            reverse_sql="DROP TABLE IF EXISTS core_registrarprofile;",
        ),
    ]
