from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response

from kan_mind.models import Board, Task, Comment
from .premissions import IsBoardMemberOrOwner, IsBoardMember, IsCommentBoardMember, IsCommentAuthor
from .serializers import BoardSerializer, BoardDetailSerializer, TaskSerializer, BoardDetailPatchSerializer, TaskCommentSerializer

User = get_user_model()


class BoardView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user
        queryset = Board.objects.filter(
            Q(owner=user) | Q(members=user)).distinct()
        serializer = BoardSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = BoardSerializer(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardDetailSerializer
    permission_classes = [IsBoardMemberOrOwner]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return BoardDetailPatchSerializer
        return BoardDetailSerializer


class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsBoardMember]

    def create(self, request, *args, **kwargs):
        serializer = TaskSerializer(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)


class CommentView(generics.ListCreateAPIView):
    queryset = Comment
    serializer_class = TaskCommentSerializer
    permission_classes = [IsCommentBoardMember]

    def get(self, request, *args, **kwargs):
        task = Task.objects.get(pk=self.kwargs.get('pk'))
        comment_list = task.comment.all()
        serializer = TaskCommentSerializer(comment_list, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = TaskCommentSerializer(
            data=request.data)
        task = Task.objects.get(pk=self.kwargs.get('pk'))

        if serializer.is_valid():
            serializer.save(author=request.user, task=task)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class DeleteCommentView(generics.DestroyAPIView):
    queryset = Comment
    serializer_class = TaskCommentSerializer
    permission_classes = [IsCommentAuthor]
    lookup_field = "id"
    lookup_url_kwarg = "comment_id"
