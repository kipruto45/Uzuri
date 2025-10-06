from django.db import migrations


class Migration(migrations.Migration):
    # This migration was added to restore RegistrarProfile during local debugging.
    # It is now a no-op to avoid duplicate CreateModel operations because
    # the repository already contains a migration that creates the same model
    # (0001_initial_registrar). Keeping this as an empty migration preserves
    # the migration numbering while preventing "table already exists" errors
    # when the test runner applies migrations to a fresh test database.
    dependencies = [
        ("core", "0005_studentprofile_student_id"),
    ]

    operations = []
