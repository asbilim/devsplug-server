# Generated by Django 5.0.3 on 2024-04-02 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0004_alter_problemquiz_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='score',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
