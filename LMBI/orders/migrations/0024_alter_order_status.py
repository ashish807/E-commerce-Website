# Generated by Django 3.2.3 on 2021-05-30 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0023_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('Accepted', 'Accepted'), ('Cancelled', 'Cancelled'), ('New', 'New')], default='New', max_length=10),
        ),
    ]
