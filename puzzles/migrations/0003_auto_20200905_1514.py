# Generated by Django 2.0.2 on 2020-09-05 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0002_puzzle_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='puzzle',
            name='author',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='puzzle',
            name='commentText',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='puzzle',
            name='constraints',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='puzzle',
            name='inputDescription',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='puzzle',
            name='outputDescription',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='puzzle',
            name='puzzleType',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='puzzle',
            name='statement',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='puzzle',
            name='statementHTML',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='puzzle',
            name='testCases',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='puzzle',
            name='title',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='puzzle',
            name='topics',
            field=models.TextField(default=''),
        ),
    ]
