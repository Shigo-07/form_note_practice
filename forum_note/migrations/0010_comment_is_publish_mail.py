# Generated by Django 4.1.5 on 2023-01-14 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forum_note", "0009_comment_attach_file_comment_attach_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="is_publish_mail",
            field=models.BooleanField(default=False, verbose_name="メール発行"),
        ),
    ]