from django.urls import path, include
from .views import NoteListApiView

urlpatterns = [
    path('api', NoteListApiView.as_view())
]
