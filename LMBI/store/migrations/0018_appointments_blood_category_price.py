# Generated by Django 3.2 on 2021-07-12 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_appointments_total_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointments',
            name='blood_category_price',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]