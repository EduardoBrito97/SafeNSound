# Generated by Django 2.0.5 on 2018-07-05 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='bluetooth_id',
            field=models.CharField(default=1, max_length=30, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='device',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Device Name'),
        ),
    ]