# Generated by Django 2.0.2 on 2019-05-31 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codejam', '0003_user_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='roundresult',
            name='points',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]