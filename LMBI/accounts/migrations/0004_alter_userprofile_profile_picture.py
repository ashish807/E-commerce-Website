# Generated by Django 3.2.3 on 2021-05-29 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='userprofile/defaultAccImage.png', upload_to='userprofile'),
        ),
    ]
