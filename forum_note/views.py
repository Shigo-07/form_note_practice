from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from forum_note.models import Note, Comment, Tag


class LoginRequiredMixin404(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404("ページが見つかりません")
        return super().dispatch(request, *args, **kwargs)


class NoteListRange(LoginRequiredMixin404, View):
    def get(self, request, range, *args, **kwargs):
        # indexは全ページ表示
        if range == "index":
            notes = Note.objects.all().prefetch_related("comments")
        elif range == "public":
            notes = Note.objects.filter(open_range=range).prefetch_related("comments")
        context = {"notes": notes}
        return render(request, "forum_note/note_list.html", context)


class NoteListGroup(LoginRequiredMixin404, View):
    def get(self, request, group, *args, **kwargs):
        if group == "python_members" and request.user.python_student:
            notes = Note.objects.filter(open_range=group).prefetch_related("comments")
        elif group == "subscribers" and request.user.staff:
            notes = Note.objects.filter(open_range=group).prefetch_related("comments")
        else:
            raise Http404("ページが見つかりません")
        context = {"notes": notes}
        return render(request, "forum_note/note_list.html", context)

def NoteListTag(request, tag_name):
    return HttpResponse(b"Note list Tag")


def NoteDetail(request, pk):
    return HttpResponse(b"Note detail")


def NotePost(request):
    return HttpResponse(b"Note post")
