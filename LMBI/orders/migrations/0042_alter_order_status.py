# Generated by Django 3.2.3 on 2021-06-14 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0041_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Cancelled', 'Cancelled'), ('Accepted', 'Accepted'), ('New', 'New'), ('Completed', 'Completed')], default='New', max_length=10),
        ),
    ]
