# Generated by Django 4.0 on 2022-12-25 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_historycase'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=200)),
                ('img', models.CharField(max_length=500)),
            ],
        ),
    ]