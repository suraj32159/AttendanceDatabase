# Generated by Django 3.2.6 on 2021-11-28 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('enrollment_no', models.IntegerField(max_length=70)),
                ('file_name', models.CharField(max_length=255)),
            ],
        ),
    ]
