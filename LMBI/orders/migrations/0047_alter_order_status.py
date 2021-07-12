# Generated by Django 3.2 on 2021-07-11 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0046_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Cancelled', 'Cancelled'), ('Completed', 'Completed'), ('Accepted', 'Accepted')], default='New', max_length=10),
        ),
    ]
