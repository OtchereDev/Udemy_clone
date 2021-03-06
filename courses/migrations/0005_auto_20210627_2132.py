# Generated by Django 3.1.5 on 2021-06-27 21:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20210627_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
        migrations.AlterField(
            model_name='sector',
            name='sector_uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
