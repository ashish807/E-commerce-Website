# Generated by Django 3.2 on 2021-06-07 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_appointments_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointments',
            name='report',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
