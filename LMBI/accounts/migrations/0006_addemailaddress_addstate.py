# Generated by Django 3.2 on 2021-06-06 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210530_0915'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.TextField(blank=True, default='Chandigarh', max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='AddEmailAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.addstate')),
            ],
        ),
    ]
