from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0008_ensure_registrar_table"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE TABLE IF NOT EXISTS core_studentadmission (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    intake_year INTEGER,
                    program VARCHAR(100),
                    campus VARCHAR(100),
                    department VARCHAR(100),
                    kcse_certificate VARCHAR(100),
                    result_slip VARCHAR(100),
                    id_passport VARCHAR(100),
                    admission_letter VARCHAR(100),
                    student_id INTEGER REFERENCES core_studentprofile(id),
                    study_mode_id INTEGER REFERENCES core_studymode(id),
                    disability_id INTEGER REFERENCES core_disability(id)
                );
            """,
            reverse_sql="DROP TABLE IF EXISTS core_studentadmission;",
        ),
        migrations.RunSQL(
            sql="""
                CREATE TABLE IF NOT EXISTS core_leaveofabsence (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reason TEXT,
                    status VARCHAR(16),
                    requested_at DATETIME,
                    approved_at DATETIME,
                    student_id INTEGER REFERENCES core_studentprofile(id),
                    approved_by_id INTEGER REFERENCES core_registrarprofile(id)
                );
            """,
            reverse_sql="DROP TABLE IF EXISTS core_leaveofabsence;",
        ),
        migrations.RunSQL(
            sql="""
                CREATE TABLE IF NOT EXISTS core_transferrequest (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    from_program VARCHAR(100),
                    to_program VARCHAR(100),
                    status VARCHAR(16),
                    requested_at DATETIME,
                    approved_at DATETIME,
                    student_id INTEGER REFERENCES core_studentprofile(id),
                    approved_by_id INTEGER REFERENCES core_registrarprofile(id)
                );
            """,
            reverse_sql="DROP TABLE IF EXISTS core_transferrequest;",
        ),
        migrations.RunSQL(
            sql="""
                CREATE TABLE IF NOT EXISTS core_graduationclearance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    status VARCHAR(16),
                    checked_at DATETIME,
                    student_id INTEGER REFERENCES core_studentprofile(id),
                    checked_by_id INTEGER REFERENCES core_registrarprofile(id)
                );
            """,
            reverse_sql="DROP TABLE IF EXISTS core_graduationclearance;",
        ),
    ]
