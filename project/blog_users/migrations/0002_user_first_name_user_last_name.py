# Generated by Django 4.1.4 on 2023-01-03 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
