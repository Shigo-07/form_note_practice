from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def NoteListRange(request, range):
    return HttpResponse(b"Note list Range")


def NoteListTag(request, tag_name):
    return HttpResponse(b"Note list Tag")


def NoteDetail(request, pk):
    return HttpResponse(b"Note detail")


def NotePost(request):
    return HttpResponse(b"Note post")
