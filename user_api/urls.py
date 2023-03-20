from django.urls import path, include
from .views import UserListApiView, UserCreateApiView

urlpatterns = [
    path('api/', UserListApiView.as_view()),
    path('api/register', UserCreateApiView.as_view()),
]
