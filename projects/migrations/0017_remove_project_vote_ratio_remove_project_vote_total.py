# Generated by Django 4.0 on 2022-08-19 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0016_alter_review_options_review_owner_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='vote_ratio',
        ),
        migrations.RemoveField(
            model_name='project',
            name='vote_total',
        ),
    ]
