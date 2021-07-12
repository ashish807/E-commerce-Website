# Generated by Django 3.2.3 on 2021-05-30 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0021_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Cancelled', 'Cancelled'), ('New', 'New'), ('Accepted', 'Accepted'), ('Completed', 'Completed')], default='New', max_length=10),
        ),
    ]
