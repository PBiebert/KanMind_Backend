from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotFound

from kan_mind.models import Board, Task, Comment


class IsBoardMemberOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if (
            request.method == "DELETE"
        ):
            return obj.owner == user
        return obj.owner == user or user in obj.members.all()


class IsBoardMember(BasePermission):
    def has_permission(self, request, view):
        board_id = request.data.get("board")
        user = request.user

        if not board_id:
            return True

        try:
            board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            return False
        return user in board.members.all()

    def has_object_permission(self, request, view, obj):
        user = request.user
        board = obj.board
        return user in board.members.all()


class IsCreatorOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        board = obj.board

        if user == board.owner or user == obj.creator:
            return True


class IsCommentBoardMember(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        task_id = view.kwargs.get("pk")

        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            raise NotFound('Task not found')
        board = task.board
        return user in board.members.all()


class IsCommentAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
