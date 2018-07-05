# Generated by Django 2.0.5 on 2018-07-05 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20180626_1323'),
        ('devices', '0002_auto_20180705_0455'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='userOwner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.User'),
            preserve_default=False,
        ),
    ]