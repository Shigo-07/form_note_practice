from django.db import models
from django.conf import settings


class Note(models.Model):
    """
    投稿記事モデル
    """
    title = models.CharField("タイトル", max_length=128)
    content = models.TextField("記事", blank=True)
    is_publish_mail = models.BooleanField("メール発行", default=False)
    attach_file = models.FileField(
        upload_to='uploads/%Y/%m/%d/',
        verbose_name="添付ファイル",
        blank=True,
    )
    attach_image = models.ImageField(
        upload_to="images/%Y/%m/%d/",
        verbose_name="添付画像",
        blank=True,
    )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   verbose_name="投稿者",
                                   default="名無しさん",
                                   on_delete=models.SET_DEFAULT)
    created_at = models.DateTimeField('投稿日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)

    open_range = models.CharField("公開範囲", default="subscribers", max_length=20)

    class Meta:
        db_table = "notes"

    def __str__(self):
        return f"{self.pk} {self.title}"


class Comment(models.Model):
    """
    コメントモデル
    """
    content = models.TextField("コメント", blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   verbose_name="投稿者",
                                   on_delete=models.CASCADE)
    created_at = models.DateTimeField('投稿日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)
    note_to = models.ForeignKey(Note, verbose_name="投稿", on_delete=models.CASCADE,related_name="comments")

    class Meta:
        db_table = "comments"

    def __str__(self):
        return f"{self.pk} {self.created_by} comment"

class Tag(models.Model):
    """
    タグモデル
    """
    tag_name = models.CharField("タグ", max_length=30)
    note_to = models.ManyToManyField(Note, verbose_name="投稿", related_query_name="tags")

    class Meta:
        db_table = "tags"

    def __str__(self):
        return self.tag_name
