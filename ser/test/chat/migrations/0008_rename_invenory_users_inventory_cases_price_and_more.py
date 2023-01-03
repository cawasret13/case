# Generated by Django 4.0 on 2022-12-26 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_alter_users_invenory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='invenory',
            new_name='inventory',
        ),
        migrations.AddField(
            model_name='cases',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='item',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='users',
            name='money',
            field=models.FloatField(default=0),
        ),
    ]