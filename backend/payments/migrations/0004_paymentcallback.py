from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_payment_is_non_refundable_payment_is_verified_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentCallback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(max_length=64)),
                ('callback_id', models.CharField(max_length=128, unique=True)),
                ('payload', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=models.deletion.SET_NULL, to='payments.payment')),
            ],
        ),
    ]
