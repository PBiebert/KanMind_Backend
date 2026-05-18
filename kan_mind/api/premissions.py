from rest_framework.permissions import BasePermission

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

# nochmal überarbeiten


class IsCommentBoardMember(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        task_id = view.kwargs.get("pk")
        task = Task.objects.get(pk=task_id)
        board = task.board

        try:
            board
        except Board.DoesNotExist:
            return False
        return user in board.members.all()


class IsCommentAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
