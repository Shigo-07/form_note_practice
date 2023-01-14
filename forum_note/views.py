from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.db.models import Q
from django.contrib import messages

from forum_note.models import Note, Comment, Tag
from forum_note.forms import NewNoteForm, CommentForm


class CheckUserAuthority(UserPassesTestMixin):
    def test_func(self):
        note_instance = get_object_or_404(Note, pk=self.kwargs["pk"])
        try:
            if note_instance.open_range == "python_members":
                return self.request.user.python_student
            if note_instance.open_range == "subscribers":
                return self.request.user.staff
            if note_instance.open_range == "public":
                return True
        except AttributeError:
            return False

    def handle_no_permission(self):
        raise Http404("ページが見つかりません")


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
                notes = notes.order_by("-created_at")

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
                notes = notes.order_by("-created_at")
            else:
                notes = Note.objects.filter(open_range=range).prefetch_related("comments")
                notes = notes.order_by("-created_at")
            public_notes = Note.objects.filter(open_range="public")
            tags = set(Tag.objects.filter(note_to__in=public_notes))

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
            notes = notes.order_by("-created_at")
        else:
            notes = Note.objects.filter(open_range=group).prefetch_related("comments")
            notes = notes.order_by("-created_at")

        if group == "python_members" and request.user.python_student:
            python_notes = Note.objects.filter(open_range="python_members")
            tags = set(Tag.objects.filter(note_to__in=python_notes))
        elif group == "subscribers" and request.user.staff:
            subscribe_notes = Note.objects.filter(open_range="subscribers")
            tags = set(Tag.objects.filter(note_to__in=subscribe_notes))
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


class NoteDetail(CheckUserAuthority, LoginRequiredMixin404, View):

    def get(self, request, pk, *args, **kwargs):
        context = {}
        note = get_object_or_404(Note, pk=pk)
        comments = Comment.objects.filter(note_to__pk=pk)
        tags = set(Tag.objects.filter(note_to__pk=pk))
        form = CommentForm()
        context["note"] = note
        context["comments"] = comments
        context['form'] = form
        context['tags'] = tags
        return render(request, "forum_note/note_detail.html", context)

    def post(self, request, pk, *args, **kwargs):
        form = CommentForm(request.POST, request.FILES)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.created_by = request.user
            new_comment.note_to = get_object_or_404(Note, pk=pk)
            new_comment.save()
        messages.success(request, "コメントの投稿が完了しました！")
        return redirect("note:note_detail", pk=pk)


class NotePost(LoginRequiredMixin404, View):
    def get(self, request, *args, **kwargs):
        form = NewNoteForm()
        context = {"form": form}
        return render(request, "forum_note/note_post.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = NewNoteForm(request.POST, request.FILES)
        form.user = request.user
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            ip_publish_mail = form.cleaned_data["is_publish_mail"]
            attach_file = form.cleaned_data["attach_file"]
            attach_image = form.cleaned_data["attach_image"]
            open_range = form.cleaned_data["open_range"]
            created_by = request.user

            obj = Note(
                title=title,
                content=content,
                is_publish_mail=ip_publish_mail,
                attach_file=attach_file,
                attach_image=attach_image,
                created_by=created_by,
                open_range=open_range,
            )
            obj.save()
            for tag in form.cleaned_data["tags"]:
                tag.note_to.add(obj)
            messages.success(request, "記事の投稿が完了しました！")
            return redirect("note:note_detail", obj.pk)

        return render(request, "forum_note/note_post.html", {"form": form})
