# Generated by Django 3.2.3 on 2021-06-13 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0040_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Cancelled', 'Cancelled'), ('New', 'New'), ('Completed', 'Completed')], default='New', max_length=10),
        ),
    ]
