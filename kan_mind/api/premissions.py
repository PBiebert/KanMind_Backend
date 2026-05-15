from rest_framework.permissions import BasePermission

from kan_mind.models import Board, Task, Comment


class IsBoardMemberOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # request: Das aktuelle Request-Objekt (enthält User, Methode etc.)
        # view: Die aktuelle View-Instanz (könnte für komplexere Checks genutzt werden)
        # obj: Das Board-Objekt, auf das zugegriffen werden soll
        user = request.user  # Der aktuell angemeldete User
        if (
            request.method == "DELETE"
        ):  # Wenn die HTTP-Methode DELETE ist, darf nur der Owner löschen
            return obj.owner == user
        # Für alle anderen Methoden (GET, PATCH, etc.): Owner oder Mitglied darf zugreifen
        return obj.owner == user or user in obj.members.all()


class IsBoardMember(BasePermission):
    def has_permission(self, request, view):
        board_id = request.data.get("board")
        board = Board.objects.get(id=board_id)
        user = request.user

        try:
            board
        except Board.DoesNotExist:
            return False
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
