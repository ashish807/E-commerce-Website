# Generated by Django 3.2.3 on 2021-05-17 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20210517_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointments',
            name='blood_category',
            field=models.ForeignKey(default='Diabetes', null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.bloodcategory'),
        ),
    ]
