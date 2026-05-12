from rest_framework.response import Response
from rest_framework import generics
from django.db.models import Q
from django.contrib.auth import get_user_model
from kan_mind.models import Board, Task
from .serializers import BoardSerializer, BoardDetailSerializer, TaskSerializer

User = get_user_model()


class BoardView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def list(self, request):
        user = self.request.user
        queryset = Board.objects.filter(
            Q(owner=user) | Q(members=user)).distinct()
        serializer = BoardSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = BoardSerializer(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class BoardDetailView(generics.RetrieveUpdateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardDetailSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        obj = self.get_object()
        if obj.owner == user or user in obj.members.all():
            serializer = self.serializer_class(obj)
            return Response(serializer.data)
        else:
            return Response({"detail": "The user must be either a member of the board or the owner of the board."}, status=403)

    def patch(self, request, *args, **kwargs):
        user = self.request.user
        obj = self.get_object()
        serializer = self.serializer_class(
            obj, data=request.data, partial=True)
        if obj.owner == user or user in obj.members.all():
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response({"detail": "The user must be either a member of the board or the owner of the board."}, status=403)

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        obj = self.get_object()
        if obj.owner == user:
            obj.delete()
            return Response(status=204)
        else:
            return Response({"detail": "The user must be the owner of the board."}, status=403)


class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
