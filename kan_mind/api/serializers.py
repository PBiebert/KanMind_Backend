from django.contrib.auth import get_user_model
from rest_framework import serializers

from kan_mind.models import Board, Task, Comment

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for compact user representation.

    Returns id, email, and fullname. Used as a nested
    serializer in other serializers.
    """

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]


class TaskCommentSerializer(serializers.ModelSerializer):
    """
    Serializer for representing comments of a task.

    Returns id, creation timestamp, author's full name,
    and the comment content.
    """

    created_at = serializers.DateTimeField(
        read_only=True,
    )
    author = serializers.CharField(source="author.fullname", read_only=True)
    content = serializers.CharField()

    class Meta:
        model = Comment
        fields = ["id", "created_at", "author", "content"]


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for tasks including board reference.

    Assignee and reviewer can be set by ID (write-only) and
    are returned as nested objects (read-only).
    Also includes the number of related comments.
    """

    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="assignee", write_only=True, required=False
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="reviewer", write_only=True, required=False
    )
    assignee = UserDetailSerializer(read_only=True)
    reviewer = UserDetailSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "board",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "assignee_id",
            "reviewer",
            "reviewer_id",
            "due_date",
            "comments_count",
        ]

    def get_comments_count(self, obj):
        """Returns the number of comments for the task."""
        return obj.comment.count()


class TaskSerializerWithoutBoardId(TaskSerializer):
    """
    Variant of TaskSerializer without the board field.

    Used e.g. for nested representation of tasks
    within a board, since board membership is already
    clear from the context.
    """

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "assignee_id",
            "reviewer",
            "reviewer_id",
            "due_date",
            "comments_count",
        ]


class UpdateSingleTaskSerializer(TaskSerializer):
    """
    Serializer for updating a single task (PATCH/PUT).

    Inherits from TaskSerializer but excludes the board field,
    since the board should not be changed on update.
    """

    class Meta(TaskSerializer.Meta):
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "assignee_id",
            "reviewer",
            "reviewer_id",
            "due_date",
            "comments_count",
        ]


class BoardDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the detailed view of a board.

    Returns members and tasks as fully nested objects.
    """

    members = UserDetailSerializer(many=True, read_only=True)
    tasks = TaskSerializerWithoutBoardId(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "owner_id", "members", "tasks"]


class BoardDetailPatchSerializer(serializers.ModelSerializer):
    """
    Serializer for PATCH requests on a board.

    Returns owner and members as nested objects.
    Used to represent the current board data in the response after an update.
    """

    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True
    )
    members_data = UserDetailSerializer(many=True, read_only=True, source="members")
    owner_data = UserDetailSerializer(read_only=True, source="owner")

    class Meta:
        model = Board
        fields = ["id", "title", "members", "owner_data", "members_data"]


class BoardSerializer(serializers.ModelSerializer):
    """
    Serializer for the list representation of boards.

    Includes aggregated metrics such as member count, ticket count,
    number of open tasks (to-do), and high-priority tasks.
    Members are provided by ID when creating (write-only).
    """

    owner_id = serializers.PrimaryKeyRelatedField(read_only=True, source="owner")
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True
    )
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "member_count",
            "ticket_count",
            "tasks_to_do_count",
            "tasks_high_prio_count",
            "owner_id",
            "members",
        ]

    def get_member_count(self, obj):
        """Returns the number of members of the board."""
        return obj.members.count()

    def get_ticket_count(self, obj):
        """Returns the total number of tasks (tickets) of the board."""
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        """Returns the number of tasks with status 'to-do'."""
        return obj.tasks.filter(status="to-do").count()

    def get_tasks_high_prio_count(self, obj):
        """Returns the number of tasks with high priority."""
        return obj.tasks.filter(status="high").count()

    def create(self, validated_data):
        """
        Creates a new board and assigns the members.

        The logged-in user is automatically set as the owner.
        Member IDs are extracted from the validated data
        and assigned to the board after creation.
        """
        members = validated_data.pop("members", [])
        user = self.context["request"].user
        board = Board.objects.create(owner=user, **validated_data)
        board.members.set(members)
        return board
