# Generated by Django 3.2.13 on 2022-08-12 00:19

import DevSearch.utils.uploads
import auto_prefetch
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_alter_review_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='featured_image',
            field=models.ImageField(blank=True, default='user-default.png', null=True, upload_to=DevSearch.utils.uploads.project_image_upload_path),
        ),
        migrations.AlterField(
            model_name='review',
            name='project',
            field=auto_prefetch.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_reviews', to='projects.project'),
        ),
    ]
