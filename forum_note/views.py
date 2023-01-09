from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.db.models import Q

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
            if request.user.python_student and request.user.staff:
                tags = Tag.objects.all()
            elif request.user.python_student:
                python_public_notes = Note.objects.filter(Q(open_range="python_members") | Q(open_range="public"))
                tags = Tag.objects.filter(note_to__in=python_public_notes)
            elif request.user.staff:
                staff_public_notes = Note.objects.filter(Q(open_range="subscribers") | Q(open_range="public"))
                tags = Tag.objects.filter(note_to__in=staff_public_notes)
            else:
                public_notes = Note.objects.filter(open_range="public")
                tags = Tag.objects.filter(note_to__in=public_notes)

        elif range == "public":
            notes = Note.objects.filter(open_range=range).prefetch_related("comments")
            public_notes = Note.objects.filter(open_range="public")
            tags = Tag.objects.filter(note_to__in=public_notes)
        context = {"notes": notes, "tags": tags}
        return render(request, "forum_note/note_list.html", context)


class NoteListGroup(LoginRequiredMixin404, View):
    def get(self, request, group, *args, **kwargs):
        if group == "python_members" and request.user.python_student:
            notes = Note.objects.filter(open_range=group).prefetch_related("comments")
            python_notes = Note.objects.filter(open_range="python_members")
            tags = Tag.objects.filter(note_to__in=python_notes)
        elif group == "subscribers" and request.user.staff:
            notes = Note.objects.filter(open_range=group).prefetch_related("comments")
            subscribe_notes = Note.objects.filter(open_range="subscribers")
            tags = Tag.objects.filter(note_to__in=subscribe_notes)
        else:
            raise Http404("ページが見つかりません")
        context = {"notes": notes, "tags": tags}
        return render(request, "forum_note/note_list.html", context)


def NoteListTag(request, tag_name):
    return HttpResponse(b"Note list Tag")


def NoteDetail(request, pk):
    return HttpResponse(b"Note detail")


def NotePost(request):
    return HttpResponse(b"Note post")
