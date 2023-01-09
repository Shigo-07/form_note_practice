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
        # keywordのクエリパラメータを受けとった場合、検索用search_queryを生成する
        if "keyword" in request.GET:
            str_search_word = request.GET.get("keyword")
            list_search_word = str_search_word.split()
            search_query = Q()
            for search_word in list_search_word:
                sub_query = Q(title__icontains=search_word) | Q(content__icontains=search_word)
                search_query.add(sub_query, Q.AND)

        if range == "index":
            if "keyword" in request.GET:
                notes = Note.objects.filter(search_query).prefetch_related("comments")
            else:
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
            if "keyword" in request.GET:
                notes = Note.objects.filter(Q(open_range__exact=range) & search_query).prefetch_related("comments")
            else:
                notes = Note.objects.filter(open_range=range).prefetch_related("comments")
            public_notes = Note.objects.filter(open_range="public")
            tags = Tag.objects.filter(note_to__in=public_notes)

        context = {"notes": notes, "tags": tags}
        return render(request, "forum_note/note_list.html", context)


class NoteListGroup(LoginRequiredMixin404, View):
    def get(self, request, group, *args, **kwargs):
        # keywordのクエリパラメータを受けとった場合、検索用search_queryを生成する
        if "keyword" in request.GET:
            str_search_word = request.GET.get("keyword")
            list_search_word = str_search_word.split()
            search_query = Q()
            for search_word in list_search_word:
                sub_query = Q(title__icontains=search_word) | Q(content__icontains=search_word)
                search_query.add(sub_query, Q.AND)
            notes = Note.objects.filter(Q(open_range__exact=group) & search_query).prefetch_related("comments")
        else:
            notes = Note.objects.filter(open_range=group).prefetch_related("comments")

        if group == "python_members" and request.user.python_student:
            python_notes = Note.objects.filter(open_range="python_members")
            tags = Tag.objects.filter(note_to__in=python_notes)
        elif group == "subscribers" and request.user.staff:
            subscribe_notes = Note.objects.filter(open_range="subscribers")
            tags = Tag.objects.filter(note_to__in=subscribe_notes)
        else:
            raise Http404("ページが見つかりません")
        context = {"notes": notes, "tags": tags}
        return render(request, "forum_note/note_list.html", context)


class NoteListTag(LoginRequiredMixin404, View):
    def get(self, request, tag_word, *args, **kwargs):
        match_notes = Note.objects.filter(tags__search_word=tag_word)
        if len(match_notes) == 0:
            raise Http404("ページが見つかりません")
        tags = Tag.objects.filter(search_word=tag_word)
        context = {"notes": match_notes, "tags": tags}
        return render(request, "forum_note/note_list.html", context)


def NoteDetail(request, pk):
    return HttpResponse(b"Note detail")


def NotePost(request):
    return HttpResponse(b"Note post")
