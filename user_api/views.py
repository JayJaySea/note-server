from django.shortcuts import render
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserTokenObtainPairSerializer

from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.
class UserListApiView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs) -> Response:
        notes = User.objects
        serializer = UserSerializer(notes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserCreateApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs) -> Response:
        user = User.objects.filter(username=request.data.get("username"))
        if not user:
            user = User.objects.create_user(
                request.data.get("username"),
                request.data.get("email"),
                request.data.get("password")
            )
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"detail": "User already exists!"},
                status=status.HTTP_409_CONFLICT
            )


class UserObtainTokenPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserTokenObtainPairSerializer


class UserProfileApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    allowed_update = [ "username", "email", "password" ]

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = User.objects.filter(username=request.data.get("username"))
        if user:
            return Response(
                {"detail": "User already exists!"},
                status=status.HTTP_409_CONFLICT
            )

        user = User.objects.get(id=request.user.id)

        for key in request.data.keys():
            if key in user and key in self.allowed_update:
                if key == "password":
                    user.set_password(request.data[key])
                else:
                    user[key] = request.data[key]

        return self.update_user(user)

    def update_user(self, data):
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        user.delete()
        
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
