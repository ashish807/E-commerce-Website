# Generated by Django 3.2 on 2021-05-26 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20210525_0608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Cancelled', 'Cancelled'), ('Completed', 'Completed'), ('New', 'New')], default='New', max_length=10),
        ),
    ]
