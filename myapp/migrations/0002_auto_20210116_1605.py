# Generated by Django 3.1.4 on 2021-01-16 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='username',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
