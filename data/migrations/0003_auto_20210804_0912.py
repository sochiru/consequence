# Generated by Django 3.1.13 on 2021-08-04 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_usercred'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercred',
            name='user',
        ),
        migrations.AddField(
            model_name='usercred',
            name='client_id',
            field=models.TextField(null=True),
        ),
    ]