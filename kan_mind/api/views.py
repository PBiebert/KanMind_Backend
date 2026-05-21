from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from kan_mind.models import Board, Task, Comment
from .premissions import (
    IsBoardMemberOrOwner,
    IsBoardMember,
    IsCommentBoardMember,
    IsCommentAuthor,
    IsCreatorOrOwner,
)
from .serializers import (
    BoardSerializer,
    BoardDetailSerializer,
    TaskSerializer,
    BoardDetailPatchSerializer,
    TaskCommentSerializer,
    UpdateSingleTaskSerializer,
)

User = get_user_model()


class BoardView(generics.ListCreateAPIView):
    """
    API view for listing and creating boards.

    Returns only boards where the logged-in user
    is owner or member.
    """

    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsBoardMemberOrOwner]

    def list(self, request, *args, **kwargs):
        """Returns all boards the user belongs to (as owner or member)."""
        user = self.request.user
        queryset = Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()
        serializer = BoardSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Creates a new board with the logged-in user as owner."""
        serializer = BoardSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a single board.

    For PATCH requests, BoardDetailPatchSerializer is used,
    which returns owner and members as nested objects.
    """

    queryset = Board.objects.all()
    serializer_class = BoardDetailSerializer
    permission_classes = [IsBoardMemberOrOwner]

    def get_serializer_class(self):
        """Selects the serializer based on the HTTP method."""
        if self.request.method == "PATCH":
            return BoardDetailPatchSerializer
        return BoardDetailSerializer


class AssignedToMeTasksView(generics.ListAPIView):
    """
    API view for retrieving all tasks assigned to the logged-in user.
    """

    queryset = Task
    serializer_class = TaskSerializer

    def get_queryset(self):
        """Filters tasks by the currently logged-in user as assignee."""
        user = self.request.user
        return Task.objects.filter(assignee=user)


class ReviewingTasksView(generics.ListAPIView):
    """
    API view for retrieving all tasks where the logged-in user is set as reviewer.
    """

    queryset = Task
    serializer_class = TaskSerializer

    def get_queryset(self):
        """Filters tasks by the currently logged-in user as reviewer."""
        user = self.request.user
        return Task.objects.filter(reviewer=user)


class SingleTaskView(
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView
):
    """
    API view for updating (PATCH) and deleting (DELETE) a single task.

    DELETE is only allowed for the creator of the task or the board owner.
    PATCH is allowed for all board members.
    """

    queryset = Task.objects.all()
    serializer_class = UpdateSingleTaskSerializer

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsCreatorOrOwner()]
        return [IsBoardMember()]

    def get_permissions(self):
        """Sets permissions depending on the HTTP method."""
        if self.request.method == "DELETE":
            permission_classes = [IsCreatorOrOwner]
        else:
            permission_classes = [IsBoardMember]
        return [permission() for permission in permission_classes]

    def patch(self, request, *args, **kwargs):
        """Partially updates a task (partial update)."""
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Deletes a task."""
        return self.destroy(request, *args, **kwargs)


class TaskCreateView(generics.CreateAPIView):
    """
    API view for creating a new task.

    Only accessible to members of the associated board.
    The logged-in user is automatically set as creator.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsBoardMember]

    def create(self, request, *args, **kwargs):
        """Creates a new task and sets the logged-in user as creator."""
        serializer = TaskSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class CommentView(generics.ListCreateAPIView):
    """
    API view for retrieving and creating comments for a task.

    The task is identified via the URL parameter (pk).
    Only accessible to members of the associated board.
    """

    queryset = Comment
    serializer_class = TaskCommentSerializer
    permission_classes = [IsCommentBoardMember]

    def get(self, request, *args, **kwargs):
        """Returns all comments for the specified task."""
        task = Task.objects.get(pk=self.kwargs.get("pk"))
        comment_list = task.comment.all()
        serializer = TaskCommentSerializer(comment_list, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Creates a new comment and assigns it to the task and author."""
        serializer = TaskCommentSerializer(data=request.data)
        task = Task.objects.get(pk=self.kwargs.get("pk"))

        if serializer.is_valid():
            serializer.save(author=request.user, task=task)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class DeleteCommentView(generics.DestroyAPIView):
    """
    API view for deleting a single comment.

    Only the author of the comment is allowed to delete it.
    The comment is identified via comment_id in the URL.
    """

    queryset = Comment
    serializer_class = TaskCommentSerializer
    permission_classes = [IsCommentAuthor]
    lookup_field = "id"
    lookup_url_kwarg = "comment_id"
