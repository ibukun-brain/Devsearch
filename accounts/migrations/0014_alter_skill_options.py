# Generated by Django 4.0 on 2022-08-16 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_alter_skill_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='skill',
            options={'ordering': ['name', '-description']},
        ),
    ]