# Generated by Django 3.2.3 on 2021-05-29 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Completed', 'Completed'), ('Accepted', 'Accepted'), ('Cancelled', 'Cancelled')], default='New', max_length=10),
        ),
    ]
