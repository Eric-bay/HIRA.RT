# Generated by Django 5.1 on 2024-09-15 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
