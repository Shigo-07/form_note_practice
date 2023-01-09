"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from forum_note import views

app_name = "note"
urlpatterns = [
    path("create/", views.NotePost, name="note_post"),
    path("g/<slug:group>/", views.NoteListGroup.as_view(), name="note_list_group"),
    path("<slug:range>/", views.NoteListRange.as_view(), name="note_list_range"),
    path("tag/<slug:tag_word>/", views.NoteListTag.as_view(), name="note_list_tag"),
    path("entry/<int:pk>/", views.NoteDetail, name="note_detail"),
]
