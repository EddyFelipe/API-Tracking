# Generated by Django 3.0.8 on 2020-07-27 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200726_2228'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paquete',
            options={'ordering': ['-modificado_en']},
        ),
    ]
