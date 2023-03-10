# Generated by Django 4.0 on 2023-01-05 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0017_alter_cases_history_alter_cases_items_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cases',
            name='history',
            field=models.JSONField(default=[]),
        ),
        migrations.AlterField(
            model_name='cases',
            name='items',
            field=models.JSONField(default=[]),
        ),
        migrations.AlterField(
            model_name='cases',
            name='status',
            field=models.IntegerField(choices=[(0, 'Published'), (1, 'Expectation'), (2, 'Archive')], default=1),
        ),
    ]
