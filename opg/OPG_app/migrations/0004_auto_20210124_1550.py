# Generated by Django 3.1.5 on 2021-01-24 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OPG_app', '0003_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(default='Adresa 123, 123 Grad', max_length=64),
        ),
        migrations.AddField(
            model_name='profile',
            name='email2',
            field=models.CharField(default='info@info.com', max_length=64),
        ),
        migrations.AddField(
            model_name='profile',
            name='opg_id',
            field=models.CharField(default='OPG Marko', max_length=64),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(default='1234567', max_length=64),
        ),
    ]
