# Generated by Django 4.1.5 on 2023-01-09 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forum_note", "0007_alter_tag_note_to"),
    ]

    operations = [
        migrations.AddField(
            model_name="tag",
            name="search_word",
            field=models.CharField(
                default="default", max_length=20, verbose_name="検索値"
            ),
        ),
    ]
