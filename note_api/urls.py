from django.urls import path, include
from .views import NoteDetailApiView, NoteListApiView

urlpatterns = [
    path('api', NoteListApiView.as_view()),
    path('api/<int:note_id>/', NoteDetailApiView.as_view())
]
