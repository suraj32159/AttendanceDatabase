# Generated by Django 3.2.6 on 2021-12-12 17:53

from django.db import migrations, models
import enroll.models


class Migration(migrations.Migration):

    dependencies = [
        ('enroll', '0004_alter_user_file_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='course',
            field=models.CharField(choices=[('mca', 'MCA'), ('msc', 'M.Sc')], default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='file_name',
            field=models.FileField(upload_to=enroll.models.file_path_dir),
        ),
    ]
