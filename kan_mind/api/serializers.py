from django.contrib.auth import get_user_model
from rest_framework import serializers

from kan_mind.models import Board, Task, Comment

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "fullname"]


class TaskCommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        read_only=True,)
    author = serializers.CharField(source='author.fullname', read_only=True)
    content = serializers.CharField()

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']


class TaskSerializer(serializers.ModelSerializer):
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
            "comments_count"
        ]

    def get_comments_count(self, obj):
        return obj.comment.count()


class TaskSerializerWithoutBoardId(TaskSerializer):
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
            "comments_count"
        ]


class UpdateSingleTaskSerializer(TaskSerializer):

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
            "comments_count"
        ]


class BoardDetailSerializer(serializers.ModelSerializer):
    members = UserDetailSerializer(many=True, read_only=True)
    tasks = TaskSerializerWithoutBoardId(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "owner_id", "members", "tasks"]


class BoardDetailPatchSerializer(serializers.ModelSerializer):
    members_data = UserDetailSerializer(
        many=True, read_only=True, source='members')
    owner_data = UserDetailSerializer(read_only=True, source='owner')

    class Meta:
        model = Board
        fields = ["id", "title", "owner_data", "members_data"]


class BoardSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(
        read_only=True, source="owner")
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True)
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ["id", "title", "member_count", "ticket_count", "tasks_to_do_count", "tasks_high_prio_count", "owner_id", "members",
                  ]

    def get_member_count(self, obj):
        return obj.members.count()

    def get_ticket_count(self, obj):
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status="to-do").count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(status="high").count()

    def create(self, validated_data):
        members = validated_data.pop("members", [])
        user = self.context["request"].user
        board = Board.objects.create(owner=user, **validated_data)
        board.members.set(members)
        return board
