from django.shortcuts import render
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.contrib.auth.models import User
from .serializers import GetUserSerializer, CreateUserSerializer, UserTokenObtainPairSerializer

from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.
class UserListApiView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs) -> Response:
        notes = User.objects
        serializer = GetUserSerializer(notes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class UserCreateApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs) -> Response:
        data = extract_user_data(request)
        return self.create_user(data)

    def create_user(self, data):
        serializer = CreateUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def extract_user_data(request):
    data = {
        'username': request.data.get('username'),
        'email': request.data.get('email'),
        'password': request.data.get('password')
    }

    return data


class UserObtainTokenPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserTokenObtainPairSerializer
