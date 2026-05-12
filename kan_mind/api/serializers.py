from rest_framework import serializers
from kan_mind.models import Board
from django.contrib.auth import get_user_model

User = get_user_model()


class BoardSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(
        read_only=True, source='owner')
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True)
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['title', 'owner_id', 'members', 'member_count']

    def get_member_count(self, obj):
        return obj.members.count()

    def create(self, validated_data):
        members = validated_data.pop('members', [])
        user = self.context['request'].user
        board = Board.objects.create(owner=user, **validated_data)
        board.members.set(members)
        return board


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']


class BoardDetailSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all()
    )

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members']
