# Generated by Django 4.0 on 2022-08-16 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_skill_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='skill',
            options={'ordering': ['-name', '-description']},
        ),
    ]
