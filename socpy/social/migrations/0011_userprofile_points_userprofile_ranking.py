# Generated by Django 4.0.4 on 2022-05-01 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0010_userprofile_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='points',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='ranking',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]