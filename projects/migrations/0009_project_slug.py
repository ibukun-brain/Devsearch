# Generated by Django 3.2.13 on 2022-08-12 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_auto_20220812_0119'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]