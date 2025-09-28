from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0004_disability_studymode_studentprofile_disability_and_more'),
    ]
    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='student_id',
            field=models.CharField(max_length=32, unique=True, blank=True, editable=False, null=True),
        ),
    ]
