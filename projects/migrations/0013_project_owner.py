# Generated by Django 4.0 on 2022-08-13 14:46

import auto_prefetch
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_profile_username'),
        ('projects', '0012_alter_project_id_alter_review_id_alter_tag_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='owner',
            field=auto_prefetch.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.profile'),
        ),
    ]
