# Generated by Django 5.0.7 on 2024-07-27 23:24

import random
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='name',
            field=models.CharField(default=random.random, max_length=50),
            preserve_default=False,
        ),
    ]
