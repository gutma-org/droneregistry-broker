# Generated by Django 2.2.1 on 2019-05-29 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('switchboard', '0002_searchquery_credentials'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchquery',
            name='more_information_url',
            field=models.URLField(blank=True, default='', null=True),
        ),
    ]