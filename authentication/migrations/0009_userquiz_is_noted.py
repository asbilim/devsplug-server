# Generated by Django 5.0.3 on 2024-04-03 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_userquiz_total_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='userquiz',
            name='is_noted',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
