# Generated by Django 5.0.3 on 2024-04-03 18:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0005_useranswer_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='ratings',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='challenges.ratings'),
        ),
        migrations.AlterField(
            model_name='ratings',
            name='score',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
