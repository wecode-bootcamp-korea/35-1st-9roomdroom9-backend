# Generated by Django 4.0.6 on 2022-07-20 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateField(default='0000-00-00', null=True),
        ),
    ]
