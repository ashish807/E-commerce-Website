# Generated by Django 3.2 on 2021-06-06 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0032_auto_20210606_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Completed', 'Completed'), ('New', 'New'), ('Cancelled', 'Cancelled')], default='New', max_length=10),
        ),
    ]