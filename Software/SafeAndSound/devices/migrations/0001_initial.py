# Generated by Django 2.0.5 on 2018-07-04 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Device Name')),
                ('isAlarmEnabled', models.BooleanField(max_length=30, verbose_name='Enabled')),
            ],
        ),
    ]