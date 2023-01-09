# Generated by Django 4.0 on 2023-01-05 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0016_remove_cases_time_term_remove_cases_term_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cases',
            name='history',
            field=models.JSONField(default='[]'),
        ),
        migrations.AlterField(
            model_name='cases',
            name='items',
            field=models.JSONField(default='[]'),
        ),
        migrations.AlterField(
            model_name='cases',
            name='status',
            field=models.IntegerField(choices=[(1, 'Expectation'), (0, 'Published'), (2, 'Archive')], default=1),
        ),
    ]
