# Generated by Django 4.0.6 on 2022-07-20 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateField(blank=True, default='0000-00-00', null=True),
        ),
    ]
