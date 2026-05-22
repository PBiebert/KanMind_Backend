from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotFound

from kan_mind.models import Board, Task, Comment


class IsBoardMemberOrOwner(BasePermission):
    """
    Allows access only for members or the owner of a board.

    DELETE requests are restricted to the owner only.
    All other methods are allowed for both owner and members.
    """

    def has_object_permission(self, request, view, obj):
        """Checks if the user is the owner (for DELETE) or a member of the board."""
        user = request.user
        if request.method == "DELETE":
            return obj.owner == user
        return obj.owner == user or user in obj.members.all()


class IsBoardMember(BasePermission):
    """
    Allows access only for members of the associated board.

    Checked on both list and detail level.
    If board_id is missing in the request data, access is allowed.
    """

    def has_permission(self, request, view):
        """
        Checks at the list level if the user is a member of the board.

        Reads board_id from the request data. If no board with this ID exists,
        access is denied.
        """
        board_id = request.data.get("board")
        user = request.user

        if not board_id:
            return True

        try:
            board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            raise NotFound("Board not Found")
        return user in board.members.all()

    def has_object_permission(self, request, view, obj):
        """Checks at the object level if the user is a member of the associated board."""
        user = request.user
        board = obj.board
        return user in board.members.all()


class IsCreatorOrOwner(BasePermission):
    """
    Allows access only for the creator of the task or the owner of the board.
    """

    def has_object_permission(self, request, view, obj):
        """Returns True if the user is the board owner or the task creator."""
        user = request.user
        board = obj.board

        if user == board.owner or user == obj.creator:
            return True


class IsCommentBoardMember(BasePermission):
    """
    Allows access to comments only for members of the associated board.

    Determines the board via the task ID from the URL parameters.
    Raises NotFound if the task does not exist.
    """

    def has_permission(self, request, view):
        """
        Checks if the user is a member of the board to which the task belongs.

        The task ID is read from the URL kwargs (pk).
        """
        user = request.user
        task_id = view.kwargs.get("pk")

        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            raise NotFound("Task not found")
        board = task.board
        return user in board.members.all()


class IsCommentAuthor(BasePermission):
    """
    Allows access to a comment only for its author.
    """

    def has_object_permission(self, request, view, obj):
        """Returns True if the logged-in user is the author of the comment."""
        return obj.author == request.user
