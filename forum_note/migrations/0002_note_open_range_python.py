# Generated by Django 4.1.5 on 2023-01-08 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forum_note", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="note",
            name="open_range_python",
            field=models.BooleanField(default=False, verbose_name="pythonゼミ限定"),
        ),
    ]
