from django.contrib import admin
from .models import Note, Comment, Tag

# Register your models here.
admin.site.register(Note)
admin.site.register(Comment)
admin.site.register(Tag)