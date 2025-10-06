from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('core', '0005_studentprofile_student_id'),
    ]
    operations = [
        
        migrations.SeparateDatabaseAndState(
            database_operations=[
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
            ],
            state_operations=[
                migrations.CreateModel(
                    name='RegistrarProfile',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('role', models.CharField(max_length=16)),
                        ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.CustomUser')),
                    ],
                ),
            ],
        ),
        migrations.CreateModel(
            name='DisabilityCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('cue_code', models.CharField(max_length=8, blank=True)),
            ],
        ),
        migrations.RunSQL(
            sql="""
                CREATE TABLE IF NOT EXISTS core_studymode (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(32) UNIQUE
                );
            """,
            reverse_sql="DROP TABLE IF EXISTS core_studymode;"
        ),
        migrations.RunSQL(
            sql="""
                CREATE TABLE IF NOT EXISTS core_disability (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category VARCHAR(16),
                    support_needs TEXT,
                    tagged_for_reporting BOOLEAN DEFAULT 0,
                    student_id INTEGER REFERENCES core_studentprofile(id)
                );
            """,
            reverse_sql="DROP TABLE IF EXISTS core_disability;"
        ),
        migrations.CreateModel(
            name='StudentAdmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intake_year', models.IntegerField()),
                ('program', models.CharField(max_length=100)),
                ('campus', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
                ('kcse_certificate', models.FileField(blank=True, null=True, upload_to='kcse/')),
                ('result_slip', models.FileField(blank=True, null=True, upload_to='results/')),
                ('id_passport', models.FileField(blank=True, null=True, upload_to='ids/')),
                ('admission_letter', models.FileField(blank=True, null=True, upload_to='admission_letters/')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.StudentProfile')),
                ('study_mode', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.StudyMode')),
                ('disability', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Disability')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveOfAbsence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('status', models.CharField(default='pending', max_length=16)),
                ('requested_at', models.DateTimeField(auto_now_add=True)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.StudentProfile')),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.RegistrarProfile')),
            ],
        ),
        migrations.CreateModel(
            name='TransferRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_program', models.CharField(max_length=100)),
                ('to_program', models.CharField(max_length=100)),
                ('status', models.CharField(default='pending', max_length=16)),
                ('requested_at', models.DateTimeField(auto_now_add=True)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.StudentProfile')),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.RegistrarProfile')),
            ],
        ),
        migrations.CreateModel(
            name='GraduationClearance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='pending', max_length=16)),
                ('checked_at', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.StudentProfile')),
                ('checked_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.RegistrarProfile')),
            ],
        ),
        migrations.CreateModel(
            name='RegistrarAuditLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('details', models.TextField(blank=True)),
                ('encrypted', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.CustomUser')),
            ],
        ),
    ]
