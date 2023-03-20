from django.urls import path, include
from .views import UserListApiView, UserCreateApiView, UserObtainTokenPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/', UserListApiView.as_view()),
    path('api/register', UserCreateApiView.as_view()),
    path('api/login/', UserObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
