# Generated by Django 2.0.2 on 2019-05-31 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='puzzle',
            name='comments',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
