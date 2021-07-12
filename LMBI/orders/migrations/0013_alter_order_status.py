# Generated by Django 3.2.3 on 2021-05-29 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('New', 'New'), ('Accepted', 'Accepted'), ('Cancelled', 'Cancelled')], default='New', max_length=10),
        ),
    ]
