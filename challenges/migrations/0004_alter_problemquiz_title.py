# Generated by Django 5.0.3 on 2024-04-02 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0003_problems_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemquiz',
            name='title',
            field=models.CharField(max_length=250, null=True, unique=True),
        ),
    ]
