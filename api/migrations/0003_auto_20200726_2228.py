# Generated by Django 3.0.8 on 2020-07-26 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_client',
            field=models.BooleanField(default=False),
        ),
    ]