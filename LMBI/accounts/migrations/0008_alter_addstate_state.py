# Generated by Django 3.2 on 2021-06-06 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_addaddress_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addstate',
            name='state',
            field=models.TextField(default='Chandigarh', max_length=150, unique=True),
        ),
    ]
