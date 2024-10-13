# Generated by Django 5.1.2 on 2024-10-13 16:20

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_attempt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
