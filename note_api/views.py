from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Note
from .serializers import NoteSerializer

class NoteListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs) -> Response:
        notes = Note.objects.filter(user = request.user.id)
        serializer = NoteSerializer(notes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs) -> Response:
        data = extract_note_data(request)
        return self.create_note(data)

    def create_note(self, data):
        serializer = NoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def extract_note_data(request):
    data = {
        'text': request.data.get('text'),
        'timestamp': request.data.get('timestamp'),
        'priority': request.data.get('priority'),
        'user': request.user.id
    }

    return data

class NoteDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, note_id, *args, **kwargs):
        note = self.get_note(note_id, request.user.id)
        if not note:
            return Response(
                {"res": "Object with that id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(NoteSerializer(note).data, status=status.HTTP_200_OK)

    def get_note(self, note_id, user_id):
        try:
            return Note.objects.get(id=note_id, user = user_id)
        except Note.DoesNotExist:
            return None

    def put(self, request, note_id, *args, **kwargs):
        note = self.get_note(note_id, request.user.id)
        if not note:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        data = extract_note_data(request)
        return self.update_note(note, data)

    def update_note(self, note, data):
        serializer = NoteSerializer(instance = note, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, note_id, *args, **kwargs):
        note = self.get_note(note_id, request.user.id)
        if not note:
            return Response(
                {"res": "Object with that note id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        return self.delete_note(note)

    def delete_note(self, note):
        note.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
